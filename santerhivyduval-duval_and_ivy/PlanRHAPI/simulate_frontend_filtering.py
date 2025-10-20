#!/usr/bin/env python3
"""
Script pour simuler le localStorage et tester le filtrage côté frontend
"""

import requests
import json

def simulate_frontend_filtering():
    print('🔍 Simulation du filtrage côté frontend')
    print('=' * 60)
    
    try:
        # Récupérer les utilisateurs via l'API
        response = requests.get('http://localhost:8000/users')
        
        if response.status_code != 200:
            print(f'❌ Erreur API: {response.status_code}')
            return
        
        data = response.json()
        users = data.get('data', [])
        
        print(f'📊 Utilisateurs récupérés de l\'API: {len(users)}')
        print()
        
        # Simuler différents scénarios de localStorage
        scenarios = [
            {
                'name': 'Scénario 1: localStorage vide',
                'currentUser': {}
            },
            {
                'name': 'Scénario 2: localStorage avec service_id correct',
                'currentUser': {
                    'service_id': '684312ea3bd4c4c00ce9c012',
                    'first_name': 'John',
                    'last_name': 'Steve',
                    'role': 'cadre'
                }
            },
            {
                'name': 'Scénario 3: localStorage avec service_id incorrect',
                'currentUser': {
                    'service_id': '684312fa3bd4c4c00ce9c013',
                    'first_name': 'John',
                    'last_name': 'Steve',
                    'role': 'cadre'
                }
            },
            {
                'name': 'Scénario 4: localStorage sans service_id',
                'currentUser': {
                    'first_name': 'John',
                    'last_name': 'Steve',
                    'role': 'cadre'
                }
            }
        ]
        
        for scenario in scenarios:
            print(f'🧪 {scenario["name"]}')
            print('-' * 40)
            
            currentUser = scenario['currentUser']
            print(f'Current User: {currentUser}')
            
            # Appliquer le filtre comme dans le frontend
            serviceUsers = [
                user for user in users 
                if user.get('service_id') == currentUser.get('service_id') and user.get('role') != 'cadre'
            ]
            
            print(f'Utilisateurs filtrés: {len(serviceUsers)}')
            
            if serviceUsers:
                print('Agents trouvés:')
                for user in serviceUsers:
                    print(f'  - {user.get("first_name")} {user.get("last_name")} ({user.get("role")})')
            else:
                print('❌ Aucun agent trouvé')
            
            print()
        
        print('🔍 Analyse des utilisateurs par service:')
        print('-' * 60)
        
        services = {}
        for user in users:
            service_id = user.get('service_id', 'VIDE')
            if service_id not in services:
                services[service_id] = []
            services[service_id].append(user)
        
        for service_id, users_list in services.items():
            print(f'🏥 Service {service_id}: {len(users_list)} utilisateurs')
            for user in users_list:
                print(f'   - {user.get("first_name")} {user.get("last_name")} ({user.get("role")})')
            print()
        
        print('💡 Solutions possibles:')
        print('-' * 60)
        print('1. Vérifier que le localStorage contient le bon service_id')
        print('2. Vérifier que l\'utilisateur est bien connecté')
        print('3. Vérifier que le service_id n\'est pas null/undefined')
        print('4. Ajouter des logs pour voir le contenu exact du localStorage')
        
    except Exception as e:
        print(f'❌ Erreur: {e}')

if __name__ == "__main__":
    simulate_frontend_filtering()



