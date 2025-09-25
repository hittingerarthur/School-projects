# Import libraries
import streamlit as st
import sys

# Check if the script is being run through Streamlit
if not 'streamlit.runtime.scriptrunner.script_runner' in sys.modules:
    print("This is a Streamlit app, please run it with:")
    print("    python -m streamlit run deforestation.py")
    sys.exit(1)

import pandas as pd
import json
from shapely.geometry import shape, Polygon
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np
import geopandas
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap
from sklearn.neighbors import NearestNeighbors
import glob
import os
import folium
from streamlit_folium import st_folium  # Update the import
from PIL import Image
import warnings

# Suppress specific warnings
warnings.filterwarnings('ignore', 'invalid value encountered in area')
warnings.filterwarnings('ignore', 'invalid value encountered in centroid')
warnings.filterwarnings('ignore', 'A value is trying to be set on a copy of a slice from a DataFrame')


# 1. Data Loading and Preparation

# Define a function to process a single CSV file
def process_csv(filepath):
    try:
        df = pd.read_csv(filepath)  # Load the CSV
    except FileNotFoundError:
        print(f"Error: CSV file not found: {filepath}")
        return None

    # Create a copy of the DataFrame to avoid chained assignment warnings
    df = df.copy()
    
    # Identifier les zones d'eau en utilisant les valeurs NDVI très basses
    water_threshold = -0.1  # Seuil NDVI pour l'eau
    water_mask = df['mean'] < water_threshold
    df.loc[water_mask, 'mean'] = -1  # Water areas get -1
    df.loc[~water_mask & df['mean'].isna(), 'mean'] = np.nan  # Land areas without data stay as NaN

    # Coordinate Extraction
    df[['x', 'y']] = df['system:index'].str.split(',', expand=True)
    df.loc[:, 'x'] = df['x'].str.replace('"', '').astype(int)
    df.loc[:, 'y'] = df['y'].str.replace('"', '').astype(int)

    # Geometry Creation
    def create_geometry(geo_json):
        try:
            data = json.loads(geo_json)
            if data['type'] == 'Polygon':
                polygon = Polygon(data['coordinates'][0])
                return polygon
            else:
                return None
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print(f"Error processing geometry in {filepath}: {e}")
            return None

    df['geometry'] = df['.geo'].apply(create_geometry)
    df = df.dropna(subset=['geometry'])  # drop rows with invalid geometries

    # GeoDataFrame Creation
    gdf = geopandas.GeoDataFrame(df, geometry='geometry', crs="EPSG:4326")  # WGS84
    
    # Project to a suitable projected CRS (UTM Zone 21S for DRC)
    gdf_projected = gdf.to_crs("EPSG:32721")  # UTM Zone 21S for DRC

    # Calculate centroids in projected coordinates
    gdf['centroid_x'] = gdf_projected.geometry.centroid.x
    gdf['centroid_y'] = gdf_projected.geometry.centroid.y
    
    #Impute NaN centroids (e.g., with the mean) - Better option
    gdf['centroid_x'] = gdf['centroid_x'].fillna(gdf['centroid_x'].mean())
    gdf['centroid_y'] = gdf['centroid_y'].fillna(gdf['centroid_y'].mean())

    # --- k-NN Imputation ---
    missing_ndvi = gdf[gdf['mean'].isnull()]
    available_ndvi = gdf[gdf['mean'].notnull()]
    k = 5  # Number of neighbors to use

    knn = NearestNeighbors(n_neighbors=k, algorithm='auto', metric='haversine')
    knn.fit(available_ndvi[['centroid_y', 'centroid_x']].values)

    for index, row in missing_ndvi.iterrows():
        distances, indices = knn.kneighbors(row[['centroid_y', 'centroid_x']].values.reshape(1, -1))
        neighbor_ndvi_values = available_ndvi['mean'].iloc[indices[0]].values
        gdf.loc[index, 'mean'] = np.nanmean(neighbor_ndvi_values)

    gdf.loc[water_mask, 'mean'] = -0.45  # Restore water areas to -0.45

    # Extract Date Information from Filename (crucial for time series)
    filename = os.path.basename(filepath)
    start_date_str = filename.split('_')[3]  # Get the start_date
    end_date_str = filename.split('_')[4].replace('.csv', '')  # Remove ".csv"
    gdf['start_date'] = pd.to_datetime(start_date_str)
    gdf['end_date'] = pd.to_datetime(end_date_str)
    gdf['mid_date'] = gdf[['start_date', 'end_date']].mean(axis=1)  # Create the middle

    return gdf

# Get a list of all CSV files in the directory
csv_files = glob.glob("*.csv")  # Assumes all CSV files are in the current directory

