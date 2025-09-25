import numpy as np
import matplotlib.pyplot as plt
import linalg as lng
def solEE(N,tau):
    h = 1/(N+1)
    T = np.arange(0,5+tau,tau)
    X = np.arange(h,1,h)     # attention on ajoutera les extrémités après (0 et 1)
    c = 0.1*tau/(h**2)
    Me =(1-2*c)*np.eye(N)
    for i in range(0, len(X)-1):
        Me[i, i+1] = c
    for j in range(1, len(X)):
        Me[j, j-1] = c
    U = np.array([np.sin(np.pi*X)])
    for n in range(len(T)-1):
        U = np.insert(U, n+1, np.dot(Me,U[n]), axis=0)
    # on ajoute les extrémités
    X = np.append(0, X)
    X = np.append(X, 1)
    U = np.insert(U, 0, np.zeros(len(T)), axis=1)
    U = np.insert(U, len(X)-1, np.zeros(len(T)), axis=1)
    return X, T, U

## Question 2

## Cas a : h = 0.05 => N=19 et tau= 0.1
Xa,Ta,Uae=solEE(19, 0.1)
for t in [0, 1, 2, 3, 4, 5]:
    plt.plot(Xa, Uae[t*10], "*", label="u(x, t=%s)" %t)
    plt.xlabel("x")
    plt.ylabel("u(x)")
    plt.legend()
plt.show()
#ici c=nu*tau/h^2 = 4>1/2 INSTABLE

## Cas b : h = 0.05 et tau = 0.01
## N = 1/H -1
Xb,Tb,Ube=solEE(19, 0.01)
for t in [0, 1, 2, 3, 4, 5]:
    plt.plot(Xb, Ube[t*100], "*", label="u(x, t=%s)" %t)
    plt.xlabel("x")
    plt.ylabel("u(x)")
    plt.legend()
plt.show()
#ici c= 0.4<1/2 STABLE

## Cas c : h = 0.02 => N=49 et tau = 0.01
Xc,Tc,Uce=solEE(49, 0.01)
for t in [0, 1, 2, 3, 4, 5]:
    plt.plot(Xc, Uce[t*100], "*", label="u(x, t=%s)" %t)
    plt.xlabel("x")
    plt.ylabel("u(x)")
    plt.legend()
plt.show()
#ici c=nu*tau/h^2 = 2.5>1/2 INSTABLE

## Question 3

def solEI(N,tau):
    h = 1/(N+1)
    T = np.arange(0,5+tau,tau)
    X = np.arange(h,1,h)     # attention on ajoutera les extrémités après (0 et 1)
    c = 0.1*tau/(h**2)
    Mi =(1+2*c)*np.eye(N)
    for i in range(0, len(X)-1):
        Mi[i, i+1] = -c
    for j in range(1, len(X)):
        Mi[j, j-1] = -c
    U = np.array([np.sin(np.pi*X)])
    for n in range(len(T)-1):
        U = np.insert(U, n+1, np.dot(lng.inv(Mi),U[n]), axis=0)
    # on ajoute les extremités
    X = np.append(0,X)
    X = np.append(X, 1)
    U = np.insert(U, 0, np.zeros(len(T)), axis=1)
    U = np.insert(U, len(X)-1, np.zeros(len(T)), axis=1)
    return X, T, U

    ## Cas b : h = 0.05 et tau = 0.01
    ## N = 1/H -1


Xb, Tb, Ubi = solEI(19, 0.01)
for t in [0, 1, 2, 3, 4, 5]:
    plt.plot(Xb, Ubi[t * 100], "*", label="u(x, t=%s)" % t)
    plt.xlabel("x")
    plt.ylabel("u(x)")
    plt.legend()
plt.show()
# ici c= 0.4<1/2 STABLE



def solCN(N,tau):
    h = 1/(N+1)
    T = np.arange(0,5+tau,tau)
    X = np.arange(h,1,h)     # attention on ajoutera les extrémités après (0 et 1)
    c = 0.1*tau/(h**2)
    Mi =(1+c)*np.eye(N)
    for i in range(0, len(X)-1):
        Mi[i, i+1] = -c/2
    for j in range(1, len(X)):
        Mi[j, j-1] = -c/2
    U = np.array([np.sin(np.pi*X)])
    for n in range(len(T)-1):
        U = np.insert(U, n+1, np.dot(lng.inv(Mi),U[n]), axis=0)
    # on ajoute les extremités
    X = np.append(0,X)
    X = np.append(X, 1)
    U = np.insert(U, 0, np.zeros(len(T)), axis=1)
    U = np.insert(U, len(X)-1, np.zeros(len(T)), axis=1)
    return X, T, U