# Gravité artificielle : simulateur de station en rotation

Petit projet pour montrer comment une station spatiale en rotation recrée une sensation de poids, et pourquoi une petite station qui tourne vite est inconfortable.

## Contenu

| Fichier | Rôle |
|---|---|
| `index.html` | Simulateur interactif : on règle le rayon et la vitesse, on voit la station tourner et ce que ressent l'astronaute. |
| `gravite_artificielle.py` | Script Python qui calcule les valeurs et trace les figures. |
| `figures/` | Figures générées par le script (utilisables dans un rapport). |

## Ce que montre le simulateur

1. **La gravité ressentie** au plancher : `a = ω²r`, avec `ω = 2πN/60` (N en tours par minute).
2. **La différence entre la tête et les pieds** : la tête est plus près du centre, elle ressent `1 − h/r` fois la gravité des pieds.
3. **L'effet Coriolis** :
   - en marchant dans le sens de la rotation, on se sent plus lourd ; en sens inverse, plus léger : `a± = (ωr ± v)²/r` ;
   - un objet lâché depuis la hauteur de la tête ne tombe pas à la verticale, il atterrit un peu « en arrière ».

| Station donnant 1 g | Tête / pieds (1,80 m) | Variation du poids en marchant à 1,5 m/s |
|---|---|---|
| 25 m, 6 tr/min | 93 % | ± 19 % |
| 56 m, 4 tr/min | 97 % | ± 13 % |
| 224 m, 2 tr/min | 99 % | ± 6 % |

## Lancer le projet

**Simulateur :** ouvrir `index.html` dans un navigateur, rien à installer.

**Script Python :**
```bash
pip install numpy matplotlib
python gravite_artificielle.py
```

## Mettre le simulateur en ligne avec GitHub Pages

1. Créer un dépôt sur GitHub (par exemple `gravite-artificielle`) et y envoyer les fichiers.
2. Dans le dépôt : **Settings → Pages**.
3. Dans *Source*, choisir **Deploy from a branch**, puis la branche `main` et le dossier `/ (root)`.
4. Après une ou deux minutes, le simulateur est accessible à l'adresse `https://<ton-pseudo>.github.io/gravite-artificielle/`.

## Sources

- A. Globus et T. W. Hall, *Space Settlement Population Rotation Tolerance*, NSS Space Settlement Journal, 2017. https://nss.org/wp-content/uploads/NSS-JOURNAL-Space-Settlement-Population-Rotation-Tolerance.pdf
- T. W. Hall, *The Architecture of Artificial-Gravity Environments for Long-Duration Space Habitation*, thèse, University of Michigan, 1994. https://artificial-gravity.com/Dissertation/FrontMatter.htm
- *Design Limits on Large Space Stations*, arXiv:2408.00152. https://arxiv.org/abs/2408.00152
