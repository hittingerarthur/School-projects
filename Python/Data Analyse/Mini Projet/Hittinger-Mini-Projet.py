import math

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sb
from scipy.stats import norm, t

#           Code du projet de Sciences des données et de la décision    #  Arthur Hittinger       #

######      EXERCICE 1        #####

#1.a)

data1 = pd.read_csv("DataMP.csv",sep=";",encoding = "unicode_escape", engine="python")

#1.b)    

DATA = data1.values
print(DATA)

#1.c)

x = [ DATA[i][1] for i in range(len(DATA))]
y = [ DATA[i][2] for i in range(len(DATA))]

X = np.array(x)
Y = np.array(y)

#2) (voir graph 1)

plt.scatter(X , Y, label = "Nuage de points")

#3)

Xbarre = np.mean(X)
Ybarre = np.mean(Y)

ecX = np.std(X)
ecY = np.std(Y)

#4)

covar = np.cov(X , Y)[0][1]

#5)

coefco = covar/(ecX*ecY)

#6.a)          

slope, intercept = np.polyfit(X, Y, 1)

Y_pred = slope * X + intercept

plt.plot(X, Y_pred, color='red', label='Droite de régression')
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()

#7)

xm = Xbarre
ym = Ybarre

plt.scatter(xm, ym, color='black', label='Point moyen')
plt.title('1 : Droite de regression linéaire et nuage de points')
plt.show()

#8.a)

residuals = Y - Y_pred
vr1 = np.var(residuals)
vr2 = np.mean((Y - np.mean(Y))**2)

#8.b) 

ve1 = np.var(slope * X + intercept)
ve2 = np.cov(X, Y)[0, 1]**2 / np.var(X)

#8.c)  

var = np.var(Y)
variance_sum_method = ve1 + vr1
is_variance_equation_valid = np.isclose(var, variance_sum_method)
print(f"L'équation de la variance est vérifiée : {is_variance_equation_valid}")

#####         EXERCICE 2          #####

