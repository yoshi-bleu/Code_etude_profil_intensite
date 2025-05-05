import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

os.environ['JAVA_TOOL_OPTIONS'] = '-Djava.awt.headless=true'

from imageJ_v2 import epaisseur
# Chemins vers les fichiers CSV dans le dossier "resultats"
base_dir = Path(__file__).resolve().parent
resultats_dir = base_dir / "resultats"

print("début du traitement des données aquises")

N = epaisseur

# Vérifier la valeur de N
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

    # Vérifiez si tous les fichiers existent
    for canal, path in csv_files.items():
        if not path.exists():
            print(f"❌ Fichier introuvable pour le canal {canal} : {path}")
            exit(1)

    # Charger les données et les enregistrer dans des tableaux
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
            i += 1
        except Exception as e:
            print(f"❌ Erreur lors du chargement des données pour le canal {canal} au trait {j} : {e}")
            exit(1)

# Convertir les données en tableaux numpy
donneesR = np.array(donneesR).T
donneesG = np.array(donneesG).T
donneesB = np.array(donneesB).T

# Calculer les moyennes
Rfin = np.array([np.mean(i) for i in donneesR])
Gfin = np.array([np.mean(i) for i in donneesG])
Bfin = np.array([np.mean(i) for i in donneesB])

dRfin = np.array([np.sqrt(1/(11*10)) * np.sqrt(np.sum((Rfin[i] - donneesR[i])**2)) for i in range(len(Rfin))])
dGfin = np.array([np.sqrt(1/(11*10)) * np.sqrt(np.sum((Gfin[i] - donneesG[i])**2)) for i in range(len(Gfin))])
dBfin = np.array([np.sqrt(1/(11*10)) * np.sqrt(np.sum((Bfin[i] - donneesB[i])**2)) for i in range(len(Bfin))])

# Enregistrer les moyennes dans des fichiers CSV
pd.DataFrame({"Position": data["Position"], "Intensité Moyenne": Rfin}).to_csv(resultats_dir / "R_moyenne.csv", index=False)
pd.DataFrame({"Position": data["Position"], "Intensité Moyenne": Gfin}).to_csv(resultats_dir / "G_moyenne.csv", index=False)
pd.DataFrame({"Position": data["Position"], "Intensité Moyenne": Bfin}).to_csv(resultats_dir / "B_moyenne.csv", index=False)
print("✅ Les moyennes des courbes ont été enregistrées dans le dossier 'resultats'.")

# Calculer les incertitudes
dRfin = np.array([np.sqrt(1/(11*10)) * np.sqrt(np.sum((Rfin[i] - donneesR[i])**2)) for i in range(len(Rfin))])
dGfin = np.array([np.sqrt(1/(11*10)) * np.sqrt(np.sum((Gfin[i] - donneesG[i])**2)) for i in range(len(Gfin))])
dBfin = np.array([np.sqrt(1/(11*10)) * np.sqrt(np.sum((Bfin[i] - donneesB[i])**2)) for i in range(len(Bfin))])

# Enregistrer les incertitudes dans des fichiers CSV
pd.DataFrame({"Position": data["Position"], "Incertitude Statistique R": dRfin}).to_csv(resultats_dir / "incertitudes_statistiquesR.csv", index=False)
pd.DataFrame({"Position": data["Position"], "Incertitude Statistique G": dGfin}).to_csv(resultats_dir / "incertitudes_statistiquesG.csv", index=False)
pd.DataFrame({"Position": data["Position"], "Incertitude Statistique B": dBfin}).to_csv(resultats_dir / "incertitudes_statistiquesB.csv", index=False)
print("✅ Les incertitudes statistiques ont été enregistrées dans le dossier 'resultats'.")

"""print("Rfin :", Rfin)
print("Gfin :", Gfin)
print("Bfin :", Bfin)
print("Position :", data["Position"])"""

# Afficher le graphique des profils d'intensité moyennes
plt.figure(figsize=(10, 6))
plt.plot(data["Position"], Rfin, label=f"Profil R", color='r')
plt.plot(data["Position"], Gfin, label=f"Profil G", color='g')
plt.plot(data["Position"], Bfin, label=f"Profil B", color='b')


# Tracer les incertitudes 
plt.errorbar(data["Position"], Rfin, yerr=dRfin, color='r')
plt.errorbar(data["Position"], Gfin, yerr=dGfin, color='g')
plt.errorbar(data["Position"], Bfin, yerr=dBfin, color='b')
plt.title("Profils d'intensités moyennes (R, G, B) avec incertitudes statistiques", fontsize=16)
plt.xlabel("Position (pixels)", fontsize=14)
plt.ylabel("Intensité", fontsize=14)
plt.legend()
plt.grid(True)
plt.tight_layout()

# Enregistrer le graphique et l'afficher
plt.savefig(resultats_dir / "profils_intensite_moyennes.png")
plt.show()  # Afficher le graphique
plt.close()  # Fermer le graphique

# Calcul des ratios
I = I.T
print("R/G =", np.mean(I[0]) / np.mean(I[1]))
print("R/B =", np.mean(I[0]) / np.mean(I[2]))
print("G/B =", np.mean(I[1]) / np.mean(I[2]))

ratios = np.array(["R/G", "R/B", "G/B"])
Valeurs_ratios = np.array([np.mean(I[0]) / np.mean(I[1]), np.mean(I[0]) / np.mean(I[2]), np.mean(I[1]) / np.mean(I[2])])

# Enregistrer les ratios dans un fichier CSV
ratios_df = pd.DataFrame({"Ratios": ratios, "Valeurs": Valeurs_ratios})
ratios_df.to_csv(resultats_dir / "ratios.csv", index=False)

# Tracer le graphique des ratios
plt.figure(figsize=(10, 6))
plt.bar(ratios, Valeurs_ratios, color=['red', 'green', 'blue'])
plt.title("Ratios des intensités", fontsize=16)
plt.xlabel("Rapports", fontsize=14)
plt.ylabel("Valeurs des ratios", fontsize=14)
plt.tight_layout()

# Enregistrer le graphique et l'afficher
plt.savefig(resultats_dir / "ratios.png")
plt.show()  # Afficher le graphique
plt.close()  # Fermer le graphique