# Process each CSV file and combine the data
all_data = []
for filepath in csv_files:
    print(f"Processing: {filepath}")
    gdf = process_csv(filepath)
    if gdf is not None:
        all_data.append(gdf)

# Concatenate all GeoDataFrames into a single GeoDataFrame
combined_gdf = pd.concat(all_data, ignore_index=True)

print(f"Combined data shape: {combined_gdf.shape}")
print(combined_gdf.head())

# 2. Feature Engineering for Time Series

# Add a 'time' feature representing the days since the first observation
combined_gdf = combined_gdf.sort_values(by='mid_date')
combined_gdf['time'] = (combined_gdf['mid_date'] - combined_gdf['mid_date'].min()).dt.days

# Create a unique identifier for each spatial location
combined_gdf['location_id'] = combined_gdf['x'].astype(str) + '_' + combined_gdf['y'].astype(str)

# 3. Prepare Data for Machine Learning

features = ['x', 'y', 'centroid_x', 'centroid_y', 'time']  # Include 'time'
X = combined_gdf[features]
y = combined_gdf['mean']

# 4. Split Data into Training and Validation Sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Model Training
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Model Evaluation
y_pred = model.predict(X_val)
mse = mean_squared_error(y_val, y_pred)
print(f"Mean Squared Error: {mse}")

# 7. Prediction for Future Dates (Corrected GeoDataFrame Creation)

# To predict future forest cover, you need to create a DataFrame
# with the 'x', 'y', 'centroid_x', 'centroid_y' values for the
# locations you want to predict *and* the 'time' values for the
# future dates you want to predict.

# Example: Predict for the year 2025 (adjust as needed)
future_date = pd.to_datetime('2025-01-01')

# Create a DataFrame with all unique locations from the original dataset
unique_locations = combined_gdf[['x', 'y', 'centroid_x', 'centroid_y']].drop_duplicates()
X_future = unique_locations.copy()

# Add the future time for prediction
first_date = combined_gdf['mid_date'].min()
X_future['time'] = (future_date - first_date).days  # Days since first observation

# Make predictions for all locations
predicted_ndvi_future = model.predict(X_future[features])  # Use the same features as training

# Create the future GeoDataFrame
combined_gdf_aux = combined_gdf[['x', 'y', 'geometry']].drop_duplicates(['x', 'y'])
combined_gdf_aux = combined_gdf_aux.reset_index(drop=True)

X_future = X_future.reset_index(drop=True)
gdf_future = pd.merge(X_future, combined_gdf_aux, on=['x', 'y'], how='left')
gdf_future = geopandas.GeoDataFrame(gdf_future, geometry='geometry', crs="EPSG:4326")
gdf_future['predicted_ndvi'] = predicted_ndvi_future

# 8. Visualization (Illustrative)

# Define a custom colormap: blue -> white -> green with special handling for NaN
cdict = {
    'red':   [[0.0, 0.0, 0.0],      # Blue (water): -1 to -0.15
               [0.5, 0.0, 0.0],    # Stay Blue up to -0.15
               [0.6, 1.0, 1.0],    # Start White at 0.35
               [0.8, 1.0, 1.0],     # Stay White until 0.4
               [1.0, 0.024, 0.0]],  # Green (vegetation): 0.4 and above

    'green': [[0.0, 0.0, 0.0],
               [0.5, 0.0, 0.0],    # Stay Blue up to -0.15
               [0.6, 1.0, 1.0],    # Start White at 0.35
               [0.8, 1.0, 1.0],     # Stay White until 0.4
               [1.0, 0.251, 1.0]],

    'blue':  [[0.0, 1.0, 1.0],      # Blue (water): -1 to -0.15
               [0.5, 1.0, 1.0],    # Stay Blue up to -0.15
               [0.6, 1.0, 1.0],    # Start White at 0.35
               [0.8, 1.0, 1.0],     # Stay White until 0.4
               [1.0, 0.169, 0.0]]
}
cmap = LinearSegmentedColormap('CustomMap', cdict)
cmap.set_bad(color='white')

ndvi_min = -1
ndvi_max = combined_gdf['mean'].max()  # Use max from combined data
norm = mcolors.TwoSlopeNorm(vmin=ndvi_min, vcenter=0.0, vmax=ndvi_max)

#################### Visualisation of Results ########################

st.title("Forest Cover Prediction Dashboard")

#####################Map####################

st.subheader("Map prediction")

