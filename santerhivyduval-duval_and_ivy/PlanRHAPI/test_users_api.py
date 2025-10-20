#!/usr/bin/env python3
"""
Script pour tester l'API des utilisateurs et voir ce qu'elle retourne
"""

import requests
import json

def test_users_api():
    print('🔍 Test de l\'API /users')
    print('=' * 60)
    
    try:
        # Test de l'endpoint /users
        response = requests.get('http://localhost:8000/users')
        
        if response.status_code == 200:
            data = response.json()
            print('✅ API /users fonctionne')
            print(f'📊 Nombre d\'utilisateurs retournés: {len(data.get("data", []))}')
            print()
            
            users = data.get('data', [])
            
            print('📋 Utilisateurs retournés par l\'API:')
            print('-' * 60)
            
            for user in users:
                print(f'👤 {user.get("first_name", "N/A")} {user.get("last_name", "N/A")}')
                print(f'   Role: {user.get("role", "N/A")}')
                print(f'   Service ID: {user.get("service_id", "VIDE")}')
                print(f'   Matricule: {user.get("matricule", "N/A")}')
                print()
            
            # Focus sur John Steve et Loick Eyoum
            print('🎯 Focus sur John Steve et Loick Eyoum:')
            print('-' * 60)
            
            john_steve = None
            loick_eyoum = None
            
            for user in users:
                if user.get('first_name') == 'John' and user.get('last_name') == 'Steve':
                    john_steve = user
                elif user.get('first_name') == 'Loick' and user.get('last_name') == 'Eyoum':
                    loick_eyoum = user
            
            if john_steve:
                print('✅ John Steve trouvé dans l\'API:')
                print(f'   Role: {john_steve.get("role")}')
                print(f'   Service ID: {john_steve.get("service_id")}')
                print(f'   Matricule: {john_steve.get("matricule")}')
            else:
                print('❌ John Steve NON trouvé dans l\'API')
            
            print()
            
            if loick_eyoum:
                print('✅ Loick Eyoum trouvé dans l\'API:')
                print(f'   Role: {loick_eyoum.get("role")}')
                print(f'   Service ID: {loick_eyoum.get("service_id")}')
                print(f'   Matricule: {loick_eyoum.get("matricule")}')
            else:
                print('❌ Loick Eyoum NON trouvé dans l\'API')
            
            print()
            print('🔍 Test du filtrage côté API:')
            print('-' * 60)
            
            if john_steve and loick_eyoum:
                john_service = john_steve.get('service_id')
                loick_service = loick_eyoum.get('service_id')
                
                print(f'John Steve service: {john_service}')
                print(f'Loick Eyoum service: {loick_service}')
                
                if john_service == loick_service:
                    print('✅ Même service - Le filtrage devrait fonctionner')
                    
                    # Simuler le filtrage côté frontend
                    filtered_users = [
                        user for user in users 
                        if user.get('service_id') == john_service and user.get('role') != 'cadre'
                    ]
                    
                    print(f'📊 Utilisateurs qui devraient apparaître: {len(filtered_users)}')
                    for user in filtered_users:
                        print(f'   - {user.get("first_name")} {user.get("last_name")} ({user.get("role")})')
                else:
                    print('❌ Services différents - C\'est le problème !')
            
        else:
            print(f'❌ Erreur API: {response.status_code}')
            print(f'Réponse: {response.text}')
            
    except Exception as e:
        print(f'❌ Erreur de connexion: {e}')
        print('Vérifiez que l\'API est démarrée sur http://localhost:8000')

if __name__ == "__main__":
    test_users_api()



