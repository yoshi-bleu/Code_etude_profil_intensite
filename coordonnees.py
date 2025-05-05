#!/usr/bin/env python3
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from tkinter import Tk, filedialog
from astropy.io import fits  # Pour lire les fichiers FITS

# Étape 1 : Choisir une image
Tk().withdraw()
file_path = filedialog.askopenfilename(title="Choisis une image",
                                       filetypes=[("Images", "*.jpg *.png *.tif *.jpeg *.fit *.fits")])
if not file_path:
    print("Aucune image sélectionnée.")
    exit()

# Étape 2 : Charger l'image
if file_path.endswith(('.fit', '.fits')):
    # Lire un fichier FITS
    with fits.open(file_path) as fits_file:
        img_data = fits_file[0].data  # Charger les données de l'image
        img = np.array(img_data, dtype=np.float32)  # Convertir en tableau numpy

        # Calculer les percentiles pour ajuster la luminosité
        p_low, p_high = np.percentile(img, (1, 99))  # 1% et 99% des valeurs
        img = np.clip((img - p_low) / (p_high - p_low), 0, 1)  # Normaliser entre 0 et 1

        # Inverser l'axe vertical pour corriger l'orientation
        img = np.flipud(img)
else:
    # Lire un fichier image standard
    img = mpimg.imread(file_path)
    if img.dtype == np.uint8:
        img = img.astype(np.float32) / 255.0  # Normaliser si nécessaire

# Étape 3 : Afficher l’image ajustée pour sélection
plt.imshow(img, cmap='gray')  # Utiliser 'gray' pour les images FITS
plt.title("Image ajustée : clique sur le point de départ puis d’arrivée")
points = plt.ginput(2, timeout=0)  # Sélection par clics
plt.close()

# Étape 4 : Résultat
(x1, y1), (x2, y2) = points
print(f"Point de départ : ({x1:.1f}, {y1:.1f})")
print(f"Point d’arrivée : ({x2:.1f}, {y2:.1f})")