T2 = [0.1 , 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
V2 = [5.098, 3.618, 2.581, 2.011, 1.486, 1.028, 0.845, 0.573, 0.429, 0.29, 0.2]

#2)

Xln = np.array([math.log(T2[i]) for i in range(1, len(T2))])

#3)


Yln = np.array([math.log(V2[i]) for i in range(1, len(V2))])


plt.scatter(Xln, Yln)
plt.xlabel('Temps')
plt.ylabel('Potentiel')


slope2, intercept2 = np.polyfit(Xln, Yln, 1)

ypred2 = slope2 * Xln + intercept2

plt.xlabel('X')
plt.ylabel('Y')
plt.title('2 : Droite de regression du potentiel en fct du temps')
plt.show()


#####         EXERCICE 3          #####

anee = list(range(1944, 1963))

# 1)

XPA = np.array([100, 61, 76, 74, 90, 93, 102, 98, 103, 110, 117, 118, 112, 115, 116, 121, 134, 130])

#2) 

YPI = np.array([10 , 50 , 84, 99, 113, 122, 128, 143, 145, 159, 172, 188, 204, 213, 220, 242, 254, 273])

#3) (voir graph 2)
#4)

G = [sum(XPA)/len(XPA), sum(YPI)/len(YPI)]

plt.scatter(XPA, YPI)
plt.scatter(G[0], G[1], c = 'red')
plt.xlabel('XPA')
plt.ylabel('YPI')

#5)

covar3 = np.cov(XPA , YPI)[0][1]

#6) 

Xbarre3 = np.mean(XPA)          #Calcul des moyennes des tableaux
Ybarre3 = np.mean(YPI)

ecX3 = np.std(XPA)              #Calcul des écarts-types des variables
ecY3 = np.std(YPI)

coefco3 = covar/(ecX*ecY)       #Calcul du coef de correlation

#8.a)

a3 , b3 = np.polyfit(XPA, YPI, 1)
ypred3 = a3 * XPA + b3

plt.plot(XPA, ypred3,color = 'red')
plt.title('3 : Régression linéaire de y en x')

# 8.b) 

distance = YPI - ypred3

#8.c) 

Vr = np.var(distance)
Ve = np.var(ypred3)

#8.d)   

plt.show()

#9.a)

a3prim , b3prim = np.polyfit(YPI, XPA, 1)
xpred3 = a3prim * YPI + b3prim

plt.scatter(XPA, YPI)
plt.plot(XPA, ypred3,color = 'black')
plt.title('3 : Régression linéaire de x en y')

#9.b)

distanceprim = XPA - xpred3

# 9.c)

Vrprim = np.var(distanceprim)
Veprim = np.var(xpred3)

# 9.d)

plt.show()

#10.a)

# On a : a' = r * a

#####         EXERCICE 4              #####

#1), 2)

longueurs = np.array([153, 165, 160, 150, 159, 151, 163, 160, 158, 150, 154, 153, 163, 150, 158, 150, 158, 155, 163, 159, 157, 162, 160, 152, 164, 158, 153, 162, 166, 162, 165, 157, 174, 158, 171, 162, 155, 156, 159, 162, 152, 158, 164, 164, 162, 158, 156, 171, 164, 158])

#3) 

#Il s'agit ici d'une variable continue car les valeurs mesurées peuvent prendre n’importe quelle valeur dans un intervalle donné. 

#4)

BonasaUmbellus = longueurs

# 5)

lmin = np.min(BonasaUmbellus)           #Valeur min
lamx = np.max(BonasaUmbellus)           #Valeur max
etendue =  np.ptp(BonasaUmbellus)       #Etendue
moyenne = np.mean(BonasaUmbellus)       #Moyenne
mediane = np.median(BonasaUmbellus)     #Médiane (2e quartile)
q1 = np.percentile(BonasaUmbellus, 25)  #1er quartile
q3 = np.percentile(BonasaUmbellus, 75)  #3e quartile

#6)   

var4 = np.var(BonasaUmbellus)           #Variance
ect4  = np.std(BonasaUmbellus)          #Ecart-type

#7)

plt.boxplot(BonasaUmbellus)
plt.title('4 : Boite de dispersion')
plt.ylabel('Longueur rectrice')
plt.show()

#8)

plt.hist(BonasaUmbellus, bins = 10 , edgecolor = 'black')
plt.title('4 : Histogramme des lonngueurs')
plt.xlabel('Longueur rectrice')
plt.ylabel('Frequence')
plt.show()

#####            EXERCICE 5            #####

###            PARTIE 1              ###

# 1), 2), 3)


data5 = pd.read_csv("data.csv",sep=";",encoding = "unicode_escape", engine="python")

DATA5 = data5.values

S1t = np.loadtxt('data.csv')

#4) (voir graph 3)

valeurs, occurences = np.unique(S1t, return_counts = True)
plt.bar(valeurs, occurences, width = 0.1, align = 'center', edgecolor = 'black')
plt.title('5 : Diagramme batons S1')
plt.xlabel('Foids')
plt.ylabel('Freq')
plt.show()

#5)

moy5 = np.mean(S1t)          #Moyenne
ect5 = np.std(S1t)           #Ecart-type

#6)

plt.boxplot(S1t)
plt.title('5 : Boite de dispersion S1')
plt.ylabel('Poids')
plt.show()

#####        Exercice 6        ######


#1 
#La loi binomiale est une distribution de probabilité discrète utilisée pour modéliser le nombre de succès dans une série d'essais indépendants, où chaque essai a deux résultats possibles. La moyenne (μ) de cette distribution est calculée comme le produit du nombre d'essais (n) et de la probabilité de succès par essai (p), soit μ = n * p. L'écart-type (σ) est défini comme σ = √(n * p * (1 - p)), où √ représente la racine carrée. En résumé, la loi binomiale décrit le comportement probabiliste d'une série d'essais, avec sa moyenne et son écart-type déterminés par le nombre d'essais et la probabilité de succès.#

#2
# X suit une loi binomiale puisque son nombre d’essais (indépendants) est fixe : n=500 et X suit une loi de Bernoulli donc l’expérience aléatoire n’admet que deux issues : succès ou échec de probabilités respectives p=0,031175 et q=1-p. 

#3 
#La moyenne et l’écart type d’une loi binomiale se calculent de la manière suivante : 

n = 500
p = 0.031175

m = n*p 
sigma = sqrt( n * p (1-p) )


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

##### EXERCICE 7:   ######

# Paramètres de la distribution normale
mu = 360
sigma = np.sqrt(36)

# 1. Tracer la courbe de densité de probabilité (voir graph 4)

x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)
pdf = norm.pdf(x, mu, sigma)
plt.plot(x, pdf, label='Densité de probabilité')
plt.title('Courbe de densité de probabilité de Y')
plt.xlabel('Nombre d\'opérations réussies (Y)')
plt.ylabel('Densité de probabilité')
plt.legend()
plt.show()

