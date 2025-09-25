#Exercice 6

#Probabilité que maximum 3 personnes fassent sonner le portique 

from scipy.stats import binom

#5
# Paramètres de la distribution binomiale
n = 500  # nombre d'essais (personnes)
p = 0.031175  # probabilité de succès (portique sonne)

# Calcul de la probabilité que maximum 3 personnes fassent sonner le portique
prob_max_3 = sum(binom.pmf(k, n, p) for k in range(4))

print('\n', "5)")
print(f"La probabilité que maximum 3 personnes fassent sonner le portique est : {prob_max_3:.4f}")

#6

from scipy.stats import binom

# Paramètres de la distribution binomiale
n = 500  # nombre d'essais (personnes)
p = 0.031175  # probabilité de succès (portique sonne)

# Calcul de la probabilité P(X > 250)
prob_X_gt_250 = 1 - binom.cdf(250, n, p)

print('\n', "1)")
print(f"La probabilité que plus de 250 personnes fassent sonner le portique est : {prob_X_gt_250:.4f}")

#Calcul de P(X>50) à l'aide de l'approximation d'une loi normale 

from scipy.stats import norm

# Paramètres de la distribution binomiale
n = 500  # nombre d'essais (personnes)
p = 0.031175  # probabilité de succès (portique sonne)

# Paramètres de la distribution normale (approximation)
mu = n * p
sigma = (n * p * (1 - p))**0.5

# Calcul de la probabilité P(X > 50) en utilisant l'approximation normale
prob_X_gt_50_approx = 1 - norm.cdf(50, loc=mu, scale=sigma)

print('\n', "8)")
print(f"La probabilité que plus de 50 personnes fassent sonner le portique (approximation normale) est : {prob_X_gt_50_approx:.4f}")

#Calcul de la probabilité qu'exactement 70 personnes fassent sonner le portique par une loi normale

from scipy.stats import norm

# Paramètres de la distribution binomiale
n = 500  # nombre d'essais (personnes)
p = 0.031175  # probabilité de succès (portique sonne)

# Paramètres de la distribution normale (approximation)
mu = n * p
sigma = (n * p * (1 - p))**0.5

# Calcul de la probabilité P(X = 70) en utilisant l'approximation normale
prob_X_eq_70_approx = norm.pdf(70, loc=mu, scale=sigma)

print('\n', "9)")
print(f"La probabilité que exactement 70 personnes fassent sonner le portique (approximation normale) est : {prob_X_eq_70_approx:.4e}")