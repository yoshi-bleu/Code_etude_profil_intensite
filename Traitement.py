import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

from imageJ_v2 import epaisseur
# Chemins vers les fichiers CSV dans le dossier "resultats"
base_dir = Path(__file__).resolve().parent
resultats_dir = base_dir / "resultats"

print("début du traitement des données aquises")

N = epaisseur

#verifier la valeur de N
print("N =", N)

donneesR = []
donneesG = []
donneesB = []
for j in range(0, N):
    csv_files = {
        'R': resultats_dir / f"profil_R{j}.csv",
        'G': resultats_dir / f"profil_G{j}.csv",
        'B': resultats_dir / f"profil_B{j}.csv"
    }

    # Couleurs associées aux canaux
    colors = {
        'R': 'red',
        'G': 'green',
        'B': 'blue'
    }

    # Vérifiez si tous les fichiers existent
    for canal, path in csv_files.items():
        if not path.exists():
            print(f"❌ Fichier introuvable pour le canal {canal} : {path}")
            exit(1)

    # Tracer les graphiques pour chaque fichier
    plt.figure(figsize=(10, 6))
    I = np.zeros((N, 3))
    i = 0
    for canal, path in csv_files.items():
        try:
            # Charger les données du fichier CSV
            data = pd.read_csv(path, header=None, names=["Position", "Intensité"])
            print(f"✅ Données chargées depuis : {path}")
            if i == 0:
                donneesR.append(data["Intensité"])
            elif i == 1:
                donneesG.append(data["Intensité"])
            elif i == 2:
                donneesB.append(data["Intensité"])
            I[j][i] = np.sum(data["Intensité"])
            i = i + 1
        except Exception as e:
            print(f"❌ Erreur lors du chargement des données pour le canal {canal} au trait {j} : {e}")
            exit(1)

donneesR = np.array(donneesR).T
donneesG = np.array(donneesG).T
donneesB = np.array(donneesB).T

Rfin = np.array([np.mean(i) for i in donneesR])
Gfin = np.array([np.mean(i) for i in donneesG])
Bfin = np.array([np.mean(i) for i in donneesB])

# Enregistrer les moyennes dans des fichiers CSV
pd.DataFrame({"Position": data["Position"], "Intensité Moyenne": Rfin}).to_csv(resultats_dir / "R_moyenne.csv", index=False)
pd.DataFrame({"Position": data["Position"], "Intensité Moyenne": Gfin}).to_csv(resultats_dir / "G_moyenne.csv", index=False)
pd.DataFrame({"Position": data["Position"], "Intensité Moyenne": Bfin}).to_csv(resultats_dir / "B_moyenne.csv", index=False)
print("✅ Les moyennes des courbes ont été enregistrées dans le dossier 'resultats'.")

# On a besoin de la position qui est la même pour tous les fichiers
# donc on peut prendre la position du premier fichier
data = pd.read_csv(resultats_dir / "profil_R0.csv", header=None, names=["Position", "Intensité"])

# Tracer les données avec la couleur associée
plt.plot(data["Position"], Rfin, label=f"Profil R", color='r')
plt.plot(data["Position"], Gfin, label=f"Profil G", color='g')
plt.plot(data["Position"], Bfin, label=f"Profil B", color='b')
# Ajouter les détails du graphique
plt.title("Profils d'intensités moyennes (R, G, B)", fontsize=16)
plt.xlabel("Position (pixels)", fontsize=14)
plt.ylabel("Intensité", fontsize=14)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Afficher le graphique
plt.show()

# Enregistrer le graphique
plt.savefig(resultats_dir / "profils_intensite_moyennes.png")

# Calcul des ratios
I = I.T
print("R/G =", np.mean(I[0]) / np.mean(I[1]))
print("R/B =", np.mean(I[0]) / np.mean(I[2]))
print("G/B =", np.mean(I[1]) / np.mean(I[2]))

ratios = np.array(["R/G","R/B","G/B"])
Valeurs_ratios = np.array([np.mean(I[0]) / np.mean(I[1]), np.mean(I[0]) / np.mean(I[2]), np.mean(I[1]) / np.mean(I[2])])
# Enregistrer les ratios dans un fichier CSV
ratios_df = pd.DataFrame({"Ratios": ratios, "Valeurs": Valeurs_ratios})
ratios_df.to_csv(resultats_dir / "ratios.csv", index=False)

plt.figure(figsize=(10, 6))
plt.bar(ratios, Valeurs_ratios, color=['red', 'green', 'blue'])
plt.title("Ratios des intensités", fontsize=16)
plt.xlabel("Rapports", fontsize=14)
plt.ylabel("Valeurs des ratios", fontsize=14)
plt.legend()
plt.tight_layout()
plt.show()

# Enregistrer le graphique des ratios
plt.savefig(resultats_dir / "ratios.png")