# 2. Calculer la probabilité que la clinique réussisse au moins 345 opérations
prob_success_at_least_345 = 1 - norm.cdf(345, mu, sigma)
print(f"Probabilité que la clinique réussisse au moins 345 opérations : {prob_success_at_least_345:.4f}")

# 3. Calculer la probabilité que la clinique rate plus de 28 opérations
prob_failure_more_than_28 = norm.cdf(28, mu, sigma)
print(f"Probabilité que la clinique rate plus de 28 opérations : {prob_failure_more_than_28:.4f}")

# 4. Trouver le nombre d'opérations avec seulement 1% de chances d'être dépassé
target_probability = 0.01
critical_value = norm.ppf(target_probability, mu, sigma)
print(f"Nombre d'opérations avec seulement 1% de chances d'être dépassé : {critical_value:.2f}")


#####             EXERCICE 8              #####

# 1
# Données ordonnées
donnees = [54.8, 55.4, 57.7, 59.6, 60.1, 61.2, 62.0, 63.1, 63.5, 64.2, 65.2, 65.4, 65.9, 66.0, 67.6, 68.1, 69.5, 70.6, 71.5, 73.4, 75.0, 75.2]

# Calcul de la moyenne
moyenne = sum(donnees) / len(donnees)

# Calcul de la variance
variance = sum((x - moyenne) ** 2 for x in donnees) / (len(donnees) - 1)

# Calcul de l'écart-type
ecart_type = math.sqrt(variance)

print("Moyenne :", moyenne)
print("Écart-type :", ecart_type)


#2 (voir graph 5)

# Paramètres de l'histogramme
nombre_de_bins = 10  # Vous pouvez ajuster ce nombre en fonction de votre préférence

# Création de l'histogramme
plt.hist(donnees, bins=nombre_de_bins, edgecolor='black', alpha=0.7)

# Ajout de titres et d'étiquettes
plt.title('8 : Histogramme des niveaux de bruit')
plt.xlabel('Niveau de bruit (décibels)')
plt.ylabel('Fréquence')

# Affichage de l'histogramme
plt.show()


#4a
# Calcul de la moyenne
moyenne_estimee = np.mean(donnees)

# Calcul de l'écart-type
ecart_type_estime = np.std(donnees, ddof=1)  # ddof=1 pour utiliser la formule de l'écart-type d'un échantillon

print("Estimation de la moyenne :", moyenne_estimee)
print("Estimation de l'écart-type :", ecart_type_estime)


#4b
# Nombre de degrés de liberté
nu = 21  # Pour n-1, où n est la taille de l'échantillon (22 dans votre exemple)

# Générer des valeurs pour la distribution de Student
x = np.linspace(-3, 3, 1000)
pdf = t.pdf(x, df=nu)

# Tracer la densité de probabilité
plt.plot(x, pdf, label=f'Distribution de Student (df={nu})')
plt.title('8 : Distribution de Student')
plt.xlabel('Valeurs de t')
plt.ylabel('Densité de probabilité')
plt.legend()
plt.show()


#4c,  4d
# Taille de l'échantillon
n = len(donnees)

# Degrés de liberté pour la distribution de Student
df = n - 1

# Niveau de confiance
confiance = 0.95

# Calcul de la moyenne et de l'écart-type de l'échantillon
moyenne = np.mean(donnees)
ecart_type = np.std(donnees, ddof=1)

