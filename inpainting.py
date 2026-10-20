import cv2 as cv
import numpy as np

def generer_lignes_aleatoires(dimensions, nb_lignes=20, epaisseur_max=4):
    """Génère une liste de traits aléatoires."""
    hauteur, largeur = dimensions[:2]
    lignes = []

    for _ in range(nb_lignes):
        pt1 = (np.random.randint(0, largeur), np.random.randint(0, hauteur))
        pt2 = (np.random.randint(0, largeur), np.random.randint(0, hauteur))
        epaisseur = np.random.randint(1, epaisseur_max + 1)
        lignes.append((pt1, pt2, epaisseur))

    return lignes


def dessiner_masque(dimensions, lignes):
    """Dessine un masque binaire (0 et 255) à partir de traits aléatoires."""
    hauteur, largeur = dimensions[:2]
    masque = np.zeros((hauteur, largeur), dtype=np.uint8)
    for pt1, pt2, epaisseur in lignes:
        cv.line(masque, pt1, pt2, 255, epaisseur)
    return masque

# Chargement de l'image
img = cv.imread('images/images.jfif')
if img is None:
    raise FileNotFoundError("Image introuvable. Vérifiez le chemin du fichier.")

NB_LIGNES = 25
rayon = 3
lignes = generer_lignes_aleatoires(img.shape, nb_lignes=NB_LIGNES, epaisseur_max=5)


# Slider de dégradation : 0% = image originale, 100% = toutes les lignes du masque
def degradation(val):
    nb_lignes_actives = round(NB_LIGNES * val / 100)
    masque_courant = dessiner_masque(img.shape, lignes[:nb_lignes_actives])

    img_abimee = img.copy()
    img_abimee[masque_courant == 255] = 255

    if nb_lignes_actives:
        restaure_telea = cv.inpaint(img_abimee, masque_courant, rayon, cv.INPAINT_TELEA)
        restaure_ns = cv.inpaint(img_abimee, masque_courant, rayon, cv.INPAINT_NS)
    else:
        restaure_telea = img_abimee.copy()
        restaure_ns = img_abimee.copy()

    # Toutes les fenêtres sont réaffichées ensemble pour rester synchronisées
    cv.imshow('2 - Masque aleatoire', masque_courant)
    cv.imshow('3 - Image abimee', img_abimee)
    cv.imshow('4 - Restauration Telea', restaure_telea)
    cv.imshow('5 - Restauration Navier-Stokes', restaure_ns)


# Affichage des étapes
cv.imshow('1 - Image originale', img)
cv.imshow('2 - Masque aleatoire', np.zeros(img.shape[:2], dtype=np.uint8))
cv.imshow('3 - Image abimee', img)
cv.imshow('4 - Restauration Telea', img)
cv.imshow('5 - Restauration Navier-Stokes', img)

# Création du slider
cv.createTrackbar('Degradation', '1 - Image originale', 0, 100, degradation)
degradation(cv.getTrackbarPos('Degradation', '1 - Image originale'))

# Boucle d'événements : indispensable pour que le slider rafraîchisse les images
while True:
    touche = cv.waitKey(20) & 0xFF
    if touche in (27, ord('q')):
        break

cv.destroyAllWindows()