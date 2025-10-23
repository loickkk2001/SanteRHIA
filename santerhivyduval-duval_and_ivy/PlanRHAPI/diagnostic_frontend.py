#!/usr/bin/env python3
"""
Script de diagnostic pour le frontend Angular
"""

import requests
import json
import time

def check_frontend_status():
    """Vérifie le statut du frontend Angular"""
    print("🔍 Diagnostic du frontend Angular")
    print("=" * 50)
    
    # Vérifier si le serveur Angular répond
    try:
        print("1. Vérification du serveur Angular (port 4200)...")
        response = requests.get("http://localhost:4200", timeout=5)
        if response.status_code == 200:
            print("   ✅ Serveur Angular accessible")
            print(f"   📄 Contenu HTML reçu: {len(response.text)} caractères")
            
            # Vérifier si le contenu contient l'app-root
            if "<app-root></app-root>" in response.text:
                print("   ✅ Balise <app-root> trouvée")
            else:
                print("   ❌ Balise <app-root> manquante")
                
        else:
            print(f"   ❌ Serveur Angular non accessible - Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur de connexion au serveur Angular: {e}")
        return False
    
    # Vérifier si le serveur backend répond
    try:
        print("\n2. Vérification du serveur backend (port 8000)...")
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("   ✅ Serveur backend accessible")
        else:
            print(f"   ❌ Serveur backend non accessible - Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur de connexion au serveur backend: {e}")
    
    # Vérifier les endpoints critiques
    endpoints_to_check = [
        "/login",
        "/user-info",
        "/availabilities",
        "/plannings"
    ]
    
    print("\n3. Vérification des endpoints backend...")
    for endpoint in endpoints_to_check:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=3)
            if response.status_code in [200, 405, 422]:  # 405 = Method Not Allowed, 422 = Unprocessable Entity
                print(f"   ✅ {endpoint} - Accessible")
            else:
                print(f"   ⚠️  {endpoint} - Status: {response.status_code}")
        except Exception as e:
            print(f"   ❌ {endpoint} - Erreur: {e}")
    
    print("\n" + "=" * 50)
    print("💡 Solutions possibles pour un frontend vide:")
    print("1. Ouvrir les outils de développement du navigateur (F12)")
    print("2. Vérifier l'onglet Console pour les erreurs JavaScript")
    print("3. Vérifier l'onglet Network pour les requêtes échouées")
    print("4. Vider le cache du navigateur (Ctrl+F5)")
    print("5. Redémarrer le serveur Angular: npm start")
    print("6. Vérifier que tous les modules PrimeNG sont correctement importés")
    
    return True

if __name__ == "__main__":
    check_frontend_status()







