#!/usr/bin/env python3
from IMPORTS import *  # Importer tout depuis imports.py

print("debut obtention des profils d'intensité via Fiji") 

# Répertoire du script (script.py)
base_dir = Path(__file__).resolve().parent

# Chemin vers le dossier Fiji (dans le même dossier que le script)
chemin_Fiji = base_dir / "Fiji"

# Initialiser ImageJ
try:
    ij = imagej.init(str(chemin_Fiji), mode='headless')
    print("✅ ImageJ initialisé avec succès.")
except Exception as e:
    print(f"❌ Erreur lors de l'initialisation d'ImageJ : {e}")
    exit(1)


#réglage de la demi-épaisseur
print("L'épaisseur du trait est de 11 pixels")
epaisseur = 11
L_epaisseur = np.arange(epaisseur)

# Liste des images (R, G, B)
images = {
    'R': base_dir / "Images" / "R1.fit",
    'G': base_dir / "Images" / "G1.fit",
    'B': base_dir / "Images" / "B1.fit"
}

# Vérifiez si les fichiers d'image existent
for canal, path in images.items():
    if not os.path.exists(path):
        print(f"❌ Fichier introuvable pour le canal {canal} : {path}")
        exit(1)

# Crée un dossier "resultats" s'il n'existe pas
output_dir = base_dir / "resultats"
output_dir.mkdir(exist_ok=True)

# Coordonnées du profil principal (en pixels)
from coordonnees import x1, y1, x2, y2
x1, y1 = 2430, 2700
x2, y2 = 2580, 1925

#listes des coordonnées de tous les points des traits
List_x_1 = np.array([x1-5+i for i in L_epaisseur])
List_y_1 = np.array([y1-5+i for i in L_epaisseur])
List_x_2 = np.array([x2-5+i for i in L_epaisseur])
List_y_2 = np.array([y2-5+i for i in L_epaisseur])

#boucle pour traiter chaque trait
n=0
for X1, Y1, X2, Y2 in zip(List_x_1, List_y_1, List_x_2, List_y_2):
    # Traitement de chaque image
    for canal, path in images.items():
        #print(f"🔄 Traitement du canal {canal}"+str(n)+f" avec le fichier {path}")
        macro = f"""
        open("{path}");
        makeLine({X1}, {Y1}, {X2}, {Y2});
        run("Plot Profile");
        Plot.getValues(x, y);
        output = "{output_dir}/profil_{canal}{n}.csv";
        file = File.open(output);
        for (i = 0; i < x.length; i++) {{
            print(file, x[i] + "," + y[i]);
        }}
        File.close(file);
        """
        try:
            ij.py.run_macro(macro)
            #print(f"✅ Profil exporté : {output_dir}/profil_{canal}"+str(n)+".csv")
        except Exception as e:
            print(f"❌ Erreur lors de l'exécution de la macro pour le canal {canal}"+str(n)+f": {e}")
    n+=1
print("✅ Tous les profils ont été exportés.")
#ij.get_context().dispose()  # Fermer ImageJ proprement
