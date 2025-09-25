import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#Exercice 4

#4
BonasaUmbellus = np.array([153, 165, 160, 150, 159, 151, 163, 160, 158, 150, 154, 153, 163, 150, 158, 150, 158, 155, 163, 159,
                   157, 162, 160, 152, 164, 158, 153, 162, 166, 162, 165, 157, 174, 158, 171, 162, 155, 156, 159, 162,
                   152, 158, 164, 164, 162, 158, 156, 171, 164, 158])

#5
mini=np.min(BonasaUmbellus)
maxi=np.max(BonasaUmbellus)
etendue=np.ptp(BonasaUmbellus)
m=np.mean(BonasaUmbellus)
median=np.median(BonasaUmbellus)
q1=np.percentile(BonasaUmbellus,25)
q3=np.percentile(BonasaUmbellus,75)
ecart_interquartile=q3-q1

#6
V=np.var(BonasaUmbellus)
s=np.std(BonasaUmbellus)

#7
plt.boxplot(BonasaUmbellus)
#plt.title('Boîte de dispersion de la longueur de la rectrice centrale')
plt.show()

#8
plt.hist(BonasaUmbellus,bins=10,edgecolor='black')
#plt.title('Histogramme de la longueur de la rectrice centrale')
plt.xlabel('longueur')
plt.ylabel('Fréquence')
plt.show()

print('\n', "5)")
print('\n', "Minimum = ", mini)
print('\n', "Maximum = ", maxi)
print('\n', "Etendue = ", etendue)
print('\n', "Moyenne = ", m)
print('\n', "Médiane = ", median)
print('\n', "Q1 = ", q1)
print('\n', "Q3 = ", q3)
print('\n', "Ecart interquartile = ", ecart_interquartile)
print('\n', "6)")
print('\n', "Variance = ", V)
print('\n', "Ecart-type = ", s)