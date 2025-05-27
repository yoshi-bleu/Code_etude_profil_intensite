#!/usr/bin/env python3
from coordonnees import main as get_coords
from imageJ_v2 import init_imagej, run_imagej_task
from Traitement import main as analyze_data
from IMPORTS import *

def main():
    x1, y1, x2, y2 = get_coords()
    
    # Initialiser ImageJ
    init_thread = threading.Thread(target=init_imagej)
    init_thread.start()
    
    # Lancer le traitement une fois ImageJ prêt
    task_thread = threading.Thread(target=run_imagej_task, args=(x1, x2, y1, y2))
    task_thread.start()
    
    init_thread.join()
    task_thread.join()

    # Puis analyse
    analyze_data()
    print("✅  terminé.")

if __name__ == "__main__":
    main()