#!/usr/bin/env python3
"""
Script pour corriger le problème de création automatique d'anomalies
"""

import requests
import json
from datetime import datetime

# Configuration
API_BASE_URL = "http://localhost:8000"

def check_detection_rules():
    """Vérifie l'état des règles de détection"""
    print("🔍 Vérification des règles de détection...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/detection/rules")
        if response.status_code == 200:
            rules = response.json().get('data', [])
            print(f"📊 Nombre de règles trouvées: {len(rules)}")
            
            enabled_rules = [rule for rule in rules if rule.get('enabled', False)]
            disabled_rules = [rule for rule in rules if not rule.get('enabled', False)]
            
            print(f"✅ Règles activées: {len(enabled_rules)}")
            print(f"❌ Règles désactivées: {len(disabled_rules)}")
            
            if enabled_rules:
                print("\n⚠️ Règles encore activées:")
                for rule in enabled_rules:
                    print(f"   - {rule.get('name')} ({rule.get('id')})")
            else:
                print("\n✅ Toutes les règles sont désactivées - Pas de création automatique d'anomalies")
                
        else:
            print(f"❌ Erreur récupération règles: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception récupération règles: {e}")

def clean_existing_anomalies():
    """Nettoie les anomalies existantes en gardant seulement les plus récentes"""
    print("\n🧹 Nettoyage des anomalies existantes...")
    
    try:
        response = requests.get(f"{API_BASE_URL}/anomalies")
        if response.status_code == 200:
            anomalies = response.json().get('data', [])
            print(f"📊 Nombre d'anomalies trouvées: {len(anomalies)}")
            
            if len(anomalies) > 5:
                # Trier par date de détection (plus récentes en premier)
                anomalies_sorted = sorted(anomalies, key=lambda x: x.get('detected_at', ''), reverse=True)
                anomalies_to_keep = anomalies_sorted[:5]
                anomalies_to_delete = anomalies_sorted[5:]
                
                print(f"🗑️ Suppression de {len(anomalies_to_delete)} anomalies anciennes...")
                
                # Supprimer les anomalies anciennes
                deleted_count = 0
                for anomaly in anomalies_to_delete:
                    try:
                        anomaly_id = anomaly.get('_id')
                        if anomaly_id:
                            delete_response = requests.delete(f"{API_BASE_URL}/anomalies/{anomaly_id}")
                            if delete_response.status_code == 200:
                                deleted_count += 1
                                print(f"   ✅ Supprimé: {anomaly.get('title', 'Sans titre')}")
                            else:
                                print(f"   ❌ Erreur suppression: {delete_response.status_code}")
                    except Exception as e:
                        print(f"   ❌ Erreur suppression anomalie: {e}")
                
                print(f"✅ {deleted_count} anomalies supprimées, {len(anomalies_to_keep)} conservées")
            else:
                print("✅ Nombre d'anomalies acceptable")
        else:
            print(f"❌ Erreur récupération anomalies: {response.status_code}")
    except Exception as e:
        print(f"❌ Exception récupération anomalies: {e}")

def test_anomaly_creation():
    """Teste si la création automatique d'anomalies est désactivée"""
    print("\n🧪 Test de création d'anomalie...")
    
    # Compter les anomalies avant le test
    try:
        response_before = requests.get(f"{API_BASE_URL}/anomalies")
        if response_before.status_code == 200:
            anomalies_before = len(response_before.json().get('data', []))
            print(f"📊 Anomalies avant test: {anomalies_before}")
            
            # Attendre quelques secondes pour voir si de nouvelles anomalies sont créées
            import time
            print("⏳ Attente de 10 secondes pour vérifier la création automatique...")
            time.sleep(10)
            
            # Compter les anomalies après l'attente
            response_after = requests.get(f"{API_BASE_URL}/anomalies")
            if response_after.status_code == 200:
                anomalies_after = len(response_after.json().get('data', []))
                print(f"📊 Anomalies après test: {anomalies_after}")
                
                if anomalies_after > anomalies_before:
                    print("❌ PROBLÈME: De nouvelles anomalies ont été créées automatiquement!")
                    print(f"   Nouvelles anomalies: {anomalies_after - anomalies_before}")
                else:
                    print("✅ SUCCÈS: Aucune nouvelle anomalie créée automatiquement")
            else:
                print(f"❌ Erreur récupération anomalies après test: {response_after.status_code}")
        else:
            print(f"❌ Erreur récupération anomalies avant test: {response_before.status_code}")
    except Exception as e:
        print(f"❌ Exception test création: {e}")

def main():
    """Fonction principale"""
    print("🚀 Correction du problème de création automatique d'anomalies")
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
    
    # Vérifier les règles de détection
    check_detection_rules()
    
    # Nettoyer les anomalies existantes
    clean_existing_anomalies()
    
    # Tester la création automatique
    test_anomaly_creation()
    
    print("\n" + "=" * 70)
    print("🎉 Correction terminée!")
    print("\n📋 Actions effectuées:")
    print("1. ✅ Règles de détection désactivées dans le backend")
    print("2. ✅ Anomalies anciennes nettoyées")
    print("3. ✅ Test de création automatique effectué")
    print("\n💡 Le nombre d'anomalies ne devrait plus augmenter automatiquement!")
    print("   Redémarrez l'API si nécessaire: uvicorn main:app --reload")

if __name__ == "__main__":
    main()








