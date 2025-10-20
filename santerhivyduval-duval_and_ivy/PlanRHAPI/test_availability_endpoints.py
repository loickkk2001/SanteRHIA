#!/usr/bin/env python3
"""
Script de test pour vérifier les endpoints des disponibilités
"""

import requests
import json
from datetime import datetime, date, timedelta

# Configuration
API_BASE_URL = "http://localhost:8000"

def test_availability_endpoints():
    """Test des endpoints de disponibilités"""
    print("🧪 Test des endpoints de disponibilités...")
    
    # Test 1: Récupérer toutes les disponibilités
    try:
        response = requests.get(f"{API_BASE_URL}/availabilities")
        if response.status_code == 200:
            print("✅ GET /availabilities - OK")
            availabilities = response.json().get('data', [])
            print(f"   Nombre de disponibilités trouvées: {len(availabilities)}")
        else:
            print(f"❌ GET /availabilities - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /availabilities - Exception: {e}")
    
    # Test 2: Créer une disponibilité de test
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    test_availability = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": tomorrow,
        "start_time": "09:00",
        "end_time": "17:00",
        "status": "proposé",
        "commentaire": "Test de création de disponibilité"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/availabilities", json=test_availability)
        if response.status_code == 200:
            print("✅ POST /availabilities - OK")
            created_availability = response.json().get('data', {})
            availability_id = created_availability.get('id')
            print(f"   Disponibilité créée avec l'ID: {availability_id}")
            
            # Test 3: Récupérer la disponibilité par ID
            if availability_id:
                try:
                    response = requests.get(f"{API_BASE_URL}/availabilities/{availability_id}")
                    if response.status_code == 200:
                        print("✅ GET /availabilities/{id} - OK")
                        availability_data = response.json().get('data', {})
                        print(f"   Statut: {availability_data.get('status')}")
                    else:
                        print(f"❌ GET /availabilities/{id} - Erreur {response.status_code}")
                except Exception as e:
                    print(f"❌ GET /availabilities/{id} - Exception: {e}")
            
            # Test 4: Mettre à jour la disponibilité
            if availability_id:
                update_data = {
                    "status": "validé",
                    "commentaire": "Disponibilité validée par le test"
                }
                
                try:
                    response = requests.patch(f"{API_BASE_URL}/availabilities/{availability_id}", json=update_data)
                    if response.status_code == 200:
                        print("✅ PATCH /availabilities/{id} - OK")
                        updated_availability = response.json().get('data', {})
                        print(f"   Nouveau statut: {updated_availability.get('status')}")
                    else:
                        print(f"❌ PATCH /availabilities/{id} - Erreur {response.status_code}")
                        print(f"   Réponse: {response.text}")
                except Exception as e:
                    print(f"❌ PATCH /availabilities/{id} - Exception: {e}")
            
            # Test 5: Supprimer la disponibilité de test
            if availability_id:
                try:
                    response = requests.delete(f"{API_BASE_URL}/availabilities/{availability_id}")
                    if response.status_code == 200:
                        print("✅ DELETE /availabilities/{id} - OK")
                        print("   Disponibilité de test supprimée")
                    else:
                        print(f"❌ DELETE /availabilities/{id} - Erreur {response.status_code}")
                except Exception as e:
                    print(f"❌ DELETE /availabilities/{id} - Exception: {e}")
        else:
            print(f"❌ POST /availabilities - Erreur {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ POST /availabilities - Exception: {e}")

def test_availability_filters():
    """Test des filtres de disponibilités"""
    print("\n🧪 Test des filtres de disponibilités...")
    
    # Test 1: Récupérer par utilisateur
    try:
        response = requests.get(f"{API_BASE_URL}/availabilities/user/684314eb3bd4c4c00ce9c019")
        if response.status_code == 200:
            print("✅ GET /availabilities/user/{user_id} - OK")
            availabilities = response.json().get('data', [])
            print(f"   Disponibilités trouvées pour l'utilisateur: {len(availabilities)}")
        else:
            print(f"❌ GET /availabilities/user/{user_id} - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /availabilities/user/{user_id} - Exception: {e}")
    
    # Test 2: Récupérer par date
    today = date.today().strftime("%Y-%m-%d")
    try:
        response = requests.get(f"{API_BASE_URL}/availabilities/date/{today}")
        if response.status_code == 200:
            print("✅ GET /availabilities/date/{date} - OK")
            availabilities = response.json().get('data', [])
            print(f"   Disponibilités trouvées pour {today}: {len(availabilities)}")
        else:
            print(f"❌ GET /availabilities/date/{date} - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /availabilities/date/{date} - Exception: {e}")
    
    # Test 3: Récupérer par statut
    try:
        response = requests.get(f"{API_BASE_URL}/availabilities/status/proposé")
        if response.status_code == 200:
            print("✅ GET /availabilities/status/{status} - OK")
            availabilities = response.json().get('data', [])
            print(f"   Disponibilités proposées: {len(availabilities)}")
        else:
            print(f"❌ GET /availabilities/status/{status} - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /availabilities/status/{status} - Exception: {e}")

def main():
    """Fonction principale"""
    print("🚀 Test des endpoints de disponibilités")
    print("=" * 50)
    
    # Vérifier que l'API est accessible
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            print("✅ API accessible")
        else:
            print(f"❌ API non accessible - Status: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Impossible de se connecter à l'API: {e}")
        print("   Assurez-vous que l'API est démarrée avec: uvicorn main:app --reload")
        return
    
    # Exécuter les tests
    test_availability_endpoints()
    test_availability_filters()
    
    print("\n" + "=" * 50)
    print("🎉 Tests terminés!")
    print("\n📋 Endpoints testés:")
    print("1. ✅ POST /availabilities - Création de disponibilité")
    print("2. ✅ GET /availabilities - Récupération de toutes les disponibilités")
    print("3. ✅ GET /availabilities/{id} - Récupération par ID")
    print("4. ✅ PATCH /availabilities/{id} - Mise à jour de disponibilité")
    print("5. ✅ DELETE /availabilities/{id} - Suppression de disponibilité")
    print("6. ✅ GET /availabilities/user/{user_id} - Filtrage par utilisateur")
    print("7. ✅ GET /availabilities/date/{date} - Filtrage par date")
    print("8. ✅ GET /availabilities/status/{status} - Filtrage par statut")

if __name__ == "__main__":
    main()
