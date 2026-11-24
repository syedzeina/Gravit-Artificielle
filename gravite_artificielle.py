"""
Gravité artificielle dans une station spatiale en rotation.

Ce script calcule et trace :
  1. la vitesse de rotation nécessaire pour obtenir 1 g selon le rayon ;
  2. le rapport entre la gravité ressentie à la tête et aux pieds ;
  3. la variation de poids quand on marche (effet Coriolis).

Les figures sont enregistrées dans le dossier "figures/".
Utilisation : python gravite_artificielle.py
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

G = 9.81          # pesanteur terrestre (m/s²)
TAILLE = 1.80     # taille de l'astronaute (m)
MARCHE = 1.5      # vitesse de marche (m/s)

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)


def omega(n_trmin):
    """Convertit une vitesse en tours par minute en vitesse angulaire (rad/s)."""
    return 2 * np.pi * n_trmin / 60


def acceleration(r, n_trmin):
    """Gravité ressentie au plancher : a = ω² r."""
    return omega(n_trmin) ** 2 * r


def rayon_pour(a_voulue, n_trmin):
    """Rayon nécessaire pour obtenir l'accélération voulue : r = a / ω²."""
    return a_voulue / omega(n_trmin) ** 2


def rapport_tete_pieds(r, h=TAILLE):
    """Gravité à la tête divisée par la gravité aux pieds : 1 - h/r."""
    return 1 - h / r


def poids_en_marchant(r, n_trmin, v=MARCHE):
    """Gravité ressentie en marchant dans le sens de la rotation (+) ou en sens inverse (-)."""
    w = omega(n_trmin)
    return (w * r + v) ** 2 / r, (w * r - v) ** 2 / r


def tableau():
    print("Stations donnant 1 g :")
    print(f"{'tr/min':>7} {'rayon (m)':>10} {'tête/pieds':>11} {'marche ±':>9}")
    for n in [1, 2, 3, 4, 6, 10]:
        r = rayon_pour(G, n)
        pro, retro = poids_en_marchant(r, n)
        ecart = (pro - retro) / 2 / G * 100
        print(f"{n:>7} {r:>10.1f} {rapport_tete_pieds(r) * 100:>10.1f}% {ecart:>8.1f}%")
    print()
    print("Exemples historiques :")
    for nom, r, n in [("Von Braun 1952 (76 m de diamètre)", 38, 3),
                      ("Station de 2001 (≈300 m de diamètre)", 150, 1),
                      ("Brevet Energia (5 tr/min, 0,5 g)", rayon_pour(0.5 * G, 5), 5)]:
        a = acceleration(r, n)
        print(f"  {nom}: r = {r:.0f} m, {n} tr/min → a = {a:.2f} m/s² ({a / G:.2f} g)")


def figures():
    plt.rcParams.update({"figure.dpi": 150, "font.size": 11})
    rayons = np.linspace(5, 500, 500)

    # 1. Vitesse nécessaire pour 1 g
    n_1g = np.sqrt(G / rayons) * 60 / (2 * np.pi)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(rayons, n_1g, color="#2b6cb0", lw=2)
    ax.axhspan(0, 2, color="#38a169", alpha=0.12, label="Confortable (≤ 2 tr/min)")
    ax.axhspan(2, 6, color="#dd6b20", alpha=0.12, label="Adaptation nécessaire (2 à 6 tr/min)")
    ax.axhspan(6, 14, color="#e53e3e", alpha=0.10, label="Trop rapide pour y vivre")
    for r, n in [(25, 6), (56, 4), (224, 2)]:
        ax.plot(r, n, "o", color="#1a202c")
        ax.annotate(f"{r} m, {n} tr/min", (r, n), textcoords="offset points", xytext=(8, 6))
    ax.set(xlabel="Rayon de la station (m)", ylabel="Vitesse de rotation (tr/min)",
           title="Vitesse de rotation nécessaire pour obtenir 1 g", ylim=(0, 14), xlim=(0, 500))
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "1_vitesse_pour_1g.png")

    # 2. Tête / pieds
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(rayons, rapport_tete_pieds(rayons) * 100, color="#2b6cb0", lw=2)
    for r in [25, 224]:
        ax.plot(r, rapport_tete_pieds(r) * 100, "o", color="#1a202c")
        ax.annotate(f"{r} m : {rapport_tete_pieds(r) * 100:.0f} %", (r, rapport_tete_pieds(r) * 100),
                    textcoords="offset points", xytext=(8, -14))
    ax.set(xlabel="Rayon de la station (m)", ylabel="Gravité à la tête / aux pieds (%)",
           title=f"Différence de gravité entre la tête et les pieds (personne de {TAILLE} m)",
           ylim=(60, 101), xlim=(0, 500))
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "2_tete_pieds.png")

    # 3. Marche et Coriolis (stations à 1 g)
    n_vals = np.linspace(0.5, 10, 300)
    r_vals = rayon_pour(G, n_vals)
    pro, retro = poids_en_marchant(r_vals, n_vals)
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.plot(n_vals, pro / G, color="#c53030", lw=2, label="Marche dans le sens de la rotation")
    ax.plot(n_vals, retro / G, color="#2b6cb0", lw=2, label="Marche en sens inverse")
    ax.axhline(1, color="#4a5568", ls="--", lw=1, label="Debout immobile (1 g)")
    ax.set(xlabel="Vitesse de rotation de la station (tr/min)", ylabel="Poids ressenti (en g)",
           title=f"Effet Coriolis : poids en marchant à {MARCHE} m/s (stations à 1 g)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(OUT / "3_coriolis_marche.png")

    print(f"Figures enregistrées dans {OUT}/")


if __name__ == "__main__":
    tableau()
    figures()
