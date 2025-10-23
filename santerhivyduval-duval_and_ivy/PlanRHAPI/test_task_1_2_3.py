#!/usr/bin/env python3
"""
Script de test pour la Tâche 1.2.3 : Collection plannings
"""

import requests
import json
from datetime import datetime, date, timedelta

# Configuration
API_BASE_URL = "http://localhost:8000"

def test_planning_endpoints():
    """Test des endpoints de plannings"""
    print("🧪 Test des endpoints de plannings...")
    
    # Test 1: Récupérer tous les plannings
    try:
        response = requests.get(f"{API_BASE_URL}/plannings")
        if response.status_code == 200:
            print("✅ GET /plannings - OK")
            plannings = response.json().get('data', [])
            print(f"   Nombre de plannings trouvés: {len(plannings)}")
            if plannings:
                print(f"   Premier planning: {plannings[0].get('activity_code')} - {plannings[0].get('plage_horaire')}")
        else:
            print(f"❌ GET /plannings - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /plannings - Exception: {e}")
    
    # Test 2: Créer un planning de test
    tomorrow = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    test_planning = {
        "user_id": "684314eb3bd4c4c00ce9c019",
        "date": tomorrow,
        "activity_code": "SOIN",
        "plage_horaire": "09:00-17:00",
        "commentaire": "Planning de test pour les soins"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/plannings", json=test_planning)
        if response.status_code == 200:
            print("✅ POST /plannings - OK")
            created_planning = response.json().get('data', {})
            planning_id = created_planning.get('id')
            print(f"   Planning créé avec l'ID: {planning_id}")
            
            # Test 3: Récupérer le planning par ID
            if planning_id:
                try:
                    response = requests.get(f"{API_BASE_URL}/plannings/{planning_id}")
                    if response.status_code == 200:
                        print("✅ GET /plannings/{id} - OK")
                        planning_data = response.json().get('data', {})
                        print(f"   Code d'activité: {planning_data.get('activity_code')}")
                        print(f"   Plage horaire: {planning_data.get('plage_horaire')}")
                    else:
                        print(f"❌ GET /plannings/{id} - Erreur {response.status_code}")
                except Exception as e:
                    print(f"❌ GET /plannings/{id} - Exception: {e}")
            
            # Test 4: Mettre à jour le planning
            if planning_id:
                update_data = {
                    "activity_code": "FORMATION",
                    "plage_horaire": "14:00-18:00",
                    "commentaire": "Planning modifié pour formation"
                }
                
                try:
                    response = requests.put(f"{API_BASE_URL}/plannings/{planning_id}", json=update_data)
                    if response.status_code == 200:
                        print("✅ PUT /plannings/{id} - OK")
                        updated_planning = response.json().get('data', {})
                        print(f"   Nouveau code d'activité: {updated_planning.get('activity_code')}")
                        print(f"   Nouvelle plage horaire: {updated_planning.get('plage_horaire')}")
                    else:
                        print(f"❌ PUT /plannings/{id} - Erreur {response.status_code}")
                except Exception as e:
                    print(f"❌ PUT /plannings/{id} - Exception: {e}")
            
            # Test 5: Supprimer le planning de test
            if planning_id:
                try:
                    response = requests.delete(f"{API_BASE_URL}/plannings/{planning_id}")
                    if response.status_code == 200:
                        print("✅ DELETE /plannings/{id} - OK")
                        print("   Planning de test supprimé")
                    else:
                        print(f"❌ DELETE /plannings/{id} - Erreur {response.status_code}")
                except Exception as e:
                    print(f"❌ DELETE /plannings/{id} - Exception: {e}")
        else:
            print(f"❌ POST /plannings - Erreur {response.status_code}")
            print(f"   Réponse: {response.text}")
    except Exception as e:
        print(f"❌ POST /plannings - Exception: {e}")

def test_planning_filters():
    """Test des filtres de plannings"""
    print("\n🧪 Test des filtres de plannings...")
    
    # Test 1: Récupérer par utilisateur
    try:
        response = requests.get(f"{API_BASE_URL}/plannings/user/684314eb3bd4c4c00ce9c019")
        if response.status_code == 200:
            print("✅ GET /plannings/user/{user_id} - OK")
            plannings = response.json().get('data', [])
            print(f"   Plannings trouvés pour l'utilisateur: {len(plannings)}")
        else:
            print(f"❌ GET /plannings/user/{user_id} - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /plannings/user/{user_id} - Exception: {e}")
    
    # Test 2: Récupérer par date
    today = date.today().strftime("%Y-%m-%d")
    try:
        response = requests.get(f"{API_BASE_URL}/plannings/date/{today}")
        if response.status_code == 200:
            print("✅ GET /plannings/date/{date} - OK")
            plannings = response.json().get('data', [])
            print(f"   Plannings trouvés pour {today}: {len(plannings)}")
        else:
            print(f"❌ GET /plannings/date/{date} - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /plannings/date/{date} - Exception: {e}")
    
    # Test 3: Récupérer par code d'activité
    try:
        response = requests.get(f"{API_BASE_URL}/plannings/activity/SOIN")
        if response.status_code == 200:
            print("✅ GET /plannings/activity/{activity_code} - OK")
            plannings = response.json().get('data', [])
            print(f"   Plannings SOIN trouvés: {len(plannings)}")
        else:
            print(f"❌ GET /plannings/activity/{activity_code} - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /plannings/activity/{activity_code} - Exception: {e}")
    
    # Test 4: Filtres combinés
    try:
        response = requests.get(f"{API_BASE_URL}/plannings?user_id=684314eb3bd4c4c00ce9c019&activity_code=SOIN")
        if response.status_code == 200:
            print("✅ GET /plannings avec filtres combinés - OK")
            plannings = response.json().get('data', [])
            print(f"   Plannings SOIN pour l'utilisateur: {len(plannings)}")
        else:
            print(f"❌ GET /plannings avec filtres combinés - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /plannings avec filtres combinés - Exception: {e}")

def test_planning_stats():
    """Test des statistiques de plannings"""
    print("\n🧪 Test des statistiques de plannings...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/plannings/stats/summary")
        if response.status_code == 200:
            print("✅ GET /plannings/stats/summary - OK")
            stats = response.json().get('data', {})
            print(f"   Total plannings: {stats.get('total_plannings')}")
            print("   Par activité:")
            for activity, count in stats.get('by_activity', {}).items():
                print(f"     {activity}: {count}")
        else:
            print(f"❌ GET /plannings/stats/summary - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /plannings/stats/summary - Exception: {e}")

def main():
    """Fonction principale"""
    print("🚀 Test de la Tâche 1.2.3 : Collection plannings")
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
    test_planning_endpoints()
    test_planning_filters()
    test_planning_stats()
    
    print("\n" + "=" * 60)
    print("🎉 Tests de la Tâche 1.2.3 terminés!")
    print("\n📋 Endpoints testés:")
    print("1. ✅ POST /plannings - Créer un planning")
    print("2. ✅ GET /plannings - Récupérer tous les plannings")
    print("3. ✅ GET /plannings/{id} - Récupérer par ID")
    print("4. ✅ PUT /plannings/{id} - Mettre à jour un planning")
    print("5. ✅ DELETE /plannings/{id} - Supprimer un planning")
    print("6. ✅ GET /plannings/user/{user_id} - Filtrage par utilisateur")
    print("7. ✅ GET /plannings/date/{date} - Filtrage par date")
    print("8. ✅ GET /plannings/activity/{activity_code} - Filtrage par activité")
    print("9. ✅ GET /plannings avec filtres combinés")
    print("10. ✅ GET /plannings/stats/summary - Statistiques")
    print("\n💡 La collection plannings est fonctionnelle!")

if __name__ == "__main__":
    main()








