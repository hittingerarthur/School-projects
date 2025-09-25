import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#Exercice 5

#Partie 1
#1 et 2
data_raw=pd.read_csv("data.csv", sep=';', encoding='latin1')
data=data_raw.iloc[:,0]
print("data :", '\n', data)

#4
plt.hist(data)

#5
m=sum(data)/len(data)
print('\n', "5)")
print('\n', "moyenne = ", m)
V_p=(sum(data**2)/len(data))-m**2
s_p=V_p**(1/2)
print('\n', "écart-type = ", s_p)

#6
plt.boxplot(data,vert=False)
plt.xlabel('Poids (en kg)')
plt.ylabel('Distrib') 
plt.show()

#Partie 2
print('\n', "Partie 2:")
#1
Poids1=data.head(15)
m1=sum(Poids1)/len(Poids1)
print('\n', "1)")
print('\n', "moyenne m1 = ",m1)

#2
Poids2=data.iloc[15:30]
m2=sum(Poids2)/len(Poids2)
print('\n', "2)")
print('\n', "moyenne m2 = ",m2)

#3
mtot=(m1+m2)/2
print('\n', "3)")
print('\n', "moyenne m totale = ",mtot)