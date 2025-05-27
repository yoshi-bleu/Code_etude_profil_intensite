#!/usr/bin/env python3
from IMPORTS import *  # Importer tout depuis imports.py
#from coordonnees import x1, y1, x2, y2

ij = None
imagej_ready = threading.Event()

base_dir = Path(__file__).resolve().parent

images = {
    'R': base_dir / "Images" / "R1.fit",
    'G': base_dir / "Images" / "G1.fit",
    'B': base_dir / "Images" / "B1.fit"
}

output_dir = base_dir / "resultats"
output_dir.mkdir(exist_ok=True)

def init_imagej():
    global ij
    try:
        ij = imagej.init(mode='headless')
        print("✅ ImageJ initialisé avec succès.")
        imagej_ready.set()
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation d'ImageJ : {e}")

def run_imagej_task(x1, x2, y1, y2):
    imagej_ready.wait()
    print("Démarrage du traitement ImageJ...")

    L_epaisseur = np.arange(epaisseur)
    List_x_1 = np.array([x1-5+i for i in L_epaisseur])
    List_y_1 = np.array([y1-5+i for i in L_epaisseur])
    List_x_2 = np.array([x2-5+i for i in L_epaisseur])
    List_y_2 = np.array([y2-5+i for i in L_epaisseur])

    for n, (X1, Y1, X2, Y2) in enumerate(zip(List_x_1, List_y_1, List_x_2, List_y_2)):
        for canal, path in images.items():
            print(f"🔄 Traitement du canal {canal} {n} avec le fichier {path}")
            output_path = output_dir / f"profil_{canal}{n}.csv"

            macro = f"""
            open("{path.as_posix()}");
            makeLine({X1}, {Y1}, {X2}, {Y2});
            run("Plot Profile");
            Plot.getValues(x, y);
            file = File.open("{output_path.as_posix()}");
            for (i = 0; i < x.length; i++) {{
                print(file, x[i] + "," + y[i]);
            }}
            File.close(file);
            """

            try:
                ij.py.run_macro(macro)
                print(f"✅ Profil exporté : {output_path}")
            except Exception as e:
                print(f"❌ Erreur canal {canal} {n} : {e}")

    print("✅ Traitement ImageJ terminé.")


def main():
    print("Début de l'obtention des profils d'intensité via Fiji")
    for canal, path in images.items():
        print(f"Canal {canal} : {'✅ OK' if path.exists() else '❌ Manquant'}")

    t1 = threading.Thread(target=init_imagej)
    t2 = threading.Thread(target=run_imagej_task)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

#on a desactivé le main car on y fait directement appelle dans assemblage
#if __name__ == "__main__":
#   main()
