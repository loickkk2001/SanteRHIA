#!/usr/bin/env python3
"""
Script de test pour vérifier que tous les endpoints de planification fonctionnent correctement
"""

import requests
import json
from datetime import datetime, date, timedelta

# Configuration
API_BASE_URL = "http://localhost:8000"

def test_endpoint(url, method="GET", data=None, expected_status=200):
    """Test un endpoint et affiche le résultat"""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        
        print(f"\n🔍 Test: {method} {url}")
        print(f"Status: {response.status_code}")
        
        if response.status_code == expected_status:
            print("✅ Succès")
            if response.headers.get('content-type', '').startswith('application/json'):
                data = response.json()
                if isinstance(data, dict) and 'data' in data:
                    print(f"Données: {len(data['data'])} éléments")
                else:
                    print(f"Réponse: {str(data)[:100]}...")
        else:
            print("❌ Échec")
            print(f"Erreur: {response.text}")
        
        return response.status_code == expected_status
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def main():
    """Teste tous les endpoints de planification"""
    print("🚀 Test des endpoints de planification")
    print("=" * 50)
    
    # Test 1: Endpoint des utilisateurs
    test_endpoint(f"{API_BASE_URL}/users")
    
    # Test 2: Endpoint des disponibilités
    test_endpoint(f"{API_BASE_URL}/availabilities")
    
    # Test 3: Endpoint des disponibilités avec filtres
    test_endpoint(f"{API_BASE_URL}/availabilities?status=proposé")
    
    # Test 4: Endpoint des plannings
    test_endpoint(f"{API_BASE_URL}/plannings")
    
    # Test 5: Endpoint des services
    test_endpoint(f"{API_BASE_URL}/services")
    
    # Test 6: Endpoint des alertes
    test_endpoint(f"{API_BASE_URL}/alerts")
    
    # Test 7: Endpoint des anomalies
    test_endpoint(f"{API_BASE_URL}/anomalies")
    
    # Test 8: Endpoint des événements
    test_endpoint(f"{API_BASE_URL}/events")
    
    print("\n" + "=" * 50)
    print("🎯 Résumé des tests")
    
    # Test de création d'une disponibilité
    print("\n📝 Test de création d'une disponibilité...")
    today = date.today()
    tomorrow = today + timedelta(days=1)
    
    availability_data = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": tomorrow.strftime("%Y-%m-%d"),
        "start_time": "08:00",
        "end_time": "16:00",
        "commentaire": "Test de création via script"
    }
    
    response = requests.post(f"{API_BASE_URL}/availabilities", json=availability_data)
    if response.status_code == 200:
        print("✅ Création de disponibilité réussie")
        availability_id = response.json()['data']['id']
        
        # Test de mise à jour
        print("\n📝 Test de mise à jour d'une disponibilité...")
        update_data = {"status": "validé"}
        response = requests.put(f"{API_BASE_URL}/availabilities/{availability_id}", json=update_data)
        if response.status_code == 200:
            print("✅ Mise à jour de disponibilité réussie")
        else:
            print(f"❌ Échec de mise à jour: {response.text}")
    else:
        print(f"❌ Échec de création: {response.text}")
    
    print("\n🎉 Tests terminés !")
    print("\n💡 Si tous les tests sont ✅, l'API est prête pour l'application Angular")

if __name__ == "__main__":
    main()






