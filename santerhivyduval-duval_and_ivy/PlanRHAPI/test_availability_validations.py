#!/usr/bin/env python3
"""
Script de test pour vérifier les nouvelles validations des disponibilités
"""

import requests
import json
from datetime import datetime, date, timedelta

# Configuration
API_BASE_URL = "http://localhost:8000"

def test_availability_validations():
    """Test des nouvelles validations de disponibilités"""
    print("🧪 Test des validations de disponibilités...")
    
    # Test 1: Format de date invalide
    print("\n1. Test format de date invalide:")
    invalid_date_data = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": "2024-13-45",  # Date invalide
        "start_time": "09:00",
        "end_time": "17:00",
        "commentaire": "Test date invalide"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/availabilities", json=invalid_date_data)
        if response.status_code == 400:
            print("✅ Validation date invalide - OK")
            print(f"   Message: {response.json().get('detail', '')}")
        else:
            print(f"❌ Validation date invalide - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 2: Format d'heure invalide
    print("\n2. Test format d'heure invalide:")
    invalid_time_data = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": "2024-12-15",
        "start_time": "25:00",  # Heure invalide
        "end_time": "17:00",
        "commentaire": "Test heure invalide"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/availabilities", json=invalid_time_data)
        if response.status_code == 400:
            print("✅ Validation heure invalide - OK")
            print(f"   Message: {response.json().get('detail', '')}")
        else:
            print(f"❌ Validation heure invalide - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 3: Plage horaire invalide (fin < début)
    print("\n3. Test plage horaire invalide:")
    invalid_range_data = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": "2024-12-15",
        "start_time": "17:00",
        "end_time": "09:00",  # Fin avant début
        "commentaire": "Test plage invalide"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/availabilities", json=invalid_range_data)
        if response.status_code == 400:
            print("✅ Validation plage horaire invalide - OK")
            print(f"   Message: {response.json().get('detail', '')}")
        else:
            print(f"❌ Validation plage horaire invalide - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 4: Utilisateur inexistant
    print("\n4. Test utilisateur inexistant:")
    invalid_user_data = {
        "user_id": "000000000000000000000000",  # ID utilisateur inexistant
        "date": "2024-12-15",
        "start_time": "09:00",
        "end_time": "17:00",
        "commentaire": "Test utilisateur inexistant"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/availabilities", json=invalid_user_data)
        if response.status_code == 400:
            print("✅ Validation utilisateur inexistant - OK")
            print(f"   Message: {response.json().get('detail', '')}")
        else:
            print(f"❌ Validation utilisateur inexistant - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 5: Données valides
    print("\n5. Test données valides:")
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    valid_data = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": tomorrow,
        "start_time": "09:00",
        "end_time": "17:00",
        "commentaire": "Test données valides"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/availabilities", json=valid_data)
        if response.status_code == 200:
            print("✅ Validation données valides - OK")
            created_availability = response.json().get('data', {})
            availability_id = created_availability.get('id')
            print(f"   Disponibilité créée avec l'ID: {availability_id}")
            
            # Nettoyer en supprimant la disponibilité de test
            if availability_id:
                try:
                    delete_response = requests.delete(f"{API_BASE_URL}/availabilities/{availability_id}")
                    if delete_response.status_code == 200:
                        print("   Disponibilité de test supprimée")
                except Exception as e:
                    print(f"   Erreur lors de la suppression: {e}")
        else:
            print(f"❌ Validation données valides - Erreur {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_edge_cases():
    """Test des cas limites"""
    print("\n🧪 Test des cas limites...")
    
    # Test 1: Date limite (29 février année bissextile)
    print("\n1. Test date limite (29 février):")
    leap_year_data = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": "2024-02-29",  # 2024 est bissextile
        "start_time": "09:00",
        "end_time": "17:00",
        "commentaire": "Test année bissextile"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/availabilities", json=leap_year_data)
        if response.status_code == 200:
            print("✅ Date bissextile valide - OK")
            # Nettoyer
            created_availability = response.json().get('data', {})
            availability_id = created_availability.get('id')
            if availability_id:
                requests.delete(f"{API_BASE_URL}/availabilities/{availability_id}")
        else:
            print(f"❌ Date bissextile - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test 2: Heures limites
    print("\n2. Test heures limites:")
    edge_time_data = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": "2024-12-15",
        "start_time": "00:00",
        "end_time": "23:59",
        "commentaire": "Test heures limites"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/availabilities", json=edge_time_data)
        if response.status_code == 200:
            print("✅ Heures limites valides - OK")
            # Nettoyer
            created_availability = response.json().get('data', {})
            availability_id = created_availability.get('id')
            if availability_id:
                requests.delete(f"{API_BASE_URL}/availabilities/{availability_id}")
        else:
            print(f"❌ Heures limites - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Fonction principale"""
    print("🚀 Test des validations de disponibilités")
    print("=" * 60)
    
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
    test_availability_validations()
    test_edge_cases()
    
    print("\n" + "=" * 60)
    print("🎉 Tests de validation terminés!")
    print("\n📋 Validations testées:")
    print("1. ✅ Format de date (YYYY-MM-DD)")
    print("2. ✅ Format d'heure (HH:MM)")
    print("3. ✅ Plage horaire (fin > début)")
    print("4. ✅ Existence de l'utilisateur")
    print("5. ✅ Cas limites (année bissextile, heures limites)")

if __name__ == "__main__":
    main()
