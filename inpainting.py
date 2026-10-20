import cv2 as cv
import numpy as np

def generer_masque_aleatoire(dimensions, nb_lignes=20, epaisseur_max=4):
    """Génère un masque binaire (0 et 255) avec des traits aléatoires."""
    hauteur, largeur = dimensions[:2]
    masque = np.zeros((hauteur, largeur), dtype=np.uint8)

    for _ in range(nb_lignes):
        pt1 = (np.random.randint(0, largeur), np.random.randint(0, hauteur))
        pt2 = (np.random.randint(0, largeur), np.random.randint(0, hauteur))
        epaisseur = np.random.randint(1, epaisseur_max + 1)
        cv.line(masque, pt1, pt2, 255, epaisseur)

    return masque

# Chargement de l'image
img = cv.imread('images/fleurs.jpeg')
if img is None:
    raise FileNotFoundError("Image introuvable. Vérifiez le chemin du fichier.")

# Création automatique du masque aux dimensions exactes de l'image
masque = generer_masque_aleatoire(img.shape, nb_lignes=25, epaisseur_max=5)

# Création de l'image dégradée (pixels masqués remplacés par du blanc)
img_abimee = img.copy()
img_abimee[masque == 255] = 255

# Restauration avec les deux méthodes d'OpenCV
rayon = 3
restaure_telea = cv.inpaint(img_abimee, masque, rayon, cv.INPAINT_TELEA)
restaure_ns = cv.inpaint(img_abimee, masque, rayon, cv.INPAINT_NS)

# Affichage des étapes
cv.imshow('1 - Image originale', img)
cv.imshow('2 - Masque aleatoire', masque)
cv.imshow('3 - Image abimee', img_abimee)
cv.imshow('4 - Restauration Telea', restaure_telea)
cv.imshow('5 - Restauration Navier-Stokes', restaure_ns)

cv.waitKey(0)
cv.destroyAllWindows()