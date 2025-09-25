import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm, t

# Données 
donnees = np.array([54.8, 55.4, 57.7, 59.6, 60.1, 61.2, 62.0, 63.1, 63.5, 64.2,
                 65.2, 65.4, 65.9, 66, 67.6, 68.1, 69.5, 70.6, 71.5, 73.4, 75, 75.2])

# 1
moyenne_echantillon = np.mean(donnees)
ecart_type_echantillon = np.std(donnees, ddof=1)
print('\n', "1)")
print(f"La moyenne des échantillons est : me = {moyenne_echantillon}")
print(f"L'écratt type est : Et = {ecart_type_echantillon}")

# 4. Estimation des paramètres de la loi normale
moyenne_population = moyenne_echantillon
ecart_type_population = ecart_type_echantillon
print('\n', "4)")
print(f"La moyenne de la population est : m = {moyenne_population}")
print(f"L'écratt type est : Etp = {ecart_type_population}")

# (b) Distribution de T
degre_liberte = len(donnees) - 1
t_distribution = t(degre_liberte)

# (c) Intervalle de confiance pour la moyenne
alpha = 0.05
t_critique = t_distribution.ppf(1 - alpha/2)
marge_erreur = t_critique * (ecart_type_echantillon / np.sqrt(len(donnees)))

intervalle_confiance = (moyenne_echantillon - marge_erreur, moyenne_echantillon + marge_erreur)
print('\n', "c)")
print(f"Intervalle de confiance (95%) : {intervalle_confiance}")

# (d) Tracé de la courbe de densité de probabilité de X
plt.hist(donnees, bins='auto', density=True, edgecolor='black')
x = np.linspace(min(donnees), max(donnees), 100)
plt.plot(x, norm.pdf(x, moyenne_population, ecart_type_population), label='Densité de probabilité')
plt.xlabel('Niveau de bruit (dB)')
plt.ylabel('Fréquence relative / Densité de probabilité')
plt.legend()
plt.show()

# (e) Probabilité que le niveau de bruit dépasse 70 dB
probabilite_superieure_70 = 1 - norm.cdf(70, moyenne_population, ecart_type_population)
print('\n', "e)")
print(f"Probabilité que le niveau de bruit dépasse 70 dB : {probabilite_superieure_70:.4f}")

# (f) Probabilité que le niveau de bruit soit entre 60 dB et 75 dB
probabilite_entre_60_75 = norm.cdf(75, moyenne_population, ecart_type_population) - norm.cdf(60, moyenne_population, ecart_type_population)
print('\n', "f)")
print(f"Probabilité que le niveau de bruit soit entre 60 dB et 75 dB : {probabilite_entre_60_75:.4f}")

# (g) Déterminer t1 tel que P(X < t1) = 0,95
t1 = t_distribution.ppf(0.95)
print(f"t1 tel que P(X < t1) = 0.95 : {t1:.4f}")

# (h) Déterminer t2 tel que P(X >= t2) = 0,25
t2 = t_distribution.ppf(0.75)  # P(X >= t2) = 1 - P(X < t2) = 0.25
print('\n', "g)")
print(f"t2 tel que P(X >= t2) = 0.25 : {t2:.4f}")
