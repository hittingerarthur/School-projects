import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, expon, chisquare, ttest_ind

# Chargement des données à partir du fichier CSV
chemin_fichier = '/Users/arthurhittinger/Downloads/PROJETMA325 copie/Donn,es.csv'
df = pd.read_csv(chemin_fichier)

# Affichage des premières lignes pour vérifier le chargement des données
print(df.head())

# Calcul des moyennes et écarts-types pour chaque matière
moyennes = df.mean()
ecarts_types = df.std()
print("Moyennes pour chaque matière :", moyennes)
print("Écarts-types pour chaque matière :", ecarts_types)

# Exclusion des colonnes non numériques si nécessaire
df = df.select_dtypes(include=[np.number])

# Calcul des moyennes et écarts-types pour chaque colonne
moyennes = df.mean()
ecarts_types = df.std()

# Remplacement des NaN par la moyenne de chaque colonne (imputation)
df_filled = df.fillna(moyennes)

# Centrage et réduction des données
df_scaled = (df_filled - moyennes) / ecarts_types

# Conversion des données centrées et réduites en array NumPy
data_array = df_scaled.to_numpy()

# Calcul de la matrice de covariance des données centrées et réduites
matrice_covariance = np.cov(data_array, rowvar=False)  # Utilisation de rowvar=False pour calculer sur les colonnes

# Calcul des valeurs propres et des vecteurs propres de la matrice de covariance
valeurs_propres, vecteurs_propres = np.linalg.eig(matrice_covariance)

# Trier les valeurs propres en ordre décroissant et réorganiser les vecteurs propres correspondants
indices_tri = np.argsort(valeurs_propres)[::-1]
valeurs_propres = valeurs_propres[indices_tri]
vecteurs_propres = vecteurs_propres[:, indices_tri]

# Affichage des valeurs propres et des proportions de variance expliquée
print("Valeurs propres :", valeurs_propres)
proportions_variance = valeurs_propres / np.sum(valeurs_propres)
print("Proportions de variance expliquée :", proportions_variance)

# Tracé du graphique de proportion des variances
plt.figure(figsize=(8, 4))
plt.plot(proportions_variance, marker='o', linestyle='-', color='b')
plt.title('Proportion de variance expliquée par chaque axe')
plt.xlabel('Numéro de l’axe')
plt.ylabel('Proportion de variance')
plt.show()

# Tracé du cumul de variance restituée
plt.figure(figsize=(8, 4))
plt.plot(np.cumsum(proportions_variance), marker='o', linestyle='-', color='r')
plt.title('Cumul de variance expliquée')
plt.xlabel('Numéro de l’axe')
plt.ylabel('Cumul de variance expliquée')
plt.show()

# Projection des données sur les axes principaux
df_pca = np.dot(data_array, vecteurs_propres)
print("Coordonnées factorielles (projection des données sur les axes principaux) :")
print(df_pca)

# Affichage des pourcentages de variance portés par les axes
print("\nPourcentage de variance expliquée par chaque axe:")
for i, var in enumerate(proportions_variance):
    print(f"Axe {i + 1}: {var * 100:.2f}%")

# Calcul des carrés des distances
distances_carres = np.sum(df_pca ** 2, axis=1)
print("Distances carrées")
print(distances_carres)

# Calcul de la qualité de représentation sur les axes (COS2)
cos2 = df_pca ** 2 / distances_carres[:, np.newaxis]
print("cos2")
print(cos2)

# Contribution des individus aux axes (CTR)
ctr = df_pca ** 2 / (valeurs_propres * len(df))

# Vérification de la somme des CTR pour chaque axe
ctr_sums = np.sum(ctr, axis=0)

# Affichage des résultats
print("Somme des CTR pour chaque axe:")
print(ctr_sums)

# Affichage de la contribution des individus aux axes
print("Contribution des individus aux axes (CTR):")
print(ctr)

# Tracer des résultats pour le premier axe
plt.figure(figsize=(10, 5))
plt.bar(range(len(df)), ctr[:, 0], alpha=0.7)
plt.title("Contribution des individus à l'axe 1 (CTR)")
plt.xlabel("Individu")
plt.ylabel("CTR")
plt.show()

# Projection des individus sur les deux premières composantes principales
df_pca = np.dot(data_array, vecteurs_propres[:, :2])

# Projection des variables sur les deux premières composantes principales (vecteurs de corrélation)
loadings = vecteurs_propres[:, :2] * np.sqrt(valeurs_propres[:2])

# Tracer la projection des individus
plt.figure(figsize=(10, 5))
plt.scatter(df_pca[:, 0], df_pca[:, 1], alpha=0.7)
plt.xlabel('Première composante principale')
plt.ylabel('Deuxième composante principale')
plt.title('Projection des individus sur les deux premières composantes principales')
plt.grid(True)

# Tracer le cercle des corrélations pour les variables
plt.figure(figsize=(10, 5))
circle = plt.Circle((0, 0), 1, color='gray', fill=False)
plt.gca().add_artist(circle)
plt.scatter(loadings[:, 0], loadings[:, 1], color='red')
for i, txt in enumerate(df.columns):
    plt.annotate(txt, (loadings[i, 0], loadings[i, 1]))
