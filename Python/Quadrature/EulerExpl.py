import numpy as np
import matplotlib.pyplot as plt


def f(t, y, yp):
    return -1 / 4 * yp - np.sin(y)


def solve_euler_explicit(f, y0, yp0, t0, tf, h):
    num_steps = int((tf - t0) / h)
    t_values = np.linspace(t0, tf, num_steps + 1)
    y_values = np.zeros(num_steps + 1)
    yp_values = np.zeros(num_steps + 1)

    y_values[0] = y0
    yp_values[0] = yp0

    for i in range(num_steps):
        y_next = y_values[i] + h * yp_values[i]
        yp_next = yp_values[i] + h * f(t_values[i], y_values[i], yp_values[i])
        y_values[i + 1] = y_next
        yp_values[i + 1] = yp_next

    return t_values, y_values


# Conditions initiales
y0 = 2
yp0 = 0
t0 = 0
tf = 10
h = 0.01  # Taille du pas

# Résolution de l'équation différentielle avec la méthode d'Euler explicite
t_values, y_values = solve_euler_explicit(f, y0, yp0, t0, tf, h)

# Tracé de la solution
plt.plot(t_values, y_values, label='Solution')
plt.xlabel('t')
plt.ylabel('y(t)')
plt.title('Solution de l\'équation différentielle')
plt.legend()
plt.grid(True)
plt.show()
