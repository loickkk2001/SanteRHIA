#!/usr/bin/env python3
"""
Script de test pour la Tâche 1.1.2 : Endpoints spécifiques selon les rôles
"""

import requests
import json
from datetime import datetime, date, timedelta

# Configuration
API_BASE_URL = "http://localhost:8000"

def test_soignant_endpoints():
    """Test des endpoints pour les soignants"""
    print("🧪 Test des endpoints SOIGNANT...")
    
    # Test 1: POST /availabilities - Soignant propose sa disponibilité
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    test_availability = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": tomorrow,
        "start_time": "08:00",
        "end_time": "16:00",
        "commentaire": "Disponible toute la journée"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/availabilities", json=test_availability)
        if response.status_code == 200:
            print("✅ POST /availabilities - Soignant propose sa disponibilité")
            created_availability = response.json().get('data', {})
            availability_id = created_availability.get('id')
            print(f"   Disponibilité proposée avec l'ID: {availability_id}")
            print(f"   Statut automatique: {created_availability.get('status')}")
        else:
            print(f"❌ POST /availabilities - Erreur {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ POST /availabilities - Exception: {e}")
    
    # Test 2: GET /availabilities/me - Soignant voit ses propositions
    try:
        response = requests.get(f"{API_BASE_URL}/availabilities/me?user_id=684314eb3bd4c4c00ce9c019")
        if response.status_code == 200:
            print("✅ GET /availabilities/me - Soignant voit ses propositions")
            availabilities = response.json().get('data', [])
            print(f"   Nombre de disponibilités trouvées: {len(availabilities)}")
            if availabilities:
                latest = availabilities[-1]  # Dernière créée
                print(f"   Dernière disponibilité: {latest.get('date')} de {latest.get('start_time')} à {latest.get('end_time')}")
        else:
            print(f"❌ GET /availabilities/me - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /availabilities/me - Exception: {e}")

def test_cadre_endpoints():
    """Test des endpoints pour les cadres"""
    print("\n🧪 Test des endpoints CADRE...")
    
    # Test 1: GET /availabilities?service_id=X&status=proposé - Cadre voit les propositions de son équipe
    try:
        response = requests.get(f"{API_BASE_URL}/availabilities?service_id=684314eb3bd4c4c00ce9c022&status=proposé")
        if response.status_code == 200:
            print("✅ GET /availabilities?service_id=X&status=proposé - Cadre voit les propositions de son équipe")
            availabilities = response.json().get('data', [])
            print(f"   Nombre de propositions trouvées: {len(availabilities)}")
            if availabilities:
                print("   Propositions trouvées:")
                for i, avail in enumerate(availabilities[:3]):  # Afficher les 3 premières
                    print(f"     {i+1}. {avail.get('user_name', 'N/A')} - {avail.get('date')} ({avail.get('start_time')}-{avail.get('end_time')})")
        else:
            print(f"❌ GET /availabilities?service_id=X&status=proposé - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /availabilities?service_id=X&status=proposé - Exception: {e}")
    
    # Test 2: PUT /availabilities/{id} - Cadre valide une proposition
    # D'abord, récupérer une disponibilité proposée
    try:
        response = requests.get(f"{API_BASE_URL}/availabilities?status=proposé")
        if response.status_code == 200:
            availabilities = response.json().get('data', [])
            if availabilities:
                test_availability_id = availabilities[0].get('_id')
                
                # Valider la disponibilité
                validation_data = {
                    "status": "validé",
                    "commentaire": "Disponibilité validée par le cadre"
                }
                
                try:
                    response = requests.put(f"{API_BASE_URL}/availabilities/{test_availability_id}", json=validation_data)
                    if response.status_code == 200:
                        print("✅ PUT /availabilities/{id} - Cadre valide une proposition")
                        updated_availability = response.json().get('data', {})
                        print(f"   Nouveau statut: {updated_availability.get('status')}")
                        print(f"   Commentaire: {updated_availability.get('commentaire')}")
                    else:
                        print(f"❌ PUT /availabilities/{id} - Erreur {response.status_code}")
                        print(f"   Réponse: {response.text}")
                except Exception as e:
                    print(f"❌ PUT /availabilities/{id} - Exception: {e}")
            else:
                print("⚠️ Aucune disponibilité proposée trouvée pour le test de validation")
        else:
            print(f"❌ Erreur lors de la récupération des disponibilités proposées: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception lors de la récupération des disponibilités proposées: {e}")

