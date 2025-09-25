import numpy as np


def generate_matrix_M(N):
    # Taille de la matrice
    size = N * N
    # Création d'une matrice de zéros
    M = np.zeros((size, size))

    for i in range(N):
        for j in range(N):
            index = i * N + j
            M[index, index] = -4  # Élément central
            if i > 0:  # Si pas sur la première ligne, ajouter le voisin du haut
                M[index, index - N] = 1
            if i < N - 1:  # Si pas sur la dernière ligne, ajouter le voisin du bas
                M[index, index + N] = 1
            if j > 0:  # Si pas sur la première colonne, ajouter le voisin de gauche
                M[index, index - 1] = 1
            if j < N - 1:  # Si pas sur la dernière colonne, ajouter le voisin de droite
                M[index, index + 1] = 1

    return M


def print_matrix(M):
    for row in M:
        print(" ".join(f"{int(x):3}" for x in row))


# Taille de la grille
N = 4
# Génération de la matrice M
M = generate_matrix_M(N)
# Affichage de la matrice M
print("Matrice M = 1/h**2")
print_matrix(M)