# Calcul de l'intervalle de confiance
intervalle_confiance = t.interval(confiance, df, loc=moyenne, scale=ecart_type / np.sqrt(n))

# Générer des valeurs pour la distribution normale
x_norm = np.linspace(min(donnees) - 5, max(donnees) + 5, 1000)
pdf_norm = norm.pdf(x_norm, loc=moyenne, scale=ecart_type)

# Tracer la densité de probabilité de la distribution normale
plt.plot(x_norm, pdf_norm, label='Densité de probabilité normale')

# Tracer l'histogramme des données
plt.hist(donnees, bins=10, density=True, alpha=0.7, label='Histogramme des données', edgecolor = 'black')

# Tracer l'intervalle de confiance
plt.axvline(x=intervalle_confiance[0], color='red', linestyle='--', label='Intervalle de confiance')
plt.axvline(x=intervalle_confiance[1], color='red', linestyle='--')

# Ajout de titres et de légendes
plt.title('8 : Distribution des données et Intervalle de confiance')
plt.xlabel('Valeurs')
plt.ylabel('Densité de probabilité')
plt.legend()

# Affichage du graphique
plt.show()


#4e
# Paramètres estimés de la distribution normale
moyenne = np.mean(donnees)
ecart_type = np.std(donnees, ddof=1)

# Valeur de seuil (70 dB)
seuil = 70

# Estimation de la probabilité que le niveau de bruit dépasse le seuil
probabilite_depassement = 1 - norm.cdf(seuil, loc=moyenne, scale=ecart_type)

print(f"Probabilité que le niveau de bruit dépasse {seuil} dB : {probabilite_depassement:.4f}")


#4f
# Bornes inférieure et supérieure
borne_inf = 60
borne_sup = 75

# Estimation de la probabilité que le niveau de bruit soit entre les bornes
probabilite_interval = norm.cdf(borne_sup, loc=moyenne, scale=ecart_type) - norm.cdf(borne_inf, loc=moyenne, scale=ecart_type)

print(f"Probabilité que le niveau de bruit soit entre {borne_inf} dB et {borne_sup} dB : {probabilite_interval:.4f}")


#4g
# Probabilité cible
probabilite_cible = 0.95

# Calcul de t1 (quantile inverse)
t1 = norm.ppf(probabilite_cible, loc=moyenne, scale=ecart_type)

print(f"t1 tel que P(X < t1) = {probabilite_cible}: {t1:.4f}")


#4h
# Probabilité cible
probabilite_cible = 0.25

# Calcul de t2 (quantile inverse)
t2 = norm.ppf(1 - probabilite_cible, loc=moyenne, scale=ecart_type)

print(f"t2 tel que P(X ≥ t2) = {probabilite_cible}: {t2:.4f}")

######        Exercice 9:     ######
#1)
#Données (voir graph6)
categories = ['< 55', '55-57', '57-59', '59-61', '61-63', '> 63']
nombre_oeufs = [12, 12, 15, 18, 20, 23]

#Histogramme
plt.bar(categories, nombre_oeufs, color='blue', edgecolor = 'black')
plt.title("8 : Distribution du poids des œufs")
plt.xlabel("Poids en grammes")
plt.ylabel("Nombre d'œufs")
plt.show()

#2)
#Moyenne et Ecart-Type
poids = np.array([52, 56, 58, 60, 62, 65])  # Valeurs centrales des intervalles
moyenne = np.average(poids, weights=nombre_oeufs)
ecart_type = np.sqrt(np.average((poids - moyenne)**2, weights=nombre_oeufs))

print("Moyenne (me):", moyenne)
print("Écart-type (σe):", ecart_type)



######      Exercice 10:       ######
#1a)  
televisions = pd.read_csv('televisions.dat', delimiter='\t')
#1b)
print(televisions.head()) #Permet d'afficher les premières ligne du fichier dat
print(televisions.info()) #Affiche des informations sur le type de données et les valeurs manquantes
#2)
Resume_stats = televisions.describe()
print(Resume_stats)
#3a)

#Représentation graphique pour la variable tv
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sb.scatterplot(x='teleratio', y='espvie', data=televisions)
plt.title('10 : Nuage de points entre tv et espvie')

