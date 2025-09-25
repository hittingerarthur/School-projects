// ===============================
// DRC LAND COVER CLASSIFICATION (2021)
// ===============================

// Define region of interest (Tropical forest in the Democratic Republic of Congo)
var drc_roi = ee.Geometry.Polygon([
  [[23, -4], [30, -4], [30, 3], [23, 3], [23, -4]]
]);

// Preprocess Sentinel-2: Select bands, scale reflectance
function preprocessS2(image) {
  return image
    .select(["B2", "B3", "B4", "B8", "B11", "B12"])
    .divide(10000);
}

// Load and process Sentinel-2 for 2021
var s2_2021 = ee.ImageCollection("COPERNICUS/S2")
  .filterBounds(drc_roi)
  .filterDate("2021-01-01", "2021-12-31")
  .filter(ee.Filter.lt("CLOUDY_PIXEL_PERCENTAGE", 10))
  .map(preprocessS2)
  .median();

// Calculate NDVI from Sentinel-2 (2021)
var ndvi_2021 = s2_2021.normalizedDifference(["B8", "B4"]).rename("NDVI");

// Load Sentinel-1 VV polarization for 2021
var s1_2021 = ee.ImageCollection("COPERNICUS/S1_GRD")
  .filterBounds(drc_roi)
  .filterDate("2021-01-01", "2021-12-31")
  .filter(ee.Filter.eq("instrumentMode", "IW"))
  .filter(ee.Filter.eq("orbitProperties_pass", "DESCENDING"))
  .select("VV")
  .median()
  .rename("Radar_VV");

// Load ALOS PALSAR DEM and derive elevation and slope
var dem = ee.Image("JAXA/ALOS/AW3D30/V2_2");
var elevation = dem.select("AVE_DSM").rename("elevation");
var resampledElevation = elevation.resample('bilinear').reproject({crs: 'EPSG:4326', scale: 30});
var slope = ee.Terrain.slope(resampledElevation).rename("slope");


// ========== TRAINING DATA ==========

// Assign class labels to training features
var water = Water.map(function(f) { return f.set("class", 0); });
var urban = Urban.map(function(f) { return f.set("class", 1); });
var forest = Forest.map(function(f) { return f.set("class", 2); });
var deforested = Deforested.map(function(f) { return f.set("class", 3); });
var agriculture = Agriculture.map(function(f) { return f.set("class", 4); });
var prairie = Prairie.map(function(f) { return f.set("class", 5); });

// Merge all labeled points into a single FeatureCollection
var trainingData = water.merge(urban).merge(forest).merge(deforested).merge(agriculture).merge(prairie);

// Stack all features into one image
var input_features_2021 = s2_2021
  .addBands(ndvi_2021)
  .addBands(s1_2021)
  .addBands(elevation)
  .addBands(slope);

// Define band names used in classification
var bands = ["B2", "B3", "B4", "B8", "B11", "B12", "NDVI", "Radar_VV", "elevation", "slope"];

// Sample the image at training point locations
var training_2021 = input_features_2021.sampleRegions({
  collection: trainingData,
  properties: ["class"],
  scale: 30
});

// Train Random Forest classifier
var classifier_2021 = ee.Classifier.smileRandomForest(100).train({
  features: training_2021,
  classProperty: "class",
  inputProperties: bands
});

// Classify the 2021 image
var classified_2021 = input_features_2021.classify(classifier_2021);

// ========== VISUALIZATION ==========

// NDVI visualization
var ndviVis = {min: 0, max: 1, palette: ["yellow", "green"]};
Map.addLayer(ndvi_2021, ndviVis, "NDVI (2021)");

// Radar visualization
var radarVis = {min: -20, max: 0, palette: ["white", "black"]};
Map.addLayer(s1_2021, radarVis, "Radar VV (2021)");

// Land cover classification visualization
var classVis = {
  min: 0,
  max: 5,
  palette: ["blue", "yellow", "green", "red", "purple", "brown"], // Water, Urban, Forest, Deforested, Agriculture, Prairie
};
Map.addLayer(classified_2021, classVis, "Land Cover Classification (2021)");

// Center map
Map.centerObject(drc_roi, 6);


// ========== ACCURACY ASSESSMENT ==========

var withRandom = training_2021.randomColumn();
var split = 0.7;
var trainingPartition = withRandom.filter(ee.Filter.lt('random', split));
var testingPartition = withRandom.filter(ee.Filter.gte('random', split));

var trainedClassifier = ee.Classifier.smileRandomForest(100).train({
  features: trainingPartition,
  classProperty: 'class',
  inputProperties: bands
});

var validated = testingPartition.classify(trainedClassifier);
var testAccuracy = validated.errorMatrix('class', 'classification');
print('Confusion Matrix', testAccuracy);
print('Overall Accuracy', testAccuracy.accuracy());


// ========== EXPORT DATA ==========

Export.image.toDrive({
  image: classified_2021,
  description: 'classified_2021',
  folder: 'GEE_exports',
  fileNamePrefix: 'classified_2021',
  region: drc_roi,
  scale: 30,
  crs: 'EPSG:4326',
  maxPixels: 1e13
});

var points = classified_2021.sample({
  region: drc_roi,
  scale: 30,
  projection: 'EPSG:4326',
  numPixels: 10000,
  geometries: true
});

Export.table.toDrive({
  collection: points,
  description: 'classified_points_2021',
  fileFormat: 'CSV'
});