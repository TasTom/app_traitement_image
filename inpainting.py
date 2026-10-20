import cv2 as cv
import numpy as np

def generer_masque_aleatoire(dimensions, nb_lignes=20, epaisseur_max=4):
    """Génère un masque binaire (0 et 255) avec des traits aléatoires."""
    hauteur, largeur = dimensions[:2]
    # 1. Création d'une matrice noire (valeur 0) en entiers non signés 8 bits
    # 0 = pixel sain (à conserver), 255 = pixel dégradé (à réparer)
    masque = np.zeros((hauteur, largeur), dtype=np.uint8)

    #Dessin de traits aléatoires
    for _ in range(nb_lignes):
        #Cordonnées (x,y) aléatoires dans la limite de l'image
        pt1 = (np.random.randint(0, largeur), np.random.randint(0, hauteur))
        pt2 = (np.random.randint(0, largeur), np.random.randint(0, hauteur))
        # Épaisseur aléatoire entre 1 et epaisseur_max pixels
        epaisseur = np.random.randint(1, epaisseur_max + 1)
        # cv.line(image, point_depart, point_arrivee, couleur, epaisseur)
        cv.line(masque, pt1, pt2, 255, epaisseur)

    return masque

# Chargement de l'image
img = cv.imread('images/fleurs.jpeg')
if img is None:
    raise FileNotFoundError("Image introuvable. Vérifiez le chemin du fichier.")

# Création automatique du masque aux dimensions exactes de l'image
#On passe img.shape pour garantir que le masque a EXACTEMENT la même taille
masque = generer_masque_aleatoire(img.shape, nb_lignes=25, epaisseur_max=5)

# Création de l'image dégradée (pixels masqués remplacés par du blanc)
# Copie indépendante en mémoire pour ne pas écraser l'originale
img_abimee = img.copy()
# Indexation booléenne NumPy : là où le masque vaut 255, on remplace par du blanc [255, 255, 255]
img_abimee[masque == 255] = 255

# Restauration avec les deux méthodes d'OpenCV

# Rayon du voisinage circulaire considéré autour de chaque pixel à reconstruire
rayon = 3

#Méthode A : Algorithme de Telea (Fast Marching Method)
restaure_telea = cv.inpaint(img_abimee, masque, rayon, cv.INPAINT_TELEA)

# Méthode B : Algorithme de Navier-Stokes (Mécanique des fluides)
restaure_ns = cv.inpaint(img_abimee, masque, rayon, cv.INPAINT_NS)

# Affichage des étapes
cv.imshow('1 - Image originale', img)
cv.imshow('2 - Masque aleatoire', masque)
cv.imshow('3 - Image abimee', img_abimee)
cv.imshow('4 - Restauration Telea', restaure_telea)
cv.imshow('5 - Restauration Navier-Stokes', restaure_ns)

# Attend l'appui sur une touche du clavier pour fermer
cv.waitKey(0)
cv.destroyAllWindows()