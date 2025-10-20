from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from typing import List, Optional
from datetime import datetime
import os
from pymongo import MongoClient
from schemas.planning import PlanningCreate, PlanningUpdate

# Configuration de la base de données
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
DATABASE_NAME = os.getenv('DATABASE_NAME', 'planRhIA')

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Collection des plannings
plannings = db['plannings']

router = APIRouter()

# =============================================================================
# ENDPOINTS CRUD POUR LES PLANNINGS VALIDÉS - TÂCHE 1.2.3
# =============================================================================

@router.post("/plannings")
async def create_planning(planning_data: PlanningCreate):
    """
    POST /plannings
    Crée un planning validé
    """
    try:
        # Préparer les données avec timestamps
        planning_dict = planning_data.dict()
        planning_dict["created_at"] = datetime.now()
        planning_dict["updated_at"] = datetime.now()
        
        # Vérifier qu'il n'y a pas de conflit de créneaux pour le même utilisateur et la même date
        existing = plannings.find_one({
            "user_id": planning_dict["user_id"],
            "date": planning_dict["date"],
            "plage_horaire": planning_dict["plage_horaire"]
        })
        
        if existing:
            raise HTTPException(
                status_code=400, 
                detail="Un planning existe déjà pour ce créneau horaire"
            )
        
        # Insérer dans MongoDB
        result = plannings.insert_one(planning_dict)
        
        return {
            "message": "Planning créé avec succès",
            "data": {
                "id": str(result.inserted_id),
                "user_id": planning_dict["user_id"],
                "date": planning_dict["date"],
                "activity_code": planning_dict["activity_code"],
                "plage_horaire": planning_dict["plage_horaire"],
                "created_at": planning_dict["created_at"].isoformat()
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création: {str(e)}")

@router.get("/plannings")
async def get_all_plannings(
    user_id: Optional[str] = Query(None, description="ID de l'utilisateur"),
    date: Optional[str] = Query(None, description="Date spécifique (YYYY-MM-DD)"),
    activity_code: Optional[str] = Query(None, description="Code d'activité"),
    service_id: Optional[str] = Query(None, description="ID du service")
):
    """
    GET /plannings
    Récupère les plannings avec filtres optionnels
    """
    try:
        # Construire le filtre de requête
        query_filter = {}
        
        if user_id:
            query_filter["user_id"] = user_id
        
        if date:
            query_filter["date"] = date
        
        if activity_code:
            query_filter["activity_code"] = activity_code
        
        if service_id:
            # Récupérer les utilisateurs du service
            users_collection = db['users']
            service_users = users_collection.find({"service_id": service_id})
            user_ids = [str(user["_id"]) for user in service_users]
            query_filter["user_id"] = {"$in": user_ids}
        
        # Récupérer les plannings avec le filtre
        planning_list = []
        for planning in plannings.find(query_filter).sort("date", 1):
            planning["_id"] = str(planning["_id"])
            planning["created_at"] = planning.get("created_at", "").isoformat() if planning.get("created_at") else ""
            planning["updated_at"] = planning.get("updated_at", "").isoformat() if planning.get("updated_at") else ""
            
            # Ajouter les informations de l'utilisateur
            user_info = db['users'].find_one({"_id": ObjectId(planning["user_id"])})
            if user_info:
                planning["user_name"] = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}"
                planning["user_matricule"] = user_info.get('matricule', '')
            
            planning_list.append(planning)
        
        return {
            "message": "Plannings récupérés avec succès",
            "data": planning_list,
            "count": len(planning_list),
            "filters": {
                "user_id": user_id,
                "date": date,
                "activity_code": activity_code,
                "service_id": service_id
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

@router.get("/plannings/{planning_id}")
async def get_planning_by_id(planning_id: str):
    """
    GET /plannings/{id}
    Récupère un planning par son ID
    """
    try:
        planning = plannings.find_one({"_id": ObjectId(planning_id)})
        if planning:
            planning["_id"] = str(planning["_id"])
            planning["created_at"] = planning.get("created_at", "").isoformat() if planning.get("created_at") else ""
            planning["updated_at"] = planning.get("updated_at", "").isoformat() if planning.get("updated_at") else ""
            
            # Ajouter les informations de l'utilisateur
            user_info = db['users'].find_one({"_id": ObjectId(planning["user_id"])})
            if user_info:
                planning["user_name"] = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}"
                planning["user_matricule"] = user_info.get('matricule', '')
            
            return {"message": "Planning récupéré avec succès", "data": planning}
        else:
            raise HTTPException(status_code=404, detail="Planning non trouvé")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

@router.get("/plannings/user/{user_id}")
async def get_plannings_by_user(user_id: str):
    """
    GET /plannings/user/{user_id}
    Récupère les plannings d'un utilisateur
    """
    try:
        planning_list = []
        for planning in plannings.find({"user_id": user_id}).sort("date", 1):
            planning["_id"] = str(planning["_id"])
            planning["created_at"] = planning.get("created_at", "").isoformat() if planning.get("created_at") else ""
            planning["updated_at"] = planning.get("updated_at", "").isoformat() if planning.get("updated_at") else ""
            
            # Ajouter les informations de l'utilisateur
            user_info = db['users'].find_one({"_id": ObjectId(planning["user_id"])})
            if user_info:
                planning["user_name"] = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}"
                planning["user_matricule"] = user_info.get('matricule', '')
            
            planning_list.append(planning)
        
        return {
            "message": f"Plannings de l'utilisateur {user_id} récupérés avec succès",
            "data": planning_list,
            "count": len(planning_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

@router.get("/plannings/date/{date}")
async def get_plannings_by_date(date: str):
    """
    GET /plannings/date/{date}
    Récupère les plannings pour une date donnée
    """
    try:
        planning_list = []
        for planning in plannings.find({"date": date}).sort("plage_horaire", 1):
            planning["_id"] = str(planning["_id"])
            planning["created_at"] = planning.get("created_at", "").isoformat() if planning.get("created_at") else ""
            planning["updated_at"] = planning.get("updated_at", "").isoformat() if planning.get("updated_at") else ""
            
            # Ajouter les informations de l'utilisateur
            user_info = db['users'].find_one({"_id": ObjectId(planning["user_id"])})
            if user_info:
                planning["user_name"] = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}"
                planning["user_matricule"] = user_info.get('matricule', '')
            
            planning_list.append(planning)
        
        return {
            "message": f"Plannings du {date} récupérés avec succès",
            "data": planning_list,
            "count": len(planning_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

@router.get("/plannings/activity/{activity_code}")
async def get_plannings_by_activity(activity_code: str):
    """
    GET /plannings/activity/{activity_code}
    Récupère les plannings par code d'activité
    """
    try:
        planning_list = []
        for planning in plannings.find({"activity_code": activity_code}).sort("date", 1):
            planning["_id"] = str(planning["_id"])
            planning["created_at"] = planning.get("created_at", "").isoformat() if planning.get("created_at") else ""
            planning["updated_at"] = planning.get("updated_at", "").isoformat() if planning.get("updated_at") else ""
            
            # Ajouter les informations de l'utilisateur
            user_info = db['users'].find_one({"_id": ObjectId(planning["user_id"])})
            if user_info:
                planning["user_name"] = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}"
                planning["user_matricule"] = user_info.get('matricule', '')
            
            planning_list.append(planning)
        
        return {
            "message": f"Plannings avec l'activité '{activity_code}' récupérés avec succès",
            "data": planning_list,
            "count": len(planning_list)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération: {str(e)}")

@router.put("/plannings/{planning_id}")
async def update_planning(planning_id: str, update_data: PlanningUpdate):
    """
    PUT /plannings/{id}
    Met à jour un planning
    """
    try:
        # Convertir l'ID string en ObjectId
        object_id = ObjectId(planning_id)
        
        # Vérifier que le planning existe
        existing_planning = plannings.find_one({"_id": object_id})
        if not existing_planning:
            raise HTTPException(status_code=404, detail="Planning non trouvé")
        
        # Préparer les données de mise à jour
        update_fields = {
            "updated_at": datetime.now()
        }
        
        if update_data.activity_code:
            update_fields["activity_code"] = update_data.activity_code
        
        if update_data.plage_horaire:
            update_fields["plage_horaire"] = update_data.plage_horaire
        
        if update_data.commentaire is not None:
            update_fields["commentaire"] = update_data.commentaire
        
        # Mettre à jour le planning
        result = plannings.update_one(
            {"_id": object_id},
            {"$set": update_fields}
        )
        
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Aucune modification effectuée")
        
        # Récupérer le planning mis à jour
        updated_planning = plannings.find_one({"_id": object_id})
        updated_planning["_id"] = str(updated_planning["_id"])
        updated_planning["created_at"] = updated_planning.get("created_at", "").isoformat() if updated_planning.get("created_at") else ""
        updated_planning["updated_at"] = updated_planning.get("updated_at", "").isoformat() if updated_planning.get("updated_at") else ""
        
        # Ajouter les informations de l'utilisateur
        user_info = db['users'].find_one({"_id": ObjectId(updated_planning["user_id"])})
        if user_info:
            updated_planning["user_name"] = f"{user_info.get('first_name', '')} {user_info.get('last_name', '')}"
        
        return {
            "message": "Planning mis à jour avec succès",
            "data": updated_planning
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la mise à jour: {str(e)}")

@router.delete("/plannings/{planning_id}")
async def delete_planning(planning_id: str):
    """
    DELETE /plannings/{id}
    Supprime un planning
    """
    try:
        # Convertir l'ID string en ObjectId
        object_id = ObjectId(planning_id)
        
        # Supprimer le planning
        result = plannings.delete_one({"_id": object_id})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Planning non trouvé")
        
        return {"message": "Planning supprimé avec succès"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la suppression: {str(e)}")

@router.get("/plannings/stats/summary")
async def get_planning_stats():
    """
    GET /plannings/stats/summary
    Récupère des statistiques sur les plannings
    """
    try:
        # Statistiques générales
        total_plannings = plannings.count_documents({})
        
        # Statistiques par code d'activité
        activity_stats = {}
        activities = ["SOIN", "CONGÉ", "REPOS", "FORMATION", "ADMINISTRATIF"]
        
        for activity in activities:
            count = plannings.count_documents({"activity_code": activity})
            activity_stats[activity] = count
        
        # Statistiques par date (7 derniers jours)
        from datetime import date, timedelta
        today = date.today()
        date_stats = {}
        
        for i in range(7):
            current_date = today + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")
            count = plannings.count_documents({"date": date_str})
            date_stats[date_str] = count
        
        return {
            "message": "Statistiques des plannings récupérées avec succès",
            "data": {
                "total_plannings": total_plannings,
                "by_activity": activity_stats,
                "by_date": date_stats
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des statistiques: {str(e)}")





