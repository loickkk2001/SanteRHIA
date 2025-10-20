#!/usr/bin/env python3
"""
Script pour créer la collection "plannings" dans MongoDB
Ce script doit être exécuté une seule fois pour initialiser la collection des plannings validés
"""

from pymongo import MongoClient
from datetime import datetime, date, timedelta
import os

# Configuration de la base de données
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'planRhIA')

def create_plannings_collection():
    """Crée la collection plannings avec des données d'exemple"""
    
    # Connexion à MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    
    print(f"Connexion à la base de données {DATABASE_NAME}...")
    
    # Créer la collection plannings
    plannings_collection = db['plannings']
    if plannings_collection.count_documents({}) == 0:
        print("Création de la collection 'plannings'...")
        
        # Générer des plannings d'exemple pour les prochains jours
        sample_plannings = []
        today = date.today()
        
        # Plannings d'exemple pour différents utilisateurs
        user_ids = ["684314eb3bd4c4c00ce9c019", "684314eb3bd4c4c00ce9c020", "684314eb3bd4c4c00ce9c021"]
        
        # Codes d'activité disponibles
        activity_codes = ["SOIN", "CONGÉ", "REPOS", "FORMATION", "ADMINISTRATIF"]
        
        # Plages horaires typiques
        time_slots = [
            ("08:00-12:00", "Matin"),
            ("13:00-17:00", "Après-midi"),
            ("18:00-22:00", "Soir"),
            ("08:00-17:00", "Journée complète"),
            ("20:00-08:00", "Nuit")
        ]
        
        for i in range(14):  # 14 jours de plannings
            current_date = today + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")
            
            for j, user_id in enumerate(user_ids):
                # Créer des plannings différents pour chaque utilisateur
                if j == 0:  # Premier utilisateur - Soins
                    activity_code = "SOIN"
                    plage_horaire, description = time_slots[0]  # Matin
                elif j == 1:  # Deuxième utilisateur - Formation
                    activity_code = "FORMATION"
                    plage_horaire, description = time_slots[1]  # Après-midi
                else:  # Troisième utilisateur - Repos
                    activity_code = "REPOS"
                    plage_horaire, description = time_slots[2]  # Soir
                
                # Ajouter quelques variations
                if i % 3 == 0 and j == 0:  # Congé pour le premier utilisateur
                    activity_code = "CONGÉ"
                    plage_horaire, description = time_slots[3]  # Journée complète
                elif i % 5 == 0 and j == 1:  # Administratif pour le deuxième utilisateur
                    activity_code = "ADMINISTRATIF"
                    plage_horaire, description = time_slots[0]  # Matin
                
                planning = {
                    "user_id": user_id,
                    "date": date_str,
                    "activity_code": activity_code,
                    "plage_horaire": plage_horaire,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "validated_by": "684314eb3bd4c4c00ce9c022",  # ID d'un cadre
                    "commentaire": f"Planning {activity_code} - {description} pour le {date_str}"
                }
                sample_plannings.append(planning)
        
        plannings_collection.insert_many(sample_plannings)
        print(f"✓ Collection 'plannings' créée avec {len(sample_plannings)} plannings d'exemple")
    else:
        print("✓ Collection 'plannings' existe déjà")
    
    # Créer les index pour améliorer les performances
    print("Création des index pour la collection plannings...")
    
    # Index pour les requêtes fréquentes
    plannings_collection.create_index("user_id")
    plannings_collection.create_index("date")
    plannings_collection.create_index("activity_code")
    plannings_collection.create_index("plage_horaire")
    plannings_collection.create_index("created_at")
    plannings_collection.create_index("validated_by")
    
    # Index composé pour les requêtes complexes
    plannings_collection.create_index([("user_id", 1), ("date", 1)])
    plannings_collection.create_index([("date", 1), ("activity_code", 1)])
    plannings_collection.create_index([("user_id", 1), ("activity_code", 1)])
    plannings_collection.create_index([("date", 1), ("plage_horaire", 1)])
    
    print("✓ Index créés avec succès")
    
    # Afficher quelques statistiques
    total_count = plannings_collection.count_documents({})
    
    # Statistiques par code d'activité
    activity_stats = {}
    activities = ["SOIN", "CONGÉ", "REPOS", "FORMATION", "ADMINISTRATIF"]
    
    for activity in activities:
        count = plannings_collection.count_documents({"activity_code": activity})
        activity_stats[activity] = count
    
    # Statistiques par utilisateur
    user_stats = {}
    for user_id in user_ids:
        count = plannings_collection.count_documents({"user_id": user_id})
        user_stats[user_id] = count
    
    print(f"\n📊 Statistiques de la collection plannings:")
    print(f"   Total: {total_count}")
    print(f"   Par activité:")
    for activity, count in activity_stats.items():
        print(f"     {activity}: {count}")
    print(f"   Par utilisateur:")
    for user_id, count in user_stats.items():
        print(f"     {user_id}: {count}")
    
    client.close()
    print("\n🎉 Initialisation de la collection plannings terminée !")

if __name__ == "__main__":
    try:
        create_plannings_collection()
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        print("Vérifiez que MongoDB est démarré et accessible.")





