# 🌐 Scraper Web - Application Flask

Une application web moderne pour télécharger des sites web complets avec une interface utilisateur intuitive.

## 🚀 Fonctionnalités

- ✅ **Interface web moderne** avec Bootstrap 5
- ✅ **Formulaire simple** pour entrer l'URL
- ✅ **Téléchargement automatique** de tous les fichiers (HTML, CSS, JS, images)
- ✅ **Archive ZIP** générée automatiquement
- ✅ **Prévisualisation** du site téléchargé
- ✅ **Statistiques détaillées** des fichiers téléchargés
- ✅ **Gestion des erreurs** avec messages informatifs
- ✅ **Nettoyage automatique** des anciens fichiers
- ✅ **Interface responsive** pour mobile et desktop

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
pip install flask requests beautifulsoup4
```

## 🔧 Utilisation

### Démarrage rapide

```bash
python3 start_server.py
```

Le navigateur s'ouvrira automatiquement sur `http://localhost:5000`

### Démarrage manuel

```bash
python3 flask_app.py
```

Puis ouvrez votre navigateur sur `http://localhost:5000`

### Accès réseau

L'application est accessible depuis d'autres appareils du réseau via :
- `http://[VOTRE_IP]:5000`
- Par exemple : `http://192.168.1.100:5000`

## 🖥️ Interface Utilisateur

### Page d'accueil
- **Formulaire simple** : Entrez l'URL du site à télécharger
- **Validation automatique** : Vérification du format de l'URL
- **Design moderne** : Interface responsive avec animations

### Page de résultats
- **Statistiques** : Nombre de fichiers téléchargés par type
- **Téléchargement ZIP** : Archive complète du site
- **Prévisualisation** : Voir le site téléchargé dans le navigateur
- **Liste des fichiers** : Détails de tous les fichiers téléchargés

## 📁 Structure des fichiers

```
/
├── flask_app.py              # Application Flask principale
├── start_server.py           # Script de démarrage
├── app.py                    # Module de scraping
├── requirements.txt          # Dépendances
├── templates/                # Templates HTML
│   ├── index.html           # Page d'accueil
│   └── result.html          # Page de résultats
├── static/                   # Fichiers statiques (CSS, JS)
└── downloads/                # Dossier des téléchargements
    ├── site_20241221_143022/ # Dossier du site téléchargé
    └── site_20241221_143022.zip # Archive ZIP
```

## 🛠️ Fonctionnalités techniques

### Sécurité
- ✅ Validation des URLs
- ✅ Limite de taille des fichiers (50MB)
- ✅ Nettoyage des noms de fichiers
- ✅ Protection contre les chemins dangereux

### Performance
- ✅ Téléchargement multi-threadé
- ✅ Compression ZIP automatique
- ✅ Nettoyage automatique des anciens fichiers
- ✅ Gestion des timeouts

### Interface
- ✅ Design responsive (mobile-friendly)
- ✅ Messages d'erreur informatifs
- ✅ Indicateurs de progression
- ✅ Prévisualisation en temps réel

## 🔧 Configuration

### Variables d'environnement
```bash
export FLASK_ENV=development    # Mode développement
export FLASK_DEBUG=1           # Debug activé
```

### Configuration Flask
```python
# Dans flask_app.py
app.config['UPLOAD_FOLDER'] = 'downloads'  # Dossier de téléchargement
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # Limite 50MB
```

## 🧪 Test de l'application

### Test simple
1. Démarrez l'application : `python3 start_server.py`
2. Ouvrez `http://localhost:5000`
3. Entrez une URL : `https://example.com`
4. Cliquez sur "Télécharger le Site"
5. Téléchargez l'archive ZIP ou prévisualisez le résultat

### URLs de test recommandées
- `https://example.com` - Site simple
- `https://httpbin.org/html` - Page avec contenu HTML
- `https://www.w3.org` - Site avec CSS et images

## 🚨 Dépannage

### Erreur "Port déjà utilisé"
```bash
# Trouver le processus utilisant le port 5000
lsof -i :5000
# Tuer le processus
kill -9 [PID]
```

### Erreur de permissions
```bash
# Donner les permissions d'exécution
chmod +x start_server.py
chmod +x flask_app.py
```

### Problème d'installation Flask
```bash
# Installation avec --break-system-packages si nécessaire
pip install --break-system-packages flask
```

## 📱 Utilisation mobile

L'interface est optimisée pour les appareils mobiles :
- Design responsive
- Boutons tactiles
- Navigation simplifiée
- Affichage adaptatif

## 🔒 Sécurité et limitations

### Limitations
- Timeout de 30 secondes par fichier
- Limite de 50MB par fichier
- Pas d'exécution de JavaScript dynamique
- Protocoles HTTP/HTTPS uniquement

### Sécurité
- Validation stricte des URLs
- Nettoyage des noms de fichiers
- Protection contre les attaques de chemin
- Gestion sécurisée des erreurs

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :
1. Fork le projet
2. Créez une branche pour votre fonctionnalité
3. Committez vos changements
4. Poussez vers la branche
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT.

---

## 🎯 Utilisation rapide

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Démarrer l'application
python3 start_server.py

# 3. Ouvrir http://localhost:5000 dans votre navigateur

# 4. Entrer une URL et télécharger !
```

**Profitez de votre scraper web avec interface graphique ! 🎉**
