#!/usr/bin/env python3
"""
Exemple d'utilisation du scraper web
"""

from app import extraire_site_web, afficher_resume
import os
import shutil

def exemple_simple():
    """
    Exemple d'utilisation simple
    """
    print("🌐 EXEMPLE SIMPLE")
    print("=" * 40)
    
    url = "https://example.com"
    dossier = "exemple_simple"
    
    # Nettoyer le dossier s'il existe
    if os.path.exists(dossier):
        shutil.rmtree(dossier)
    
    try:
        # Télécharger le site
        resultats = extraire_site_web(url, dossier)
        
        # Afficher le résumé
        afficher_resume(resultats)
        
        # Vérifier les fichiers créés
        if os.path.exists(f"{dossier}/index.html"):
            print(f"✅ Fichier HTML original créé")
        if os.path.exists(f"{dossier}/index_local.html"):
            print(f"✅ Fichier HTML local créé")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")

def exemple_avec_gestion_erreurs():
    """
    Exemple avec gestion complète des erreurs
    """
    print("\n🛡️  EXEMPLE AVEC GESTION D'ERREURS")
    print("=" * 45)
    
    urls_test = [
        "https://example.com",           # URL valide
        "https://site-inexistant-xyz.com",  # URL inexistante
        "pas_une_url",                   # URL invalide
        None                             # URL None
    ]
    
    for i, url in enumerate(urls_test, 1):
        print(f"\n📋 Test {i}: {url}")
        
        try:
            resultats = extraire_site_web(url, f"test_erreur_{i}")
            print(f"✅ Succès: {len(resultats['html_original'])} caractères téléchargés")
            
        except ValueError as e:
            print(f"⚠️  Erreur de validation: {e}")
            
        except Exception as e:
            print(f"❌ Erreur de téléchargement: {e}")

def exemple_analyse_resultats():
    """
    Exemple d'analyse détaillée des résultats
    """
    print("\n📊 EXEMPLE D'ANALYSE DES RÉSULTATS")
    print("=" * 45)
    
    url = "https://example.com"
    dossier = "analyse_resultats"
    
    # Nettoyer le dossier s'il existe
    if os.path.exists(dossier):
        shutil.rmtree(dossier)
    
    try:
        resultats = extraire_site_web(url, dossier)
        
        print(f"🌐 URL analysée: {url}")
        print(f"📄 Taille HTML: {len(resultats['html_original'])} caractères")
        print(f"🎨 Fichiers CSS trouvés: {len(resultats['fichiers_css'])}")
        print(f"⚡ Fichiers JS trouvés: {len(resultats['fichiers_js'])}")
        print(f"🖼️  Images trouvées: {len(resultats['images'])}")
        
        # Analyser le contenu HTML
        if resultats['html_original']:
            html = resultats['html_original']
            print(f"\n📝 Analyse du contenu:")
            print(f"   - Contient 'DOCTYPE': {'DOCTYPE' in html.upper()}")
            print(f"   - Contient des styles: {'<style' in html}")
            print(f"   - Contient des scripts: {'<script' in html}")
            print(f"   - Nombre de liens: {html.count('<a ')}")
            print(f"   - Nombre d'images: {html.count('<img ')}")
        
        # Lister les fichiers téléchargés
        if resultats['fichiers_css']:
            print(f"\n🎨 Fichiers CSS:")
            for css in resultats['fichiers_css']:
                print(f"   - {css['fichier_local']}")
        
        if resultats['fichiers_js']:
            print(f"\n⚡ Fichiers JavaScript:")
            for js in resultats['fichiers_js']:
                print(f"   - {js['fichier_local']}")
        
        if resultats['images']:
            print(f"\n🖼️  Images:")
            for img in resultats['images']:
                print(f"   - {img['fichier_local']}")
        
        # Afficher les erreurs s'il y en a
        if resultats['erreurs']:
            print(f"\n❌ Erreurs rencontrées:")
            for erreur in resultats['erreurs']:
                print(f"   - {erreur}")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")

def nettoyer_fichiers_test():
    """
    Nettoie tous les fichiers de test créés
    """
    print("\n🧹 NETTOYAGE DES FICHIERS DE TEST")
    print("=" * 40)
    
    dossiers_test = [
        "exemple_simple",
        "analyse_resultats",
        "test_erreur_1",
        "test_erreur_2", 
        "test_erreur_3",
        "test_erreur_4",
        "test_final"
    ]
    
    for dossier in dossiers_test:
        if os.path.exists(dossier):
            shutil.rmtree(dossier)
            print(f"🗑️  Supprimé: {dossier}")
    
    print("✅ Nettoyage terminé")

if __name__ == "__main__":
    print("🚀 EXEMPLES D'UTILISATION DU SCRAPER WEB")
    print("=" * 50)
    
    # Exécuter les exemples
    exemple_simple()
    exemple_avec_gestion_erreurs()
    exemple_analyse_resultats()
    
    # Demander si on veut nettoyer
    print("\n" + "=" * 50)
    reponse = input("Voulez-vous nettoyer les fichiers de test ? (o/N): ")
    if reponse.lower() in ['o', 'oui', 'y', 'yes']:
        nettoyer_fichiers_test()
    
    print("\n🎯 EXEMPLES TERMINÉS")
    print("Consultez les dossiers créés pour voir les résultats.")
