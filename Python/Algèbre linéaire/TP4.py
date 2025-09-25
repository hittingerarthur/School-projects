import numpy as np
import tp4_donnees as tp
import matplotlib.pyplot as plt
import math as m
import random as rd
# ---------------------------------------
# Exercice 1
# ---------------------------------------

def MoindreCarre(A,b):
    '''
    Fonction permettant de resoudre Ax = b par la methode des moindres carre
    '''
    x = np.dot(np.dot(np.linalg.inv(np.dot(np.transpose(A),A)),np.transpose(A)),b)
    return x

def Theta(p,q,A):
    if A[p,p] == 0 and A[q,p] == 0:
        theta = rd.uniform(0,2*np.pi)
    elif A[p,p] == 0 and A[q,p] != 0:
        theta = (np.pi)/2
    else:
        theta = m.atan(-(A[q,p]/A[p,p]))
    return theta

def defG(p,q,theta,A):
    G = np.eye((len(A)))
    G[p,p] = m.cos(theta)
    G[q,p] = m.sin(theta)
    G[p,q] = -m.sin(theta)
    G[q,q] = m.cos(theta)
    return G

def Givens(A): 
    n = A.shape[0]
    r = A.shape[1]
    Q = np.eye(n) 
    
    for i in range(0,n): 
        for j in range(0,i): 
            if j< r :
                theta = Theta(j, i, A)
                Q = np.dot(defG(j,i,theta,A),Q)
                A = np.dot(defG(j,i,theta,A),A )

    return Q.T , A

def PMCGivens(A,b):
    '''Rend la solution du problème aux moindres carrés décrit
    par le système Ax = b en utilisant la décomposition QR de A 
    fournie par l’algorithme de Givens.
    '''
    n = A.shape[0]
    print(n)
    r = A.shape[1]
    print(r)
    Q = Givens(A)[0]
    R = Givens(A)[1]
    for i in range(0,n):
        for j in range(0,r):
            if i> j :
                R[i,j]=0
    print("\nR = ",R)
    Qtb = np.dot(np.transpose(Q),b)
    print("\nQtb = ",Qtb)
    while n > r:
        R = np.delete(R, (n-1), axis=0)
        Qtb = np.delete(Qtb, (n-1), axis = 0)
        n = R.shape[0]
    print("\nR2 = ",R)
    print("\nQtb2 = ",Qtb)
    x = np.zeros((n,1))
    
    for j in range(n-1,-1,-1):
        xr = np.dot(R[j,(j+1):n],x[(j+1):n])
        x[j] = (Qtb[j]-xr)/R[j,j]
    
    return x

def Defb(x,y):
    '''
    Fonction pour determiner b
    '''
    n = len(x)
    b = np.zeros((n,1))
    for i in range(n):
        b[i] = (x[i]**2+y[i]**2)
    return b


def DefA(x,y):
    '''
    Fonction pour determiner A
    '''
    n = len(x)
    A = np.zeros((n,3))
    for i in range(n):
        A[i,0] = 2*x[i]
        A[i,1] = 2*y[i]
        A[i,2] = 1
    return A

def Cercle(x):
    x0 = x[0][0]
    y0 = x[1][0]
    r = np.sqrt(x[2][0]+x0**2+y0**2)
    print('\nLes coordonnées du cercle sont M({},{}) de rayon {}'.format(x0,y0,r))
    return x0,y0,r


def GraphMat(x0,y0,r):

    plt.figure(figsize=(10,10))

    x,y = tp.donnees_partie2()
    theta = np.linspace(0, 2*np.pi, 100)

    x1 = r*np.cos(theta) + x0
    y1 = r*np.sin(theta) + y0

    plt.scatter(x,y, color='blue')
    plt.plot(x1, y1, 'red', label='Les coordonnées du cercle sont M({},{}) de rayon {}'.format(x0,y0,r))

    plt.title('Nuage de points de x et y')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.xlim(-10,10)
    plt.ylim(-10,10)
    
    plt.show()

# ---------------------------------------
# Exercice 2
# ---------------------------------------

def DefA2(x):
    n = len(x)
    A = np.zeros((n,6))
    for i in range(n):
        for k in range(0,6):
            A[i,k] = x[i]**k
    return A

def Defb2(x):
    n = len(x)
    b = np.zeros((n,1))  
    for i in range(n):
        b[i] = np.log(x[i])
    return b

def Resol2():
    x = np.arange(1,2,0.01)
    A = DefA2(x)
    print("\nA = ",A)
    b = Defb2(x)
    print("\nb = ",b)
    sol = MoindreCarre(A,b)
    sol2 = PMCGivens(A, b)
    e = np.linalg.norm(sol-sol2)
    print("\nSolution équation normale = ",sol)
    print("\nSolution par PMCGivens = ",sol2)
    print("\nL'erreur entre la résolution par les équations normales et la résolution PMCGivens est de : ",e)

def AproxLn(A,x):
    y = A[0][0]*(x**0) + A[1][0]*(x**1) + A[2][0]*(x**2) + A[3][0]*(x**3) + A[4][0]*(x**4) + A[5][0]*(x**5)
    return y
        
def GraphMat2():

    plt.figure(figsize=(10,10))

    x = np.arange(0.0001,10,0.0001)
    A = DefA2(x)
    b = Defb2(x)
    sol = MoindreCarre(A,b)
    y1 = AproxLn(sol,x)
    y2 = np.log(x)

    plt.plot(x, y1, 'red', label='Approximation de ln')
    plt.plot(x, y2, 'blue', label='ln')
    plt.title('Nuage de points de x et y')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.grid()
    plt.xlim(-1,30)
    plt.ylim(-5,5)
    
    plt.show()


def main(): 

    #Exercice 1
    x,y = tp.donnees_partie2()

    b = Defb(x,y)
    print("\nb = ",b)

    A = DefA(x,y)
    print("\nA = ",A)

    x = MoindreCarre(A,b)
    x2 = PMCGivens(A, b)
    e = np.linalg.norm(x-x2)
    print("\nX_MC = ",x)
    print("\nX_Givens = ",x2)
    print("\nL'erreur entre la résolution par les équations normales et la résolution PMCGivens est de : ",e)
    
    x0,y0,r = Cercle(x)

    GraphMat(x0,y0,r)
    Resol2()
    GraphMat2()
if __name__ == '__main__':
    main()