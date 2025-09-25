import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#Exercice 3

#valeur pour 1962 ? Ignorée

#1,2
N=np.array([1944,1945,1946,1947,1948,1949,1950,1951,1952,1953,1954,1955,1956,1957,1958,1959,1960,1961])
XPA=np.array([100,61,76,74,90,93,102,98,103,110,117,118,112,115,116,121,134,130])
XPI=np.array([10,50,84,99,113,122,128,143,145,145,159,172,188,204,213,220,242,254])

#3
plt.figure()
plt.scatter(XPA,XPI)
#plt.scatter(N,XPI)

#4
xpa=np.mean(XPA)
xpi=np.mean(XPI)
plt.scatter(xpa,xpi,color='black')

#5
cov_xpa_xpi=np.mean((XPA-xpa)*(XPI-xpi))
print('\n', "5)")
print('\n', "Covariance entre x et y = ", cov_xpa_xpi)

#6
V_xpa=((1/len(XPA))*sum(XPA*XPA)-(xpa*xpa))
V_xpi=((1/len(XPI))*sum(XPI*XPI)-(xpi*xpi))
s_xpa=V_xpa**(1/2)
s_xpi=V_xpi**(1/2)
r=cov_xpa_xpi/(s_xpa*s_xpi)
print('\n', "6)")
print('\n', 'Coef de corrélation = ',r)

#7
print('\n', '7)')
print('\n', "On constante une corrélation forte en XPA et XPI")

#8
a=cov_xpa_xpi/V_xpa
b=xpi-a*xpa
droite=a*XPA+b
plt.plot(XPA,droite)
d_regression=[abs(droite[i]-XPI[i]) for i in range(len(XPA))]
Vr=((1/len(XPA))*sum((XPI-a*XPA-b)**2))
Ve=(a**2)*V_xpa
print('\n', "8)")
print('\n', 'Distance à la droite : ', d_regression)
print('\n', 'Variance résiduelle = ', Vr,'\n', 'Variance expliquée = ', Ve)

#9
a2=cov_xpa_xpi/V_xpi
b2=xpa-a2*xpi
droite2=(XPA-b2)/a2
plt.plot(XPA,droite2,color='red')
plt.show()
d_regression2=[abs(droite2[i]-XPI[i])for i in range(len(XPA))]
Vr2=((1/len(XPA))*sum((XPI-a2*XPA-b2)**2))
print('\n', "9)")
print('\n', 'Variance résiduelle 2 = ',Vr2,'\n', 'Variance expliquée 2 = ',Ve)