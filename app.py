import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os
import re
from pathlib import Path
import hashlib

def extraire_site_web(url, dossier_sortie="site_telecharge"):
    """
    Télécharge une page web et tous ses fichiers CSS/JS

    Args:
        url (str): L'URL du site à télécharger
        dossier_sortie (str): Le dossier où sauvegarder les fichiers

    Returns:
        dict: Informations sur les fichiers téléchargés
    """

    # Valider l'URL
    if not url or not isinstance(url, str) or not url.startswith(('http://', 'https://')):
        raise ValueError("L'URL doit être une chaîne valide commençant par http:// ou https://")

    # Créer le dossier de sortie
    Path(dossier_sortie).mkdir(exist_ok=True)
    
    # Session pour maintenir les cookies/headers
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    
    resultats = {
        'html_original': '',
        'fichiers_css': [],
        'fichiers_js': [],
        'images': [],
        'erreurs': [],
        'url_vers_fichier': {}  # Mapping URL -> fichier local pour une correspondance exacte
    }
    
    try:
        # Télécharger la page principale
        print(f"Téléchargement de {url}...")
        response = session.get(url, timeout=30)
        response.raise_for_status()
        
        # Parser le HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        resultats['html_original'] = response.text
        
        # Sauvegarder le HTML original
        with open(f"{dossier_sortie}/index.html", 'w', encoding='utf-8') as f:
            f.write(response.text)
        
        # Extraire et télécharger les fichiers CSS
        for link in soup.find_all('link', rel='stylesheet'):
            href = link.get('href')
            if href:
                css_url = urljoin(url, href)
                nom_fichier = telecharger_fichier(session, css_url, dossier_sortie, 'css')
                if nom_fichier:
                    resultats['fichiers_css'].append({
                        'url_original': css_url,
                        'fichier_local': nom_fichier
                    })
                    resultats['url_vers_fichier'][css_url] = nom_fichier
        
        # Extraire et télécharger les fichiers JavaScript
        for script in soup.find_all('script', src=True):
            src = script.get('src')
            if src:
                js_url = urljoin(url, src)
                nom_fichier = telecharger_fichier(session, js_url, dossier_sortie, 'js')
                if nom_fichier:
                    resultats['fichiers_js'].append({
                        'url_original': js_url,
                        'fichier_local': nom_fichier
                    })
                    resultats['url_vers_fichier'][js_url] = nom_fichier
        
        # Extraire et télécharger les images
        for img in soup.find_all('img', src=True):
            src = img.get('src')
            if src:
                img_url = urljoin(url, src)
                nom_fichier = telecharger_fichier(session, img_url, dossier_sortie, 'images')
                if nom_fichier:
                    resultats['images'].append({
                        'url_original': img_url,
                        'fichier_local': nom_fichier
                    })
                    resultats['url_vers_fichier'][img_url] = nom_fichier
        
        # Ajouter l'URL de base pour la correspondance des liens
        resultats['base_url'] = url

        # Créer un HTML modifié avec les liens locaux
        html_modifie = modifier_liens_locaux(soup, resultats)
        with open(f"{dossier_sortie}/index_local.html", 'w', encoding='utf-8') as f:
            f.write(str(html_modifie))
        
        print(f"✅ Téléchargement terminé dans le dossier '{dossier_sortie}'")
        
    except Exception as e:
        resultats['erreurs'].append(f"Erreur principale: {str(e)}")
        print(f"❌ Erreur: {e}")
    
    return resultats

