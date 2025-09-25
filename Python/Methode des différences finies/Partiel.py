import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return x[0] ** 2 - x[0] * x[1] + x[1] ** 2 - x[0] - x[1]


A = np.array([[2, -1],
              [-1, 2]])

b = np.array(([1, 1]))
c = 0
val = np.linalg.eigvals(A)
print(f'les valeurs propres de la matrice sont : {val}')

x_star = np.linalg.solve(A, b)
f_xstar = 0.5 * x_star.T @ A @ x_star - b.T @ x_star + c
print(f'le point critique de la fonction est x* : {x_star} et f(x*) = {f_xstar}')

u, vecteur_propre = np.linalg.eig(A)
print(vecteur_propre)


def plot_fonction(f, x_range=(-20, 20), y_range=(-20, 20), title="Représentation 2D des fonctions", xlabel="x1",
                  ylabel="x2"):
    x_min, x_max = x_range
    y_min, y_max = y_range
    # Generate grid of x and y values
    x_values = np.linspace(x_min, x_max, 100)
    y_values = np.linspace(y_min, y_max, 100)
    X, Y = np.meshgrid(x_values, y_values)
    x = [X, Y]
    Z = f(x)
    # Plot
    plt.figure()
    plt.contour(X, Y, Z, cmap='viridis', levels=20)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.colorbar(label='z')
    plt.grid(True)
    plt.show()

plot_fonction(f)


