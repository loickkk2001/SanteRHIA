#!/usr/bin/env python3
"""
Test simple pour vérifier l'import du router saphir
"""

try:
    from routers import saphir
    print("✅ Import du router saphir réussi")
    print(f"Router: {saphir.router}")
    print(f"Routes: {[route.path for route in saphir.router.routes]}")
except Exception as e:
    print(f"❌ Erreur d'import: {e}")

try:
    from main import app
    print("✅ Import de l'app principale réussi")
    print(f"Routes de l'app: {[route.path for route in app.routes]}")
except Exception as e:
    print(f"❌ Erreur d'import de l'app: {e}")













