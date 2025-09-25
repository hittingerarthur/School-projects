import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.integrate import solve_ivp
from math import *
                                 
def MSimpson (f, a, b, N):
    h = (b-a)/N
    x = np.linspace(a,b-h,N)
    S1 = sum (f(x[1:]))
    S2 = sum (f(x+h/2))
    A = f(a)+f(b)+2*S1+4*S2
    return h*A/6
 
def I(x):
    return (x**(3/2))*np.exp((-1)*(x)/2)

def table(f,a,b,N):
    X = np.linspace(a,b,N+1)
    I = []
    for b in X:
        I.append(MSimpson(f,a,b,N)*(1/(3*np.sqrt(2*np.pi))))

    tableau = []
    for i in range(len(I)):
        tableau.append([X[i],I[i]])

    return tableau, I

print("Table des valeurs:", table(I,0,20,200)[0])

R_calcule = (1/(3*sqrt(2*pi)))*MSimpson(I,0,20,200)
print("I vaut :", R_calcule )

R_theorique = (1/(3*sqrt(2*pi)))*integrate.quad(I, 0, 20)[0]
print('Solution de scipy :', R_theorique)

print('Erreur :', abs(R_theorique-R_calcule))

x = np.linspace(0,20,201)
y = table(I,0,20,200)[1]

plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('F(x)')
plt.title('Graphique de la fonction de la répartition de la loi du chi-carré')
plt.show()