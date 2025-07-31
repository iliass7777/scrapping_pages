#!/bin/bash

# Script de démarrage pour le Scraper Web Flask
# Usage: ./run.sh

echo "🌐 SCRAPER WEB - DÉMARRAGE"
echo "=========================="

# Vérifier si Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérifier si les dépendances sont installées
echo "📦 Vérification des dépendances..."
python3 -c "import flask, requests, bs4" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installation des dépendances manquantes..."
    pip install --break-system-packages -r requirements.txt
fi

# Créer les dossiers nécessaires
mkdir -p downloads templates static

echo "✅ Prêt à démarrer !"
echo "🚀 Lancement du serveur Flask..."
echo "📱 Interface web: http://localhost:5000"
echo "🛑 Appuyez sur Ctrl+C pour arrêter"
echo ""

# Démarrer l'application
python3 start_server.py
