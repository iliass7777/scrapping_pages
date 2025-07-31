#!/usr/bin/env python3
"""
Script de démarrage pour l'application Flask Scraper Web
"""

import os
import sys
import webbrowser
import time
import threading
from flask_app import app

def open_browser():
    """Ouvre le navigateur après un délai"""
    time.sleep(2)  # Attendre que le serveur démarre
    webbrowser.open('http://localhost:5000')

def main():
    """Fonction principale"""
    print("🌐 SCRAPER WEB - APPLICATION FLASK")
    print("=" * 50)
    print("🚀 Démarrage du serveur...")
    print("📱 Interface web: http://localhost:5000")
    print("🌍 Accessible depuis le réseau: http://0.0.0.0:5000")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50)
    
    # Ouvrir le navigateur automatiquement
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Démarrer l'application Flask
        app.run(
            debug=False,  # Désactiver le debug pour la production
            host='0.0.0.0',
            port=5000,
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du serveur...")
        print("👋 Au revoir !")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
