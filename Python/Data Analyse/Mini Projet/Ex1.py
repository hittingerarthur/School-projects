import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

#Exercice 1

#1
data=pd.read_csv('dataMP.csv', sep=';' , encoding='latin1')
N=data.iloc[:,0]
X=data.iloc[:,1]
Y=data.iloc[:,2]
print('1)')
print(X)
print(Y)

#2
plt.scatter(X,Y)

#3
x=np.mean(X)
print('\n', '3)')
print('\n', "La moyenne de X est :", x)
y=np.mean(Y)
print('\n', "La moyenne de Y est :", y)

#4
cov_xy=np.mean((X-x)*(Y-y))
print('\n', '4)')
print('\n', "la covariance de X et Y est :",cov_xy)

#5
V_x=((1/len(X))*sum(X*X)-(x*x))
V_y=((1/len(Y))*sum(Y*Y)-(y*y))
s_x=V_x**(1/2)
s_y=V_y**(1/2)
r=cov_xy/(s_x*s_y)
print('\n', '5)')
print('\n', "coef de corrélation :",r)
print('\n', "Forte corrélation entre les variables X et Y ")

#6a
a1,b1,_,_,_=stats.linregress(X,Y)


#6b
a=cov_xy/V_x
b=y-a*x
plt.plot(X,a*X+b,color='r')
print('\n', '6)')
print('\n', "On fait la différence de a et de b obtenus avec la fonction linregress et a et b obtenus avec la méthode de cours:")
print('\n')
print(a1-a)
print(b1-b)
print('\n')
print("Les différences sont (environ) égale à 0. Les coefficients sont bien les mêmes.")

#7
plt.scatter(x,y,color='black')
print('\n', '7)')
print('\n', 'On peut voir que le point G (en noir) appartient bien à la droite.')

#8 a et b
Vr1=((1/len(X))*sum((Y-a*X-b)**2))
Vr2=(1-r**2)*V_y
Ve1=(a**2)*V_x
Ve2=(r**2)*V_y
print('\n', '8a) et 8b)')
print('\n', "On calcule avec deux méthodes différentes la variance résiduelle:")
print('\n', "Méthode 1:", Vr1,'\n', "Méthode 2:", Vr2)
print('\n', "On calcule avec deux méthodes différentes la variance expliquée:")
print('\n', "Méthode 1:", Ve1,'\n', "Méthode 2:", Ve2)

#8c
V_y2=Ve1+Vr1
print('\n', '8c)')
print('\n', "Pour vérifier l'équation de la variance, on calcule la différence entre V_y et V_y2. V_y2 est calculée en faisant la somme de la variance résiduelle et expliquée:")
print('\n',"V_y-Vy2 = ", V_y-V_y2)
print('\n', "La différence est (environ) nulle. L'équation de la variance est donc vérifiée.")
