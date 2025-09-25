import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#Exercice 2
#1
print('\n', "1)")
print('\n', "On a V=V0*exp(-t/τ)=a*x+b. ")
print('\n', "On applique ln() ce qui nous permet d'obtenir :")
print('\n', "ln(V)=-t/τ + ln(V0)")
print('\n', "Par identification, y=ln(V), x=t, a=-1/τ et b = ln(V0)")

#2
t = np.array([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50])
V = np.array([5.098, 3.618, 2.581, 2.011, 1.486, 1.028, 0.845, 0.573, 0.429, 0.29, 0.2])
Xln=t

#3
Yln=np.log(V)

#4
a,b=np.polyfit(Xln,Yln,1)
droite=a*Xln+b
plt.scatter(Xln,Yln,label='données')
plt.plot(Xln,droite,color='red', label='Droite de régression')
plt.xlabel('t (ms)')
plt.ylabel('ln(V)')
plt.legend()
plt.show()

#5
V0=np.exp(b)
T=-1/a
print('\n', "5)")
print('\n', 'V0 = ', V0)
print('\n', 'T = ', T)

#6
t_donné=53
V_calculé=V0*np.exp(-t_donné/T)
print('\n', "6)")
print('\n', 'Pour t=53ms, on obtient V = ', V_calculé)