#!/usr/bin/env python3
"""
Script de test pour vérifier que les endpoints SAPHIR fonctionnent
"""

import requests
import json

def test_endpoints():
    base_url = "http://localhost:8000"
    
    endpoints = [
        "/alerts",
        "/anomalies", 
        "/events",
        "/events/upcoming"
    ]
    
    print("🧪 Test des endpoints SAPHIR...")
    print("=" * 50)
    
    for endpoint in endpoints:
        try:
            url = f"{base_url}{endpoint}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: OK")
                print(f"   Données: {len(data.get('data', []))} éléments")
            else:
                print(f"❌ {endpoint}: Erreur {response.status_code}")
                print(f"   Réponse: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {endpoint}: Erreur de connexion - {e}")
        
        print()
    
    print("=" * 50)
    print("Test terminé!")

if __name__ == "__main__":
    test_endpoints()













