#!/usr/bin/env python3
"""
Test simple pour vérifier si l'application Angular se charge
"""

import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_angular_app():
    """Teste si l'application Angular se charge correctement"""
    print("🧪 Test de l'application Angular")
    print("=" * 40)
    
    # Configuration Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Mode sans interface
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    try:
        print("1. Lancement du navigateur...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print("2. Navigation vers l'application...")
        driver.get("http://localhost:4200")
        
        print("3. Attente du chargement de l'application...")
        wait = WebDriverWait(driver, 30)  # Attendre jusqu'à 30 secondes
        
        try:
            # Attendre que l'élément app-root soit présent
            app_root = wait.until(EC.presence_of_element_located((By.TAG_NAME, "app-root")))
            print("   ✅ Élément app-root trouvé")
            
            # Attendre que le contenu se charge (formulaire de connexion)
            login_form = wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
            print("   ✅ Formulaire de connexion trouvé")
            
            # Vérifier le titre de la page
            title = driver.title
            print(f"   📄 Titre de la page: {title}")
            
            # Vérifier s'il y a des erreurs dans la console
            logs = driver.get_log('browser')
            if logs:
                print(f"   ⚠️  {len(logs)} messages dans la console:")
                for log in logs[-5:]:  # Afficher les 5 derniers messages
                    print(f"      {log['level']}: {log['message']}")
            else:
                print("   ✅ Aucune erreur dans la console")
            
            # Prendre une capture d'écran
            screenshot_path = "angular_app_screenshot.png"
            driver.save_screenshot(screenshot_path)
            print(f"   📸 Capture d'écran sauvegardée: {screenshot_path}")
            
            print("\n✅ Application Angular fonctionne correctement!")
            
        except Exception as e:
            print(f"   ❌ Erreur lors du chargement: {e}")
            
            # Vérifier le code source de la page
            page_source = driver.page_source
            if "app-root" in page_source:
                print("   ℹ️  Élément app-root présent dans le HTML")
            else:
                print("   ❌ Élément app-root manquant dans le HTML")
                
            # Vérifier s'il y a des erreurs JavaScript
            logs = driver.get_log('browser')
            if logs:
                print(f"   ❌ {len(logs)} erreurs JavaScript trouvées:")
                for log in logs:
                    if log['level'] == 'SEVERE':
                        print(f"      ERREUR: {log['message']}")
        
        driver.quit()
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        print("💡 Assurez-vous que Chrome/Chromium est installé et que l'application Angular est accessible")

if __name__ == "__main__":
    test_angular_app()







