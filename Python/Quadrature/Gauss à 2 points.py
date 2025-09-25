import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

def integrand(t, x):
    return t**(x-1) * np.exp(-t)

def Gamma(x):
    result, error = quad(integrand, 0, np.inf, args=(x,))
    return result

def plot_Gamma():
    x_values = np.linspace(1, 2, 1000)
    y_values = [Gamma(x) for x in x_values]
    plt.plot(x_values, y_values)
    plt.xlabel('x')
    plt.ylabel('Gamma(x)')
    plt.title('Gamma function')
    plt.grid(True)
    plt.show()


a=1
b=2
n=100
#Formule de Gauss à 2 points
def method_LG2(Gamma,a,b,n):
    h=(b-a)/n
    x=np.linspace(a+h/2, b-h/2,n)
    r=h*np.sqrt(3)/6
    coef1=x-r
    coef2=x+r
    Sm=sum(Gamma(coef1))
    Sp=sum(Gamma(coef2))
    A=Sm+Sp
    return A*h/2

# Test et affichage des résultats
print(" Γ(1) =", "{:.5f}".format(Gamma(1)))
print(" Γ(3/2) =", "{:.5f}".format(Gamma(3/2)))
print(" Γ(2) =", "{:.5f}".format(Gamma(2)))
plot_Gamma()


print(" Minimum avec la méthode de Gauss  2 points = ",method_LG2() )