# Create the plot
fig, ax = plt.subplots(figsize=(12, 8))
gdf_future.plot(column='predicted_ndvi', legend=True, cmap=cmap, norm=norm, ax=ax, missing_kwds={'color': 'white'})
ax.set_title(f'Predicted NDVI Values for {future_date.strftime("%Y-%m-%d")}\nBleu: Mer | Blanc: Pas de données | Vert: Végétation')
st.pyplot(fig)

# Generate deforestation maps for each year before visualization
def generate_deforestation_maps():
    # Get unique time periods from the data
    periods = combined_gdf[['start_date', 'end_date']].drop_duplicates()
    periods = periods.sort_values('start_date')
    
    for _, period in periods.iterrows():
        # Filter data for the specific period
        period_data = combined_gdf[
            (combined_gdf['start_date'] == period['start_date']) & 
            (combined_gdf['end_date'] == period['end_date'])
        ]
        
        if not period_data.empty:
            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 8))
            period_data.plot(column='mean', legend=True, cmap=cmap, norm=norm, ax=ax, 
                           missing_kwds={'color': 'white'})
            
            # Format dates for title
            start_date = period['start_date'].strftime('%Y-%m-%d')
            end_date = period['end_date'].strftime('%Y-%m-%d')
            ax.set_title(f'Déforestation\n{start_date} à {end_date}\nBleu: Mer | Blanc: Pas de données | Vert: Végétation')
            
            # Save the plot with period dates in filename
            filename = f'deforestation_{start_date}_to_{end_date}.png'
            plt.savefig(filename, bbox_inches='tight', dpi=300)
            plt.close()

# Generate the maps before displaying them
generate_deforestation_maps()

#########################################
####################Visual data#####################
#########################################
st.subheader("Images comparison")

# Get list of generated images
image_files = glob.glob("deforestation_*.png")
image_files.sort()  # Sort by filename which contains dates

# Calculate number of rows needed (3 images per row)
images_per_row = 3
num_rows = (len(image_files) + images_per_row - 1) // images_per_row

# Display images in a grid
for row in range(num_rows):
    cols = st.columns(images_per_row)
    for col_idx in range(images_per_row):
        img_idx = row * images_per_row + col_idx
        if img_idx < len(image_files):
            # Extract dates from filename for caption
            filename = image_files[img_idx]
            dates = filename.replace('deforestation_', '').replace('.png', '').replace('_to_', ' à ')
            
            try:
                image = Image.open(filename)
                cols[col_idx].image(image, caption=dates, use_container_width=True)
            except FileNotFoundError:
                cols[col_idx].warning(f"Image non trouvée: {filename}")

#########################################
####################Table comparison#####################
#########################################
st.subheader("Pertes de Forêt Primaire Table Comparison")

# Data from your image/source
deforestation_data = {
    2019: {'pertes': 250000, 'evolution': 'Stable', 'facteurs': 'Exploitation légale'},
    2020: {'pertes': 200000, 'evolution': '-20%', 'facteurs': 'COVID-19'},
    2021: {'pertes': 230000, 'evolution': '+15%', 'facteurs': 'Retour des investissements chinois'},
    2022: {'pertes': 260000, 'evolution': '+13%', 'facteurs': 'Pression accrue'},
    2023: {'pertes': 280000, 'evolution': '+8%', 'facteurs': 'Projets routiers'}
}

# Convert to Pandas DataFrame
deforestation_df = pd.DataFrame.from_dict(deforestation_data, orient='index')
deforestation_df.index.name = 'Année'
deforestation_df = deforestation_df.reset_index()

# Make predictions
future_date = pd.to_datetime('2025-01-01')
future_time = (future_date - combined_gdf['mid_date'].min()).days
X_future
X_future = X_future.drop_duplicates(subset=['x', 'y', 'centroid_x', 'centroid_y'])
X_future['time'] = (future_date - combined_gdf['mid_date'].min()).days
predicted_ndvi_future = model.predict(X_future[features])
average_predicted_ndvi = np.mean(predicted_ndvi_future)

# Assuming a very simplistic relation between average NDVI and deforestation
# (This is just an example, you would need a better-calibrated relationship)
predicted_deforestation = int(280000 - (average_predicted_ndvi * 10000))
predicted_evolution = "Increase" if average_predicted_ndvi < 0.2 else "Decrease"
predicted_facteurs = "Impact des politiques environnementales"

# Add the prediction
deforestation_data[2025] = {'pertes': predicted_deforestation, 'evolution': predicted_evolution, 'facteurs': predicted_facteurs}

# Convert to Pandas DataFrame
deforestation_df = pd.DataFrame.from_dict(deforestation_data, orient='index')
deforestation_df.index.name = 'Année'
deforestation_df = deforestation_df.reset_index()

st.dataframe(deforestation_df)

##################END#######################