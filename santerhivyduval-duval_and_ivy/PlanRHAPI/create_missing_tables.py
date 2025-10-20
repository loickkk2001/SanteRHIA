#!/usr/bin/env python3
"""
Script pour créer les tables manquantes (alerts, anomalies, events) dans MongoDB
Ce script doit être exécuté une seule fois pour initialiser les collections nécessaires
"""

from pymongo import MongoClient
from datetime import datetime
import os

# Configuration de la base de données
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'planRhIA')

def create_collections():
    """Crée les collections manquantes avec des données d'exemple"""
    
    # Connexion à MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    
    print(f"Connexion à la base de données {DATABASE_NAME}...")
    
    # Créer la collection alerts
    alerts_collection = db['alerts']
    if alerts_collection.count_documents({}) == 0:
        print("Création de la collection 'alerts'...")
        sample_alerts = [
            {
                "title": "Bienvenue dans SAPHIR",
                "message": "Système de gestion des plannings et ressources humaines opérationnel.",
                "type": "info",
                "priority": "low",
                "is_read": False,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        alerts_collection.insert_many(sample_alerts)
        print(f"✓ Collection 'alerts' créée avec {len(sample_alerts)} alertes d'exemple")
    else:
        print("✓ Collection 'alerts' existe déjà")
    
    # Créer la collection anomalies
    anomalies_collection = db['anomalies']
    if anomalies_collection.count_documents({}) == 0:
        print("Création de la collection 'anomalies'...")
        sample_anomalies = [
            {
                "title": "Aucune anomalie détectée",
                "description": "Le système fonctionne normalement.",
                "type": "system",
                "severity": "low",
                "status": "resolved",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        anomalies_collection.insert_many(sample_anomalies)
        print(f"✓ Collection 'anomalies' créée avec {len(sample_anomalies)} anomalies d'exemple")
    else:
        print("✓ Collection 'anomalies' existe déjà")
    
    # Créer la collection events
    events_collection = db['events']
    if events_collection.count_documents({}) == 0:
        print("Création de la collection 'events'...")
        sample_events = [
            {
                "title": "Formation SAPHIR",
                "description": "Formation à l'utilisation du système SAPHIR pour le personnel.",
                "type": "training",
                "status": "pending",
                "due_date": (datetime.now().replace(day=datetime.now().day + 7)).isoformat(),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "title": "Réunion mensuelle RH",
                "description": "Réunion mensuelle avec l'équipe des ressources humaines.",
                "type": "meeting",
                "status": "pending",
                "due_date": (datetime.now().replace(day=datetime.now().day + 14)).isoformat(),
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        events_collection.insert_many(sample_events)
        print(f"✓ Collection 'events' créée avec {len(sample_events)} événements d'exemple")
    else:
        print("✓ Collection 'events' existe déjà")
    
    # Créer la collection notifications
    notifications_collection = db['notifications']
    if notifications_collection.count_documents({}) == 0:
        print("Création de la collection 'notifications'...")
        sample_notifications = [
            {
                "title": "Nouvelle alerte détectée",
                "message": "Une anomalie de planning a été détectée dans votre service",
                "type": "warning",
                "priority": "high",
                "category": "alert",
                "user_id": "684314eb3bd4c4c00ce9c019",
                "read": False,
                "created_at": datetime.now().isoformat(),
                "action_url": "/sec/alerts",
                "action_label": "Voir les alertes"
            },
            {
                "title": "Alerte critique",
                "message": "Sous-effectif critique détecté - Action immédiate requise",
                "type": "error",
                "priority": "critical",
                "category": "anomaly",
                "user_id": "684314eb3bd4c4c00ce9c019",
                "read": False,
                "created_at": datetime.now().isoformat(),
                "action_url": "/cadre/anomalies",
                "action_label": "Gérer les anomalies"
            },
            {
                "title": "Événement à venir",
                "message": "Formation sécurité prévue demain à 9h",
                "type": "info",
                "priority": "medium",
                "category": "event",
                "user_id": "684314eb3bd4c4c00ce9c019",
                "read": True,
                "created_at": datetime.now().isoformat(),
                "action_url": "/sec/calendar",
                "action_label": "Voir le calendrier"
            }
        ]
        notifications_collection.insert_many(sample_notifications)
        print(f"✓ Collection 'notifications' créée avec {len(sample_notifications)} notifications d'exemple")
    else:
        print("✓ Collection 'notifications' existe déjà")
    
    # Créer les index pour améliorer les performances
    print("Création des index...")
    
    # Index pour alerts
    alerts_collection.create_index("user_id")
    alerts_collection.create_index("service_id")
    alerts_collection.create_index("is_read")
    alerts_collection.create_index("created_at")
    
    # Index pour anomalies
    anomalies_collection.create_index("user_id")
    anomalies_collection.create_index("service_id")
    anomalies_collection.create_index("type")
    anomalies_collection.create_index("status")
    anomalies_collection.create_index("created_at")
    
    # Index pour events
    events_collection.create_index("user_id")
    events_collection.create_index("service_id")
    events_collection.create_index("type")
    events_collection.create_index("status")
    events_collection.create_index("due_date")
    events_collection.create_index("created_at")
    
    # Index pour notifications
    notifications_collection.create_index("user_id")
    notifications_collection.create_index("read")
    notifications_collection.create_index("created_at")
    notifications_collection.create_index([("user_id", 1), ("read", 1)])
    
    print("✓ Index créés avec succès")
    
    client.close()
    print("\n🎉 Initialisation terminée ! Les pages d'accueil devraient maintenant fonctionner correctement.")

if __name__ == "__main__":
    try:
        create_collections()
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        print("Vérifiez que MongoDB est démarré et accessible.")
