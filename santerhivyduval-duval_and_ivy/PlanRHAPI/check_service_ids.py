#!/usr/bin/env python3
"""
Script pour vérifier les service_id des utilisateurs et diagnostiquer le problème de planification
"""

from pymongo import MongoClient

def check_service_ids():
    client = MongoClient('localhost', 27017)
    db = client['planRhIA']

    print('🔍 Vérification des service_id des utilisateurs')
    print('=' * 60)

    # Récupérer tous les utilisateurs avec leurs service_id
    users = list(db.users.find({}, {'first_name': 1, 'last_name': 1, 'role': 1, 'service_id': 1, 'matricule': 1}))

    print('📋 Tous les utilisateurs et leurs service_id:')
    print('-' * 60)
    for user in users:
        print(f'👤 {user["first_name"]} {user["last_name"]} ({user["role"]})')
        print(f'   📧 Matricule: {user.get("matricule", "N/A")}')
        print(f'   🏥 Service ID: {user.get("service_id", "VIDE")}')
        print()

    print('🎯 Focus sur John Steve et Loick Eyoum:')
    print('-' * 60)

    john_steve = None
    loick_eyoum = None

    for user in users:
        if user['first_name'] == 'John' and user['last_name'] == 'Steve':
            john_steve = user
        elif user['first_name'] == 'Loick' and user['last_name'] == 'Eyoum':
            loick_eyoum = user

    if john_steve:
        print(f'✅ John Steve trouvé:')
        print(f'   Role: {john_steve["role"]}')
        print(f'   Service ID: {john_steve.get("service_id", "VIDE")}')
        print(f'   Matricule: {john_steve.get("matricule", "N/A")}')
    else:
        print('❌ John Steve non trouvé')

    print()

    if loick_eyoum:
        print(f'✅ Loick Eyoum trouvé:')
        print(f'   Role: {loick_eyoum["role"]}')
        print(f'   Service ID: {loick_eyoum.get("service_id", "VIDE")}')
        print(f'   Matricule: {loick_eyoum.get("matricule", "N/A")}')
    else:
        print('❌ Loick Eyoum non trouvé')

    print()
    print('🔍 Analyse du problème:')
    print('-' * 60)

    if john_steve and loick_eyoum:
        john_service = john_steve.get('service_id')
        loick_service = loick_eyoum.get('service_id')
        
        if john_service == loick_service:
            print('✅ MÊME SERVICE: John Steve et Loick Eyoum sont dans le même service')
            print(f'   Service ID commun: {john_service}')
        else:
            print('❌ SERVICES DIFFÉRENTS:')
            print(f'   John Steve service: {john_service}')
            print(f'   Loick Eyoum service: {loick_service}')
            print()
            print('💡 SOLUTION: Ils doivent être dans le même service pour que Loick apparaisse dans la planification de John')
        
        print()
        print('📊 Utilisateurs par service:')
        services = {}
        for user in users:
            service_id = user.get('service_id', 'VIDE')
            if service_id not in services:
                services[service_id] = []
            services[service_id].append(f'{user["first_name"]} {user["last_name"]} ({user["role"]})')
        
        for service_id, users_list in services.items():
            print(f'   🏥 Service {service_id}: {len(users_list)} utilisateurs')
            for user_info in users_list:
                print(f'      - {user_info}')

    print()
    print('🛠️ Solutions possibles:')
    print('-' * 60)
    print('1. Si services différents: Assigner Loick Eyoum au service de John Steve')
    print('2. Si service_id vide: Assigner un service_id valide')
    print('3. Si problème de localStorage: Vérifier la connexion utilisateur')

    client.close()

if __name__ == "__main__":
    try:
        check_service_ids()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("Vérifiez que MongoDB est démarré et accessible.")






