import numpy as np
import matplotlib.pyplot as plt

# Définition des constantes
t0 = 0
tf = 5
h = 0.01
n = int((tf - t0) / h) + 1

# Initialisation des vecteurs
t = np.linspace(t0, tf, n)
y = np.zeros(n)
y[0] = 1
y1 = np.zeros(n)
y1[0] = 0

# Résolution numérique de l'équation différentielle
for i in range(1, n):
    y1[i] = y1[i-1] - t[i-1] * y[i-1] * h
    y[i] = y[i-1] + y1[i-1] * h

# Représentation graphique de la solution
plt.plot(t, y, label='y(t)')
plt.legend()
plt.xlabel('t')
plt.ylabel('y')
plt.title('Solution de y\'\'=-ty avec y(0)=1 et y\'(0)=0')
plt.show()
