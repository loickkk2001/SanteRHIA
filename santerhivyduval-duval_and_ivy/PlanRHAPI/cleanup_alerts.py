#!/usr/bin/env python3
"""
Script pour nettoyer les alertes et anomalies en surplus
"""

import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"

def clean_alerts_and_anomalies():
    """Nettoie les alertes et anomalies en surplus"""
    print("🧹 Nettoyage des alertes et anomalies...")
    
    # 1. Récupérer toutes les alertes
    try:
        response = requests.get(f"{API_BASE_URL}/alerts")
        if response.status_code == 200:
            alerts = response.json().get('data', [])
            print(f"📊 Nombre d'alertes trouvées: {len(alerts)}")
            
            # Garder seulement les 5 alertes les plus récentes
            if len(alerts) > 5:
                # Trier par date de création (plus récentes en premier)
                alerts_sorted = sorted(alerts, key=lambda x: x.get('created_at', ''), reverse=True)
                alerts_to_keep = alerts_sorted[:5]
                alerts_to_delete = alerts_sorted[5:]
                
                print(f"🗑️ Suppression de {len(alerts_to_delete)} alertes anciennes...")
                
                # Supprimer les alertes anciennes
                for alert in alerts_to_delete:
                    try:
                        alert_id = alert.get('_id')
                        if alert_id:
                            delete_response = requests.delete(f"{API_BASE_URL}/alerts/{alert_id}")
                            if delete_response.status_code == 200:
                                print(f"   ✅ Supprimé: {alert.get('title', 'Sans titre')}")
                            else:
                                print(f"   ❌ Erreur suppression: {delete_response.status_code}")
                    except Exception as e:
                        print(f"   ❌ Erreur suppression alerte: {e}")
                
                print(f"✅ Gardé {len(alerts_to_keep)} alertes récentes")
            else:
                print("✅ Nombre d'alertes acceptable")
        else:
            print(f"❌ Erreur récupération alertes: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception récupération alertes: {e}")
    
    # 2. Récupérer toutes les anomalies
    try:
        response = requests.get(f"{API_BASE_URL}/anomalies")
        if response.status_code == 200:
            anomalies = response.json().get('data', [])
            print(f"📊 Nombre d'anomalies trouvées: {len(anomalies)}")
            
            # Garder seulement les 10 anomalies les plus récentes
            if len(anomalies) > 10:
                # Trier par date de détection (plus récentes en premier)
                anomalies_sorted = sorted(anomalies, key=lambda x: x.get('detected_at', ''), reverse=True)
                anomalies_to_keep = anomalies_sorted[:10]
                anomalies_to_delete = anomalies_sorted[10:]
                
                print(f"🗑️ Suppression de {len(anomalies_to_delete)} anomalies anciennes...")
                
                # Supprimer les anomalies anciennes
                for anomaly in anomalies_to_delete:
                    try:
                        anomaly_id = anomaly.get('_id')
                        if anomaly_id:
                            delete_response = requests.delete(f"{API_BASE_URL}/anomalies/{anomaly_id}")
                            if delete_response.status_code == 200:
                                print(f"   ✅ Supprimé: {anomaly.get('title', 'Sans titre')}")
                            else:
                                print(f"   ❌ Erreur suppression: {delete_response.status_code}")
                    except Exception as e:
                        print(f"   ❌ Erreur suppression anomalie: {e}")
                
                print(f"✅ Gardé {len(anomalies_to_keep)} anomalies récentes")
            else:
                print("✅ Nombre d'anomalies acceptable")
        else:
            print(f"❌ Erreur récupération anomalies: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception récupération anomalies: {e}")

def check_system_status():
    """Vérifie le statut du système après nettoyage"""
    print("\n🔍 Vérification du statut du système...")
    
    try:
        # Vérifier les alertes
        response = requests.get(f"{API_BASE_URL}/alerts")
        if response.status_code == 200:
            alerts_count = len(response.json().get('data', []))
            print(f"📊 Alertes restantes: {alerts_count}")
        
        # Vérifier les anomalies
        response = requests.get(f"{API_BASE_URL}/anomalies")
        if response.status_code == 200:
            anomalies_count = len(response.json().get('data', []))
            print(f"📊 Anomalies restantes: {anomalies_count}")
            
    except Exception as e:
        print(f"❌ Erreur vérification statut: {e}")

def main():
    """Fonction principale"""
    print("🚀 Nettoyage du système d'alertes et anomalies")
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
    
    # Nettoyer les données
    clean_alerts_and_anomalies()
    
    # Vérifier le statut après nettoyage
    check_system_status()
    
    print("\n" + "=" * 60)
    print("🎉 Nettoyage terminé!")
    print("\n📋 Actions effectuées:")
    print("1. ✅ Surveillance automatique désactivée")
    print("2. ✅ Règles de détection désactivées par défaut")
    print("3. ✅ Endpoints DELETE ajoutés au backend")
    print("4. ✅ Nettoyage des alertes/anomalies en surplus")
    print("5. ✅ Vérification du statut du système")
    print("\n💡 Le système est maintenant propre et contrôlé!")

if __name__ == "__main__":
    main()
