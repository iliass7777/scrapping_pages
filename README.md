# Scraper Web - Téléchargeur de Sites Web

Ce script Python permet de télécharger une page web complète avec tous ses fichiers associés (CSS, JavaScript, images).

## 🚀 Fonctionnalités

- ✅ Téléchargement de pages HTML complètes
- ✅ Extraction et téléchargement des fichiers CSS
- ✅ Extraction et téléchargement des fichiers JavaScript
- ✅ Extraction et téléchargement des images
- ✅ Création d'une version locale avec liens modifiés
- ✅ Gestion robuste des erreurs
- ✅ Validation des URLs
- ✅ Protection contre les fichiers trop volumineux (limite 50MB)
- ✅ Noms de fichiers sécurisés et compatibles multi-OS

## 📦 Installation

### Prérequis
- Python 3.6+
- pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

Ou manuellement :
```bash
pip install requests beautifulsoup4
```

## 🔧 Utilisation

### Utilisation basique

```python
from app import extraire_site_web, afficher_resume

# Télécharger un site
url = "https://example.com"
resultats = extraire_site_web(url, "mon_site_telecharge")

# Afficher le résumé
afficher_resume(resultats)
```

### Utilisation en ligne de commande

```bash
python3 app.py
```

### Paramètres

- `url` (str) : L'URL du site à télécharger
- `dossier_sortie` (str, optionnel) : Le dossier de destination (défaut: "site_telecharge")

## 📁 Structure des fichiers téléchargés

```
dossier_sortie/
├── index.html              # Page HTML originale
├── index_local.html         # Page HTML avec liens locaux
├── css/                     # Fichiers CSS
│   ├── style.css
│   └── ...
├── js/                      # Fichiers JavaScript
│   ├── script.js
│   └── ...
└── images/                  # Images
    ├── logo.png
    └── ...
```

## 🧪 Tests

Exécuter les tests :

```bash
python3 test_scraper.py
```

## ⚠️ Limitations

- Limite de taille de fichier : 50MB par fichier
- Timeout de téléchargement : 30 secondes
- Seuls les protocoles HTTP/HTTPS sont supportés
- Les fichiers JavaScript dynamiques ne sont pas exécutés

## 🛠️ Corrections apportées

### Bugs corrigés :
1. **Validation des URLs** : Ajout de vérifications pour les URLs invalides ou None
2. **Gestion des noms de fichiers** : Utilisation de hash MD5 pour éviter les collisions
3. **Correspondance des liens** : Mapping précis URL → fichier local
4. **Gestion des erreurs** : Gestion spécifique des timeouts et erreurs réseau
5. **Sécurité des fichiers** : Nettoyage des caractères interdits dans les noms
6. **Éviter l'écrasement** : Numérotation automatique des fichiers dupliqués

### Améliorations :
- Limite de taille des fichiers téléchargés
- Meilleure gestion des extensions de fichiers
- Validation robuste des URLs
- Messages d'erreur plus informatifs
- Structure de code plus maintenable

## 📝 Exemple d'utilisation

```python
# Exemple complet
from app import extraire_site_web, afficher_resume

try:
    # Télécharger le site
    resultats = extraire_site_web(
        url="https://httpbin.org/html",
        dossier_sortie="test_site"
    )
    
    # Afficher les résultats
    afficher_resume(resultats)
    
    # Accéder aux données
    print(f"HTML téléchargé : {len(resultats['html_original'])} caractères")
    print(f"Fichiers CSS : {len(resultats['fichiers_css'])}")
    print(f"Fichiers JS : {len(resultats['fichiers_js'])}")
    print(f"Images : {len(resultats['images'])}")
    
except ValueError as e:
    print(f"Erreur de validation : {e}")
except Exception as e:
    print(f"Erreur : {e}")
```

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou proposer une pull request.

## 📄 Licence

Ce projet est sous licence MIT.
