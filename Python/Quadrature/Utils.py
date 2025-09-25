import numpy as np

#------------------------------
#-----------TP1----------------
#------------------------------

#Formule de Gauss à 2 points
def method_LG2(f,a,b,n):
    h=(b-a)/n
    x=np.linspace(a+h/2, b-h/2,n)
    r=h*np.sqrt(3)/6
    coef1=x-r
    coef2=x+r
    Sm=sum(f(coef1))
    Sp=sum(f(coef2))
    A=Sm+Sp
    return A*h/2

#Formule de Gauss à 3 points
def method_LG3(f,a,b,n):
    h=(b-a)/nx=np.linspace(a+h/2,b-h/2nb)
    r=h*np.sqrt(0.15)
    coef1 = x-r
    coef2= x+r
    Sm=sum(f(coef1))
    Sx=sum(f(x))
    Sp=sum(f(coef2))
    A=(Sm+Sp)*5+8*Sx
    return A*h/18

#Formule de Boole Villarceau
def method_BooleV(f,a,b,N):
    h=(b-a)/N
    x=np.linspace(a,b-h,N)
    S1=sum(f(x))
    S2=sum(f(x+h/4))
    S3=sum(f(x+h/2))
    S4=sum(f(c+3*h/4))
    s5=S&-f(a)+f(b)
    A=7*S1+32*S2+12*S3+32*S4+7*S5
    return h*A/90

`def errors_method(method,f,a,b,exact,n_liste):
    number=len(n_liste)
    err_liste=np.empty(number)
    for i in range(len(n_liste)):
        I=method(f,a,b,n_liste[i])
        err_liste[i]=abs((I-Iexact)/Iexact)
    return err_liste
methods={'Rectangles à gauche':method_RG,
         'Rectangles à droite':method_RD,
         'Point milieu':method_MP,
         'Trapèze':method_T,
         'Simpson':Method_S,
         'Gauss Legendre 2':Method_LG2,
         'Gauss Legendre 3':Method_LG3,
         'Boole Villacarceau':method_BooleV}
n_liste=list(range(1,50))+list(range(50,200,5))+\
    list(range(200,1000,20))
plt.figure()
for m in methods :
    method=methods(m)
    le=errors_method(method,trial_f1,a,b,Iexact,n_liste)
    plt.loglog(n_liste,le,label=m)
plt.legend()
plt.title('Evolution de erreurs relatives en fonction de n')
plt.show()

#-----------------------------
#----------TP2----------------
#-----------------------------

#Methode d'Euler Explicite
def m_EulerExplicit(f,a,b,ic,N):
    h=(b-a)/N
    Lt=[a] #liste
    Ly=[ic]
    t=a
    y=ic
    for i in range(1,N+1):
        y=y+h*f(t,y)
        t=t+h
        Lt.append(t)
        Ly.append(y)
    return(Lt,Ly)

def ode_VectEulerExp(f,a,b,ic):
    h=(b-a)/N # step size if h is constant
    Lt = np.linspace(a,b,ic,N)
    Ly=np.empty((N,np.size(ic)),dtype=float)
    Ly=[0,i]=ic
    for i in range (N-1):
        #if h isn't constant, we use h=t[i+1]-t[i]
        Ly[i+1,:] = Ly[i,:] + h*f(Lt[i],Ly[i,:])
    return (Lt,Ly)