plt.xlabel('Première composante principale')
plt.ylabel('Deuxième composante principale')
plt.title('Cercle des corrélations')
plt.grid(True)
plt.axis('equal')  # Assurer que les proportions sont égales pour bien visualiser le cercle

plt.show()

# Calcul de COS² pour chaque variable sur chaque axe
cos2 = loadings ** 2

# Vérification de la somme des COS² pour chaque variable
cos2_sums = np.sum(cos2, axis=1)

# Affichage des résultats
print("COS² (Qualité de représentation des variables sur les axes):")
print(cos2)

print("Contribution des variables aux axes (CTR):")
print(ctr)

# Tracer des résultats pour les deux axes
plt.figure(figsize=(10, 5))
plt.bar(np.arange(len(df.columns)), cos2[:, 0], alpha=0.7, label='COS² Axe 1')
plt.bar(np.arange(len(df.columns)), cos2[:, 1], alpha=0.7, label='COS² Axe 2', bottom=cos2[:, 0])
plt.xticks(np.arange(len(df.columns)), df.columns, rotation=90)
plt.ylabel('COS²')
plt.title('Qualité de la représentation des variables sur les deux premiers axes')
plt.legend()
plt.show()


def perform_chi2_test(data, lambda_est):
    observed, bin_edges = np.histogram(data, bins=10)
    # Calcul des probabilités attendues pour chaque bin
    expected_probs = expon.cdf(bin_edges[1:], scale=1 / lambda_est) - expon.cdf(bin_edges[:-1], scale=1 / lambda_est)
    # Conversion des probabilités en fréquences attendues
    expected = expected_probs * data.size
    # Ajustement pour éviter les fréquences attendues nulles ou extrêmement basses
    expected[expected < 1] = 1  # Assurez que toutes les fréquences attendues soient au moins 1
    # Normalisation des fréquences attendues pour correspondre à la somme des fréquences observées
    expected = expected / expected.sum() * observed.sum()
    if np.any(observed == 0) and np.any(expected == 0):
        expected += 1  # Petite correction pour éviter les divisions par zéro lors du calcul du chi2
        observed += 1
    chi2_stat, p_value = chisquare(observed, expected)
    return chi2_stat, p_value


# Appliquez la fonction sur vos données
lambda_x = 1 / np.mean(df_pca[:, 0])
lambda_y = 1 / np.mean(df_pca[:, 1])

chi2_stat_x, p_value_x = perform_chi2_test(df_pca[:, 0], lambda_x)
chi2_stat_y, p_value_y = perform_chi2_test(df_pca[:, 1], lambda_y)

print(f"Chi2 Statistic for X: {chi2_stat_x}, P-value: {p_value_x}")
print(f"Chi2 Statistic for Y: {chi2_stat_y}, P-value: {p_value_y}")

# Supposons que df_pca contient les deux premières composantes principales
x = df_pca[:, 0]
y = df_pca[:, 1]

# 1. Définition des variables aléatoires X et Y
mu_x, sigma_x = np.mean(x), np.std(x, ddof=1)
mu_y, sigma_y = np.mean(y), np.std(y, ddof=1)

# 2. Test de Student pour l'indépendance
t_stat, p_value = ttest_ind(x, y)
print(f"Test t pour l'indépendance de X et Y: t-statistique = {t_stat}, p-valeur = {p_value}")


# 3. Découpage en classes et test du Chi-2 pour X
def chi2_test(data, mu, sigma):
    observed, bin_edges = np.histogram(data, bins=10)
    expected_probs = norm.cdf(bin_edges[1:], mu, sigma) - norm.cdf(bin_edges[:-1], mu, sigma)
    expected = expected_probs * len(data)
    # Ajuster les fréquences attendues pour correspondre à la somme des fréquences observées
    expected = expected / np.sum(expected) * np.sum(observed)
    chi2_stat, p_val = chisquare(observed, f_exp=expected)
    return chi2_stat, p_val


chi2_stat_x, p_val_x = chi2_test(x, mu_x, sigma_x)
print(f"Chi2 test pour X: chi2-statistique = {chi2_stat_x}, p-valeur = {p_val_x}")

chi2_stat_y, p_val_y = chi2_test(y, mu_y, sigma_y)
print(f"Chi2 test pour Y: chi2-statistique = {chi2_stat_y}, p-valeur = {p_val_y}")

# Visualisation des distributions
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(x, bins=30, alpha=0.6, color='blue', density=True)
x_range = np.linspace(mu_x - 4 * sigma_x, mu_x + 4 * sigma_x, 100)
plt.plot(x_range, norm.pdf(x_range, mu_x, sigma_x), 'k', linewidth=2)
plt.title('Distribution de X avec ajustement normal')

plt.subplot(1, 2, 2)
plt.hist(y, bins=30, alpha=0.6, color='red', density=True)
y_range = np.linspace(mu_y - 4 * sigma_y, mu_y + 4 * sigma_y, 100)
plt.plot(y_range, norm.pdf(y_range, mu_y, sigma_y), 'k', linewidth=2)
plt.title('Distribution de Y avec ajustement normal')

plt.show()