#Représentation graphique pour la variable phys

plt.subplot(1, 2, 2)
sb.scatterplot(x='physratio', y='espvie', data=televisions)
plt.title('10 : Nuage de points entre phys et espvie')

plt.show()
#3b)

plt.figure(figsize=(12, 6)) #Pour détecter des données atypiques pour les variables tv et phys

# Boxplot pour la variable tv
plt.subplot(121)
sb.boxplot(x=televisions['teleratio'])
plt.title('10 : Boxplot pour le nombre de personnes par télévision')

# Boxplot pour la variable phys
plt.subplot(122)
sb.boxplot(x=televisions['physratio'])
plt.title('10 : Boxplot pour le nombre de personnes par physicien')

plt.show()

#4)

#Histogramme pour l'espérance de vie
plt.figure(figsize=(10, 6))
sb.histplot(televisions['espvie'], kde=True, bins=20, color='purple')
plt.title("10 : Distribution de l'espérance de vie à la naissance")
plt.xlabel("Espérance de vie à la naissance")
plt.ylabel("Fréquence")
plt.show()

#Boîte à moustaches pour l'espérance de vie des hommes et des femmes
plt.figure(figsize=(12, 8))
sb.boxplot(x='espvie', y='pays', data=televisions, orient='h', palette='Set2')
plt.title("10 : Boîte à moustaches de l'espérance de vie par pays")
plt.xlabel("Espérance de vie à la naissance")
plt.ylabel("Pays")
plt.show()

#Boîte à moustaches pour l'espérance de vie des hommes et des femmes
plt.figure(figsize=(10, 6))
sb.boxplot(x='espvieH', y='pays', data=televisions, orient='h', palette='Set2')
plt.title("10 : Boîte à moustaches de l'espérance de vie des hommes par pays")
plt.xlabel("Espérance de vie des hommes à la naissance")
plt.ylabel("Pays")
plt.show()

plt.figure(figsize=(10, 6))
sb.boxplot(x='espvieF', y='pays', data=televisions, orient='h', palette='Set2')
plt.title("10 : Boîte à moustaches de l'espérance de vie des femmes par pays")
plt.xlabel("Espérance de vie des femmes à la naissance")
plt.ylabel("Pays")
plt.show()

#5)

#Nuage de points entre l'espérance de vie et le nombre de personnes par télévision
plt.figure(figsize=(10, 6))
sb.scatterplot(x='teleratio', y='espvie', data=televisions, color='green')
plt.title("10 : Nuage de points entre l'espérance de vie et le nombre de personnes par télévision")
plt.xlabel("Nombre de personnes par télévision")
plt.ylabel("Espérance de vie à la naissance")
plt.show()

#Nuage de points sans observations atypiques
plt.figure(figsize=(10, 6))
sb.scatterplot(x='teleratio', y='espvie', data=televisions, color='blue')
plt.title("10 : Nuage de points sans observations atypiques")
plt.xlabel("Nombre de personnes par télévision")
plt.ylabel("Espérance de vie à la naissance")
plt.ylim([0, 100])  # Ajuster la limite y pour exclure les valeurs aberrantes
plt.show()

#Nuage de points entre l'espérance de vie et log(nombre de personnes par télévision)

televisions['log(teleratio)'] = np.log(televisions['teleratio'])

plt.figure(figsize=(10, 6))
sb.scatterplot(x='log(teleratio)', y='espvie', data=televisions, color='red')
plt.title("10 : Nuage de points entre l'espérance de vie et log(nombre de personnes par télévision)")
plt.xlabel("Log(Nombre de personnes par télévision)")
plt.ylabel("Espérance de vie à la naissance")
plt.show()

#6)

#Nuage de points entre l'espérance de vie et le nombre de personnes par physicien

plt.figure(figsize=(8, 6))
sb.scatterplot(x='physratio', y='espvie', data=televisions, color='orange')
plt.title("10 : Nuage de points entre l'espérance de vie et le nombre de personnes par physicien")
plt.xlabel("Nombre de personnes par physicien")
plt.ylabel("Espérance de vie à la naissance")
plt.show()