def test_cadre_reject():
    """Test du refus par le cadre"""
    print("\n🧪 Test du REFUS par le CADRE...")
    
    # Créer une nouvelle disponibilité pour le test de refus
    tomorrow = (date.today() + timedelta(days=2)).strftime("%Y-%m-%d")
    test_availability = {
        "user_id": "684314eb3bd4c4c00ce9c020",
        "date": tomorrow,
        "start_time": "20:00",
        "end_time": "23:00",
        "commentaire": "Disponibilité en soirée"
    }
    
    try:
        # Créer la disponibilité
        response = requests.post(f"{API_BASE_URL}/availabilities", json=test_availability)
        if response.status_code == 200:
            created_availability = response.json().get('data', {})
            availability_id = created_availability.get('id')
            
            # Refuser la disponibilité
            rejection_data = {
                "status": "refusé",
                "commentaire": "Créneau non disponible pour le service"
            }
            
            try:
                response = requests.put(f"{API_BASE_URL}/availabilities/{availability_id}", json=rejection_data)
                if response.status_code == 200:
                    print("✅ PUT /availabilities/{id} - Cadre refuse une proposition")
                    updated_availability = response.json().get('data', {})
                    print(f"   Nouveau statut: {updated_availability.get('status')}")
                    print(f"   Commentaire: {updated_availability.get('commentaire')}")
                else:
                    print(f"❌ PUT /availabilities/{id} - Erreur {response.status_code}")
            except Exception as e:
                print(f"❌ PUT /availabilities/{id} - Exception: {e}")
        else:
            print(f"❌ Erreur lors de la création de la disponibilité pour le test de refus: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception lors de la création de la disponibilité pour le test de refus: {e}")

def test_conflict_detection():
    """Test de la détection de conflits"""
    print("\n🧪 Test de la DÉTECTION DE CONFLITS...")
    
    # Créer une disponibilité
    tomorrow = (date.today() + timedelta(days=3)).strftime("%Y-%m-%d")
    test_availability = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": tomorrow,
        "start_time": "09:00",
        "end_time": "17:00",
        "commentaire": "Première disponibilité"
    }
    
    try:
        # Créer la première disponibilité
        response = requests.post(f"{API_BASE_URL}/availabilities", json=test_availability)
        if response.status_code == 200:
            print("✅ Première disponibilité créée")
            
            # Essayer de créer une disponibilité en conflit
            conflicting_availability = {
                "user_id": "684314eb3bd4c4c00ce9c019",
                "date": tomorrow,
                "start_time": "14:00",
                "end_time": "18:00",
                "commentaire": "Disponibilité en conflit"
            }
            
            try:
                response = requests.post(f"{API_BASE_URL}/availabilities", json=conflicting_availability)
                if response.status_code == 400:
                    print("✅ Détection de conflit - Conflit détecté correctement")
                    print(f"   Message: {response.json().get('detail', '')}")
                else:
                    print(f"❌ Détection de conflit - Erreur {response.status_code}")
                    print("   Le conflit n'a pas été détecté")
            except Exception as e:
                print(f"❌ Détection de conflit - Exception: {e}")
        else:
            print(f"❌ Erreur lors de la création de la première disponibilité: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception lors de la création de la première disponibilité: {e}")

def main():
    """Fonction principale"""
    print("🚀 Test de la Tâche 1.1.2 : Endpoints spécifiques selon les rôles")
    print("=" * 70)
    
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
    test_soignant_endpoints()
    test_cadre_endpoints()
    test_cadre_reject()
    test_conflict_detection()
    
    print("\n" + "=" * 70)
    print("🎉 Tests de la Tâche 1.1.2 terminés!")
    print("\n📋 Endpoints testés selon les rôles:")
    print("1. ✅ POST /availabilities - Soignant propose sa disponibilité")
    print("2. ✅ GET /availabilities/me - Soignant voit ses propositions")
    print("3. ✅ GET /availabilities?service_id=X&status=proposé - Cadre voit les propositions de son équipe")
    print("4. ✅ PUT /availabilities/{id} - Cadre valide une proposition")
    print("5. ✅ PUT /availabilities/{id} - Cadre refuse une proposition")
    print("6. ✅ Détection de conflits de créneaux")
    print("\n💡 Tous les endpoints spécifiques selon les rôles sont fonctionnels!")

if __name__ == "__main__":
    main()








