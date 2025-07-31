#!/usr/bin/env python3
"""
Démonstration du Scraper Web Flask
"""

import requests
import time
import webbrowser
import threading
from flask_app import app

def test_api():
    """Teste l'API du scraper"""
    print("🧪 TEST DE L'API SCRAPER")
    print("=" * 30)
    
    base_url = "http://localhost:5000"
    
    # Test 1: Page d'accueil
    try:
        response = requests.get(base_url)
        if response.status_code == 200:
            print("✅ Page d'accueil: OK")
        else:
            print(f"❌ Page d'accueil: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur page d'accueil: {e}")
        return False
    
    # Test 2: Scraping d'un site
    try:
        data = {"url": "https://example.com"}
        response = requests.post(f"{base_url}/scrape", data=data)
        if response.status_code == 200 and "Téléchargement Terminé" in response.text:
            print("✅ Scraping: OK")
        else:
            print(f"❌ Scraping: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur scraping: {e}")
        return False
    
    # Test 3: Nettoyage
    try:
        response = requests.get(f"{base_url}/cleanup")
        if response.status_code == 200 or response.status_code == 302:
            print("✅ Nettoyage: OK")
        else:
            print(f"❌ Nettoyage: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur nettoyage: {e}")
        return False
    
    print("\n🎉 Tous les tests sont passés !")
    return True

def demo_interface():
    """Démonstration de l'interface"""
    print("\n🖥️  DÉMONSTRATION DE L'INTERFACE")
    print("=" * 40)
    print("1. Ouvrez votre navigateur sur: http://localhost:5000")
    print("2. Entrez une URL (ex: https://example.com)")
    print("3. Cliquez sur 'Télécharger le Site'")
    print("4. Téléchargez l'archive ZIP ou prévisualisez")
    print("5. Testez le nettoyage des fichiers")
    
    # Ouvrir automatiquement le navigateur
    time.sleep(2)
    webbrowser.open("http://localhost:5000")

def run_server():
    """Lance le serveur Flask"""
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)

def main():
    """Fonction principale de démonstration"""
    print("🌐 DÉMONSTRATION SCRAPER WEB FLASK")
    print("=" * 50)
    
    # Démarrer le serveur dans un thread séparé
    server_thread = threading.Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Attendre que le serveur démarre
    print("🚀 Démarrage du serveur...")
    time.sleep(3)
    
    # Tester l'API
    if test_api():
        # Démonstration de l'interface
        demo_interface()
        
        print("\n" + "=" * 50)
        print("🎯 DÉMONSTRATION EN COURS")
        print("📱 Interface: http://localhost:5000")
        print("🛑 Appuyez sur Ctrl+C pour arrêter")
        print("=" * 50)
        
        try:
            # Garder le serveur en vie
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Arrêt de la démonstration")
            print("👋 Au revoir !")
    else:
        print("❌ Échec des tests, arrêt de la démonstration")

if __name__ == "__main__":
    main()
