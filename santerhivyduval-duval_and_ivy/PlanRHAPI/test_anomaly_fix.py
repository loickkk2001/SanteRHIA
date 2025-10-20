#!/usr/bin/env python3
"""
Script de test pour vérifier les corrections des anomalies
"""

import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"
ANOMALY_ID = "test_anomaly_id"  # Remplacez par un ID réel

def test_anomaly_endpoints():
    """Test des endpoints d'anomalies"""
    print("🧪 Test des endpoints d'anomalies...")
    
    # Test 1: Récupérer toutes les anomalies
    try:
        response = requests.get(f"{API_BASE_URL}/anomalies")
        if response.status_code == 200:
            print("✅ GET /anomalies - OK")
            anomalies = response.json().get('data', [])
            print(f"   Nombre d'anomalies trouvées: {len(anomalies)}")
        else:
            print(f"❌ GET /anomalies - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /anomalies - Exception: {e}")
    
    # Test 2: Créer une anomalie de test
    test_anomaly = {
        "title": "Test anomalie - Conflit de planning",
        "description": "Test de création d'anomalie pour vérifier les corrections",
        "type": "schedule_conflict",
        "severity": "major",
        "status": "detected",
        "user_id": "test_user",
        "service_id": "test_service",
        "detected_at": datetime.now().isoformat()
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/detection/create-anomaly", json=test_anomaly)
        if response.status_code == 200:
            print("✅ POST /detection/create-anomaly - OK")
            created_anomaly = response.json().get('data', {})
            anomaly_id = created_anomaly.get('_id')
            print(f"   Anomalie créée avec l'ID: {anomaly_id}")
            
            # Test 3: Mettre à jour l'anomalie
            if anomaly_id:
                update_data = {
                    "status": "resolved",
                    "comment": "Test de résolution d'anomalie",
                    "resolved_at": datetime.now().isoformat(),
                    "resolved_by": "test_user"
                }
                
                try:
                    response = requests.patch(f"{API_BASE_URL}/anomalies/{anomaly_id}", json=update_data)
                    if response.status_code == 200:
                        print("✅ PATCH /anomalies/{id} - OK")
                        updated_anomaly = response.json().get('data', {})
                        print(f"   Statut mis à jour: {updated_anomaly.get('status')}")
                    else:
                        print(f"❌ PATCH /anomalies/{id} - Erreur {response.status_code}")
                        print(f"   Réponse: {response.text}")
                except Exception as e:
                    print(f"❌ PATCH /anomalies/{id} - Exception: {e}")
        else:
            print(f"❌ POST /detection/create-anomaly - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ POST /detection/create-anomaly - Exception: {e}")

def test_alert_endpoints():
    """Test des endpoints d'alertes"""
    print("\n🧪 Test des endpoints d'alertes...")
    
    # Test 1: Récupérer toutes les alertes
    try:
        response = requests.get(f"{API_BASE_URL}/alerts")
        if response.status_code == 200:
            print("✅ GET /alerts - OK")
            alerts = response.json().get('data', [])
            print(f"   Nombre d'alertes trouvées: {len(alerts)}")
        else:
            print(f"❌ GET /alerts - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ GET /alerts - Exception: {e}")
    
    # Test 2: Créer une alerte de test
    test_alert = {
        "title": "Test alerte - Absence non justifiée",
        "message": "Test de création d'alerte pour vérifier les corrections",
        "type": "warning",
        "priority": "high",
        "auto_generated": True,
        "user_id": "test_user",
        "service_id": "test_service",
        "status": "new"
    }
    
    try:
        response = requests.post(f"{API_BASE_URL}/detection/create-alert", json=test_alert)
        if response.status_code == 200:
            print("✅ POST /detection/create-alert - OK")
            created_alert = response.json().get('data', {})
            alert_id = created_alert.get('_id')
            print(f"   Alerte créée avec l'ID: {alert_id}")
            
            # Test 3: Mettre à jour l'alerte
            if alert_id:
                update_data = {
                    "status": "resolved",
                    "comment": "Test de résolution d'alerte",
                    "resolved_at": datetime.now().isoformat(),
                    "resolved_by": "test_user"
                }
                
                try:
                    response = requests.patch(f"{API_BASE_URL}/alerts/{alert_id}", json=update_data)
                    if response.status_code == 200:
                        print("✅ PATCH /alerts/{id} - OK")
                        updated_alert = response.json().get('data', {})
                        print(f"   Statut mis à jour: {updated_alert.get('status')}")
                    else:
                        print(f"❌ PATCH /alerts/{id} - Erreur {response.status_code}")
                        print(f"   Réponse: {response.text}")
                except Exception as e:
                    print(f"❌ PATCH /alerts/{id} - Exception: {e}")
        else:
            print(f"❌ POST /detection/create-alert - Erreur {response.status_code}")
    except Exception as e:
        print(f"❌ POST /detection/create-alert - Exception: {e}")

def main():
    """Fonction principale"""
    print("🚀 Test des corrections des anomalies et alertes")
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
    test_anomaly_endpoints()
    test_alert_endpoints()
    
    print("\n" + "=" * 50)
    print("🎉 Tests terminés!")
    print("\n📋 Résumé des corrections apportées:")
    print("1. ✅ Ajout de l'endpoint PATCH /anomalies/{id} pour mettre à jour les anomalies")
    print("2. ✅ Ajout de l'endpoint GET /anomalies/{id} pour récupérer une anomalie spécifique")
    print("3. ✅ Ajout de l'endpoint PATCH /alerts/{id} pour mettre à jour les alertes")
    print("4. ✅ Ajout de l'endpoint GET /alerts/{id} pour récupérer une alerte spécifique")
    print("5. ✅ Correction de la logique de création pour éviter la duplication alertes/anomalies")
    print("6. ✅ Amélioration de la gestion des erreurs dans le frontend (anomalies et alertes)")

if __name__ == "__main__":
    main()
