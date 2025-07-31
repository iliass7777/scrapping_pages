#!/usr/bin/env python3
"""
Script de test pour le scraper web
"""

import os
import shutil
from app import extraire_site_web, afficher_resume

def test_scraper():
    """
    Teste le scraper avec différents sites
    """
    
    # Sites de test
    sites_test = [
        {
            'url': 'https://httpbin.org/html',
            'nom': 'httpbin_html',
            'description': 'Page HTML simple avec du contenu'
        },
        {
            'url': 'https://example.com',
            'nom': 'example_com',
            'description': 'Site exemple basique'
        }
    ]
    
    print("🧪 TESTS DU SCRAPER WEB")
    print("=" * 50)
    
    for i, site in enumerate(sites_test, 1):
        print(f"\n📋 Test {i}: {site['description']}")
        print(f"🌐 URL: {site['url']}")
        
        dossier_test = f"test_{site['nom']}"
        
        # Nettoyer le dossier s'il existe
        if os.path.exists(dossier_test):
            shutil.rmtree(dossier_test)
        
        try:
            # Tester le scraping
            resultats = extraire_site_web(site['url'], dossier_test)
            
            # Afficher les résultats
            afficher_resume(resultats)
            
            # Vérifier que les fichiers ont été créés
            fichiers_crees = []
            if os.path.exists(f"{dossier_test}/index.html"):
                fichiers_crees.append("index.html")
            if os.path.exists(f"{dossier_test}/index_local.html"):
                fichiers_crees.append("index_local.html")
            
            print(f"📁 Fichiers créés: {', '.join(fichiers_crees)}")
            
            if resultats['erreurs']:
                print(f"⚠️  Erreurs détectées: {len(resultats['erreurs'])}")
            else:
                print("✅ Test réussi sans erreurs")
                
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
        
        print("-" * 30)

def test_validation_url():
    """
    Teste la validation des URLs
    """
    print("\n🔍 TEST DE VALIDATION DES URLs")
    print("=" * 40)
    
    urls_invalides = [
        "pas_une_url",
        "ftp://example.com",
        "",
        None
    ]
    
    for url in urls_invalides:
        try:
            print(f"Test URL invalide: {url}")
            extraire_site_web(url, "test_invalide")
            print("❌ L'URL aurait dû être rejetée")
        except (ValueError, TypeError) as e:
            print(f"✅ URL correctement rejetée: {e}")
        except Exception as e:
            print(f"⚠️  Erreur inattendue: {e}")

if __name__ == "__main__":
    test_scraper()
    test_validation_url()
    
    print("\n🎯 TESTS TERMINÉS")
    print("Vérifiez les dossiers créés pour voir les résultats.")
