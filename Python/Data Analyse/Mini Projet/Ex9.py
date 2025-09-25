import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

#Exercice 9

#1
categories = ['<55', '55-57', '57-59', '59-61', '61-63', '>63']
nombre_oeufs = [12, 12, 15, 18, 20, 23]

plt.bar(categories, nombre_oeufs, color='skyblue')
plt.xlabel('Poids des œufs (g)')
plt.ylabel('Nombre d\'œufs')
plt.title('Distribution du poids des œufs')
plt.show()

#3
s_e=3.97
#Calculé dans la question 2 (voir Word)
n=sum(nombre_oeufs)
print(n)
s=s_e*((n/(n-1))**(1/2))
print('\n', "3)")
print('\n',"s= ", s)
print('\n', "s et s_e sont très proches (3.99 et 3.97). Le vendeur a donc pris la bonne décision")