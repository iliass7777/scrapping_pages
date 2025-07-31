#!/usr/bin/env python3
"""
Application Flask pour le scraper web
Interface web pour télécharger des sites web
"""

from flask import Flask, render_template, request, jsonify, send_file, flash, redirect, url_for
import os
import shutil
import zipfile
from datetime import datetime
import threading
import time
from app import extraire_site_web, afficher_resume

app = Flask(__name__)
app.secret_key = 'scraper_web_secret_key_2024'

# Configuration
UPLOAD_FOLDER = 'downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Créer le dossier de téléchargements
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Stockage des tâches en cours
tasks = {}

@app.route('/')
def index():
    """Page d'accueil avec le formulaire"""
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def scrape_website():
    """Traiter la demande de scraping"""
    try:
        url = request.form.get('url', '').strip()
        
        if not url:
            flash('Veuillez entrer une URL', 'error')
            return redirect(url_for('index'))
        
        # Valider l'URL
        if not url.startswith(('http://', 'https://')):
            flash('L\'URL doit commencer par http:// ou https://', 'error')
            return redirect(url_for('index'))
        
        # Générer un nom de dossier unique
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        folder_name = f"site_{timestamp}"
        download_path = os.path.join(app.config['UPLOAD_FOLDER'], folder_name)
        
        # Lancer le scraping
        resultats = extraire_site_web(url, download_path)
        
        if resultats['erreurs']:
            error_msg = '; '.join(resultats['erreurs'])
            flash(f'Erreurs lors du téléchargement: {error_msg}', 'error')
            return redirect(url_for('index'))
        
        # Créer un fichier ZIP
        zip_path = f"{download_path}.zip"
        create_zip(download_path, zip_path)
        
        # Préparer les informations pour l'affichage
        info = {
            'url': url,
            'folder': folder_name,
            'zip_file': f"{folder_name}.zip",
            'html_size': len(resultats['html_original']),
            'css_count': len(resultats['fichiers_css']),
            'js_count': len(resultats['fichiers_js']),
            'images_count': len(resultats['images']),
            'files': get_file_list(download_path)
        }
        
        flash('Site téléchargé avec succès!', 'success')
        return render_template('result.html', info=info)
        
    except ValueError as e:
        flash(f'Erreur de validation: {str(e)}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'Erreur lors du téléchargement: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    """Télécharger le fichier ZIP"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            flash('Fichier non trouvé', 'error')
            return redirect(url_for('index'))
    except Exception as e:
        flash(f'Erreur lors du téléchargement: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/preview/<folder>/<path:filename>')
def preview_file(folder, filename):
    """Prévisualiser un fichier"""
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], folder, filename)
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return "Fichier non trouvé", 404
    except Exception as e:
        return f"Erreur: {str(e)}", 500

@app.route('/cleanup')
def cleanup():
    """Nettoyer les anciens fichiers"""
    try:
        cleanup_old_files()
        flash('Nettoyage effectué avec succès', 'success')
    except Exception as e:
        flash(f'Erreur lors du nettoyage: {str(e)}', 'error')
    return redirect(url_for('index'))

def create_zip(folder_path, zip_path):
    """Créer un fichier ZIP du dossier téléchargé"""
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

def get_file_list(folder_path):
    """Obtenir la liste des fichiers téléchargés"""
    files = []
    if os.path.exists(folder_path):
        for root, dirs, filenames in os.walk(folder_path):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), folder_path)
                file_size = os.path.getsize(os.path.join(root, filename))
                files.append({
                    'name': filename,
                    'path': rel_path,
                    'size': format_file_size(file_size)
                })
    return files

def format_file_size(size_bytes):
    """Formater la taille du fichier"""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def cleanup_old_files():
    """Nettoyer les fichiers de plus de 1 heure"""
    current_time = time.time()
    for item in os.listdir(app.config['UPLOAD_FOLDER']):
        item_path = os.path.join(app.config['UPLOAD_FOLDER'], item)
        if os.path.getctime(item_path) < current_time - 3600:  # 1 heure
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            else:
                os.remove(item_path)

if __name__ == '__main__':
    print("🚀 Démarrage du serveur Flask...")
    print("📱 Interface web disponible sur: http://localhost:5000")
    print("🛑 Appuyez sur Ctrl+C pour arrêter")
    app.run(debug=True, host='0.0.0.0', port=5000)
