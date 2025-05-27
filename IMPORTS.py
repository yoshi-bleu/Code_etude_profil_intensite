# Bibliothèques standard
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from pathlib import Path

# Bibliothèques tierces
import imagej
import tkinter as tk
from tkinter import messagebox,filedialog, Tk
import threading
from astropy.io import fits  # Pour lire les fichiers FITS


# Configuration l'épaisseur du trait
epaisseur = 11