def telecharger_fichier(session, url, dossier_base, type_fichier):
    """
    Télécharge un fichier spécifique
    """
    try:
        # Vérifier que l'URL est valide
        if not url or not url.startswith(('http://', 'https://')):
            print(f"  ❌ URL invalide: {url}")
            return None

        response = session.get(url, timeout=30)
        response.raise_for_status()

        # Vérifier la taille du fichier (limite à 50MB)
        content_length = response.headers.get('content-length')
        if content_length and int(content_length) > 50 * 1024 * 1024:
            print(f"  ❌ Fichier trop volumineux ({content_length} bytes): {url}")
            return None

        # Créer le sous-dossier si nécessaire
        sous_dossier = f"{dossier_base}/{type_fichier}"
        Path(sous_dossier).mkdir(exist_ok=True)

        # Générer un nom de fichier valide
        nom_fichier = generer_nom_fichier(url, type_fichier)
        chemin_complet = f"{sous_dossier}/{nom_fichier}"

        # Éviter d'écraser des fichiers existants
        compteur = 1
        chemin_original = chemin_complet
        while os.path.exists(chemin_complet):
            nom_base, extension = os.path.splitext(chemin_original)
            chemin_complet = f"{nom_base}_{compteur}{extension}"
            compteur += 1

        # Sauvegarder le fichier
        with open(chemin_complet, 'wb') as f:
            f.write(response.content)

        print(f"  ✓ {type_fichier}: {os.path.basename(chemin_complet)}")
        return chemin_complet

    except requests.exceptions.Timeout:
        print(f"  ❌ Timeout lors du téléchargement: {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ❌ Erreur réseau {url}: {e}")
        return None
    except Exception as e:
        print(f"  ❌ Erreur téléchargement {url}: {e}")
        return None

def generer_nom_fichier(url, type_fichier):
    """
    Génère un nom de fichier valide à partir de l'URL
    """
    parsed = urlparse(url)
    nom = os.path.basename(parsed.path)

    if not nom or nom == '/' or nom == '':
        # Utiliser un hash plus robuste pour éviter les collisions
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        nom = f"fichier_{url_hash}"

    # Nettoyer le nom de fichier - caractères interdits sur différents OS
    nom = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', nom)

    # Limiter la longueur du nom de fichier
    if len(nom) > 100:
        nom = nom[:100]

    # Ajouter l'extension si manquante
    if type_fichier == 'css' and not nom.endswith('.css'):
        nom += '.css'
    elif type_fichier == 'js' and not nom.endswith('.js'):
        nom += '.js'
    elif type_fichier == 'images' and not any(nom.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp', '.ico']):
        nom += '.jpg'

    return nom

def modifier_liens_locaux(soup, resultats):
    """
    Modifie les liens dans le HTML pour pointer vers les fichiers locaux
    """
    soup_copie = BeautifulSoup(str(soup), 'html.parser')

    # Modifier les liens CSS - utiliser le mapping URL -> fichier pour une correspondance exacte
    for link in soup_copie.find_all('link', rel='stylesheet'):
        href = link.get('href')
        if href:
            # Reconstruire l'URL absolue pour la correspondance
            from urllib.parse import urljoin
            css_url = urljoin(resultats.get('base_url', ''), href)
            if css_url in resultats['url_vers_fichier']:
                link['href'] = resultats['url_vers_fichier'][css_url]

    # Modifier les liens JavaScript
    for script in soup_copie.find_all('script', src=True):
        src = script.get('src')
        if src:
            js_url = urljoin(resultats.get('base_url', ''), src)
            if js_url in resultats['url_vers_fichier']:
                script['src'] = resultats['url_vers_fichier'][js_url]

    # Modifier les liens des images
    for img in soup_copie.find_all('img', src=True):
        src = img.get('src')
        if src:
            img_url = urljoin(resultats.get('base_url', ''), src)
            if img_url in resultats['url_vers_fichier']:
                img['src'] = resultats['url_vers_fichier'][img_url]

    return soup_copie

def afficher_resume(resultats):
    """
    Affiche un résumé des fichiers téléchargés
    """
    print("\n" + "="*50)
    print("RÉSUMÉ DU TÉLÉCHARGEMENT")
    print("="*50)
    
    print(f"📄 HTML original: {len(resultats['html_original'])} caractères")
    print(f"🎨 Fichiers CSS: {len(resultats['fichiers_css'])}")
    print(f"⚡ Fichiers JS: {len(resultats['fichiers_js'])}")
    print(f"🖼️  Images: {len(resultats['images'])}")
    
    if resultats['erreurs']:
        print(f"❌ Erreurs: {len(resultats['erreurs'])}")
        for erreur in resultats['erreurs']:
            print(f"   - {erreur}")

# Exemple d'utilisation
if __name__ == "__main__":
    # Remplace par l'URL que tu veux télécharger
    url_site = "https://example.com"
    
    # Télécharger le site
    resultats = extraire_site_web(url_site, "mon_site_telecharge")
    
    # Afficher le résumé
    afficher_resume(resultats)
    
    # Accéder au code source HTML
    print("\n📄 Code source HTML (premiers 500 caractères):")
    print(resultats['html_original'][:500] + "...")