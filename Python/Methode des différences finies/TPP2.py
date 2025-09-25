import numpy as np
import matplotlib.pyplot as plt

# Paramètres
L = 1.0
T = 6.0
Nx_list = [int(L / 0.01), int(L / 0.02), int(L / 0.05)]
dt_list = [0.5, 0.05, 0.001]
c = 1 / 6
x_list = [np.linspace(0, L, Nx + 1) for Nx in Nx_list]
u0_list = [(np.sin(np.pi * x)) ** 4 for x in x_list]


def explicite_centre(u, dt, dx, c):
    unew = u.copy()
    for i in range(1, len(u) - 1):
        unew[i] = u[i] - (c * dt / (2 * dx)) * (u[i + 1] - u[i - 1])
    return unew


def implicite_centre(u, dt, dx, c):
    A = np.eye(len(u)) - (c * dt / (2 * dx)) * np.eye(len(u), k=1) + (c * dt / (2 * dx)) * np.eye(len(u), k=-1)
    return np.linalg.solve(A, u)


def explicite_decentre_amont(u, dt, dx, c):
    unew = u.copy()
    for i in range(1, len(u)):
        unew[i] = u[i] - (c * dt / dx) * (u[i] - u[i - 1])
    return unew


def lax_friedrichs(u, dt, dx, c):
    unew = u.copy()
    for i in range(1, len(u) - 1):
        unew[i] = 0.5 * (u[i + 1] + u[i - 1]) - (c * dt / (2 * dx)) * (u[i + 1] - u[i - 1])
    return unew


def lax_wendroff(u, dt, dx, c):
    unew = u.copy()
    for i in range(1, len(u) - 1):
        unew[i] = u[i] - (c * dt / (2 * dx)) * (u[i + 1] - u[i - 1]) + (c ** 2 * dt ** 2 / (2 * dx ** 2)) * (
                    u[i + 1] - 2 * u[i] + u[i - 1])
    return unew


# Sélection des temps à afficher
times = [0, 1, 2, 3, 4, 5, 6]

# Méthodes à tester
methods = {
    "Explicite Centré": explicite_centre,
    "Implicite Centré": implicite_centre,
    "Explicite Décentré Amont": explicite_decentre_amont,
    "Lax-Friedrichs": lax_friedrichs,
    "Lax-Wendroff": lax_wendroff
}

# Boucle sur chaque cas
for i, (Nx, dt, x, u0) in enumerate(zip(Nx_list, dt_list, x_list, u0_list)):
    dx = L / Nx
    u_initial = u0.copy()
    case_label = f'Cas {chr(97 + i)} (h={dx}, τ={dt})'

    # Boucle sur chaque méthode
    for method_name, method in methods.items():
        u = u_initial.copy()
        results = {time: None for time in times}
        results[0] = u0.copy()

        # Boucle temporelle
        Nt = int(T / dt)
        for n in range(1, Nt + 1):
            t = n * dt

            # Application du schéma numérique
            u = method(u, dt, dx, c)

            # Condition périodique
            u[0] = u[-2]
            u[-1] = u[1]

            # Enregistrer les résultats aux temps spécifiés
            if t in times:
                results[t] = u.copy()

        # Tracé des résultats
        plt.figure(figsize=(10, 6))
        for time in times:
            if results[time] is not None:
                plt.plot(x, results[time], label=f't={time}')
        plt.xlabel('x')
        plt.ylabel('u')
        plt.legend()
        plt.title(f'{method_name} - {case_label}')
        plt.show()


'''
#1 On remarque qu'en fonction de la méthode, les résultats sont différents : 
=> Explicite centré : Les courbes obtenues sont cohérentes
=> Implicite centré : On remarque des irrégularités sur les t à partir de 2
=> Explicite décentré : Les courbes obtenues sont cohérentes
=> Lax-Friedrichs : Les courbes s'applatissent lorsque t augmente
=> Lax-Wendroff : On obtient les mêmes courbes que pour explicite centré et décentré


#2 On test les méthodes avec les différents pas :
(a)
=> Explicite centré : Les courbes obtenues semblent nulles pour la plupart sauf t=6
=> Implicite centré : 
=> Explicite décentré : 
=> Lax-Friedrichs : 
=> Lax-Wendroff : 

 (b)
=> Explicite centré : 
=> Implicite centré : 
=> Explicite décentré : 
=> Lax-Friedrichs : 
=> Lax-Wendroff : 

(c)
=> Explicite centré : 
=> Implicite centré : 
=> Explicite décentré : 
=> Lax-Friedrichs : 
=> Lax-Wendroff : 


'''