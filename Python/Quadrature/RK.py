import numpy as np
import matplotlib.pyplot as plt
def f(t, y, yp):
    return -0.25 * yp - np.sin(y)
def RK(f, a, b, y0, yp0, N):
    h = (b - a) / N
    t_values = np.linspace(a, b, N + 1)
    y_values = np.zeros(N + 1)
    yp_values = np.zeros(N + 1)
    y_values[0] = y0
    yp_values[0] = yp0

    for i in range(N):
        t = t_values[i]
        y = y_values[i]
        yp = yp_values[i]

        k1 = h * yp
        l1 = h * f(t, y, yp)
        k2 = h * (yp + 0.5 * l1)
        l2 = h * f(t + 0.5 * h, y + 0.5 * k1, yp + 0.5 * l1)
        k3 = h * (yp + 0.5 * l2)
        l3 = h * f(t + 0.5 * h, y + 0.5 * k2, yp + 0.5 * l2)
        k4 = h * (yp + l3)
        l4 = h * f(t + h, y + k3, yp + l3)

        y_values[i + 1] = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6
        yp_values[i + 1] = yp + (l1 + 2 * l2 + 2 * l3 + l4) / 6

    return t_values, y_values


# Conditions initiales
a = 0
b = 10
y0 = 2
yp0 = 0
N = 1000

# Résolution avec RK4
t_values, y_values = RK(f, a, b, y0, yp0, N)

# Représentation graphique
plt.plot(t_values, y_values)
plt.xlabel('t')
plt.ylabel('y(t)')
plt.title('Solution de l\'équation différentielle avec RK (N=1000)')
plt.grid(True)
plt.show()
