from math import cos, sin, atan, sqrt
from numpy import shape,eye,zeros,vdot,dot,array,transpose,delete,zeros
from numpy.linalg import norm, solve
from matplotlib import pyplot as plt
from numpy.random import randn
import TP4 
import tp4_donnees as tp
#DONNEES 
A1 = array([[3,10],[-4,2]])
A2 = array([[0,-1,1],[4,2,0],[3,4,0]])
A3 = array([[3,10],[-4,2],[1,1]])

A5 = array([[1,2],[0,-1],[1,1],[-2,0]])
A6 = array([[1,1],[1,-1],[2,1]])

b2 = array([[1],[-2],[2],[-3]])
b3 = array([[1],[2],[3]])

#	ALGORITHMES
#GIVENS 
#methode avec arctan
def matriceG (A,q,p) : 
	n,r = shape(A)
	G = eye(n)
	theta = atan(-(A[q,p]/A[p,p]))
	G[p,p] = cos(theta)
	G[q,p] = sin(theta)
	G[p,q] = -sin(theta)
	G[q,q] = cos(theta)
	return G

#sans arctan
def matriceG2 (A,q,p) : 
	n,r = shape(A)
	G = eye(n)
	c = A[p,p]/(sqrt(A[p,p]**2+A[q,p]**2))
	s = - A[q,p]/(sqrt(A[p,p]**2+A[q,p]**2))
	G[p,p] = c
	G[q,p] = s
	G[p,q] = - s
	G[q,q] = c
	return G

#construction de decompo QR
def matrice22(A):
	q = 2-1 #indice maths et python pas pareil en maths p = 1 et q =2
	p = 1-1
	G = matriceG(A,q,p) 
	GA = dot(G,A)
	#verification que bien nul 
	if abs(GA[q,p])<=10**(-10) :
		print ("youpi c'est nul",'\n')
	print("G",'\n',G,'\n')
	print("newA = GA",'\n',GA,'\n')


#dans cet algorithme on ne prend ps en compte le fait que seulement 2 lignes changent au max 
def decompositionQR(A):
	n,r = shape(A)
	newA = A
	Q = eye(n)
	for q in range (0,n) :
		for p in range (0,q) :
			if p < r : 
				G = matriceG2(newA,q,p)
				Q = dot(Q,transpose(G))
				newA = dot(G,newA)
	return Q,newA

Q,R = decompositionQR(A3)


#fonction donne dans TP2
def ResolTriSup(T,b):
    """ Resolution d'un systeme Tx=b
    avec T triangulaire superieure et b un vecteur.
    La solution x est rendue de meme format que b """
    frm=b.shape
    n,m=T.shape
    x=zeros(n)
    for i in range(n-1,-1,-1):
        S=T[i,i+1:]@x[i+1:]
        x[i]=(b[i]-S)/T[i,i]
    return x.reshape(frm)

#fonction donné dans TP de l'an dernier des gens en prépa intégrée à l'IPSA
def ResolutionSystTriSup(Tring):
    n = len(Tring)
    X = zeros(n)
    for j in range(1, n+1):
        X[n-j] = Tring[n-j][n] / Tring[n-j][n-j]
        for i in range(1, j):
            if Tring[n-j][n-j] != 0:
                X[n-j] = X[n-j] - ((Tring[n-j][n-i] / Tring[n-j][n-j]) * X[n-i])
            else:
                print("Pas de solution")
    return X

def ResolGivens(A,b):
	Q,R = decompositionQR(A)
	QT = transpose(Q)
	return ResolTriSup(R,dot(QT,b))	


#dans TP1
def Hilbert(n):
	H = zeros((n,n))
	for i in range (0,n):
		for j in range (0,n):
			H[i,j] = 1/((i+1)+(j+1)-1)
	return H

#dans TP2 
def DecompositionGS(A):
	n,m = shape(A)
	if n != m:
		raise Exception('Pas une matrice carree')
	Q = zeros((n,n))
	R = zeros((n,n)) 
	for j in range(0,n): #maths et python pas meme indice 
		for i in range(0,n):
			if i < j: 
				R[i,j] = vdot(A[:,j],Q[:,i])
		somme = zeros(n)
		for k in range(0,j):
			somme += R[k,j]*Q[:,k]
		w = A[:,j] - somme
		R[j,j] = norm(w,2)
		Q[:,j] = 1/R[j,j] * w #pour simplifier complexité on fait qu'une fois la division
	return Q,R

Q1,R1 = decompositionQR(Hilbert(8))
Q2,R2 = DecompositionGS(Hilbert(8))


def ResolGivens2(A,b):
	n,r = shape(A)
	newA = A
	for q in range (0,n) :
		for p in range (0,q) :
			if p < r : 
				G = matriceG2(newA,q,p)
				newA = dot(G,newA)
	R_tild = zeros((n, n+1))
	for i in range(n):
		for j in range(n):
			R_tild[i,j] = newA[i,j]
		R_tild[i,n] = b[i]
	return ResolutionSystTriSup(R_tild)

#print(ResolGivens2(A2,b3))

def ResolGS(A,b):
	n,m = shape(A)
	if n != m:
		raise Exception('Pas une matrice carree')
	Q,R = DecompositionGS(A)
	QT = transpose(Q)
	return ResolTriSup(R,dot(QT,b))

def erreur_comparaison():
    e1 = []
    e2 = []
    e3 = []
    e4 = []
    for n in range(10,50):
        A = randn(n,n) 
        b = randn(n)
        x1 = ResolGivens(A,b)
        x2 = ResolGivens2(A,b)
        x3 = ResolGS(A,b)
        x4 = solve(A,b)
        e1.append(norm(dot(A,x1)-b))
        e2.append(norm(dot(A,x2)-b))
        e3.append(norm(dot(A,x3)-b))
        e4.append(norm(dot(A,x4)-b))
    plt.semilogy(range(10,50),e1,label="ResolGivens")
    plt.semilogy(range(10,50),e2,label="ResolGivens2")
    plt.semilogy(range(10,50),e3,label="ResolGS")
    plt.semilogy(range(10,50),e4,label="solve")
    plt.grid()
    plt.title("erreur pour les différentes méthodes de résolution")
    plt.xlabel("n = taille matrice A")
    plt.ylabel("Erreur calculé")
    plt.legend()
    plt.show()

erreur_comparaison()
x,y = tp.donnees_partie2()
A12=TP4.DefA(x,y)
b12=TP4.Defb(x,y)

def PMCGivens(A,b):
	"""Fonction qui rend la solution du problème aux moindres carrés décrit par le système Ax = b"""
	Q,R = decompositionQR(A)
	q,p = shape(R)
	R1 = R
	l = []
	for n in range(0,q):
		k = 0
		for m in range(0,p):
			if R[n,m] <= 10**(-10):
				k += 1
		if k == p:
			l.append(n)
	c = dot(transpose(Q), b)
	c1 = c
	print(R)
	print(c)
	print()
	for i in range(1,len(l)+1):
		R1 = delete(R1,(l[0]),axis=0)
		c1 = delete(c1,(l[0]),axis=0)
		print(R1)
		print(c1)
		print()
	x = ResolTriSup(R1,c1)
	print(x)

PMCGivens(A12,b12)


