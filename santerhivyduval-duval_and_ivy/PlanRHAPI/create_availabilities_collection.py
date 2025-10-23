#!/usr/bin/env python3
"""
Script pour créer la collection "availabilities" dans MongoDB
Ce script doit être exécuté une seule fois pour initialiser la collection des disponibilités
"""

from pymongo import MongoClient
from datetime import datetime, date, timedelta
import os

# Configuration de la base de données
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'planRhIA')

def create_availabilities_collection():
    """Crée la collection availabilities avec des données d'exemple"""
    
    # Connexion à MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    
    print(f"Connexion à la base de données {DATABASE_NAME}...")
    
    # Créer la collection availabilities
    availabilities_collection = db['availabilities']
    if availabilities_collection.count_documents({}) == 0:
        print("Création de la collection 'availabilities'...")
        
        # Générer des disponibilités d'exemple pour les prochains jours
        sample_availabilities = []
        today = date.today()
        
        # Disponibilités d'exemple pour différents utilisateurs
        user_ids = ["684314eb3bd4c4c00ce9c019", "684314eb3bd4c4c00ce9c020", "684314eb3bd4c4c00ce9c021"]
        
        for i in range(7):  # 7 jours de disponibilités
            current_date = today + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")
            
            for j, user_id in enumerate(user_ids):
                # Créer des créneaux différents pour chaque utilisateur
                if j == 0:  # Premier utilisateur - matin
                    start_time = "08:00"
                    end_time = "12:00"
                    status = "proposé"
                elif j == 1:  # Deuxième utilisateur - après-midi
                    start_time = "13:00"
                    end_time = "17:00"
                    status = "validé"
                else:  # Troisième utilisateur - soir
                    start_time = "18:00"
                    end_time = "22:00"
                    status = "proposé"
                
                availability = {
                    "user_id": user_id,
                    "date": date_str,
                    "start_time": start_time,
                    "end_time": end_time,
                    "status": status,
                    "commentaire": f"Disponibilité {status} pour le {date_str}",
                    "created_at": datetime.now(),
                    "updated_at": datetime.now()
                }
                sample_availabilities.append(availability)
        
        availabilities_collection.insert_many(sample_availabilities)
        print(f"✓ Collection 'availabilities' créée avec {len(sample_availabilities)} disponibilités d'exemple")
    else:
        print("✓ Collection 'availabilities' existe déjà")
    
    # Créer les index pour améliorer les performances
    print("Création des index pour la collection availabilities...")
    
    # Index pour les requêtes fréquentes
    availabilities_collection.create_index("user_id")
    availabilities_collection.create_index("date")
    availabilities_collection.create_index("status")
    availabilities_collection.create_index("created_at")
    
    # Index composé pour les requêtes complexes
    availabilities_collection.create_index([("user_id", 1), ("date", 1)])
    availabilities_collection.create_index([("date", 1), ("status", 1)])
    availabilities_collection.create_index([("user_id", 1), ("status", 1)])
    
    print("✓ Index créés avec succès")
    
    # Afficher quelques statistiques
    total_count = availabilities_collection.count_documents({})
    proposed_count = availabilities_collection.count_documents({"status": "proposé"})
    validated_count = availabilities_collection.count_documents({"status": "validé"})
    refused_count = availabilities_collection.count_documents({"status": "refusé"})
    
    print(f"\n📊 Statistiques de la collection availabilities:")
    print(f"   Total: {total_count}")
    print(f"   Proposées: {proposed_count}")
    print(f"   Validées: {validated_count}")
    print(f"   Refusées: {refused_count}")
    
    client.close()
    print("\n🎉 Initialisation de la collection availabilities terminée !")

if __name__ == "__main__":
    try:
        create_availabilities_collection()
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        print("Vérifiez que MongoDB est démarré et accessible.")








