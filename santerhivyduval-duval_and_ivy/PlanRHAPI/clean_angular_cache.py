#!/usr/bin/env python3
"""
Script pour nettoyer et redémarrer le serveur Angular
"""

import subprocess
import os
import sys

def clean_and_restart_angular():
    """Nettoie le cache et redémarre Angular"""
    print("🧹 Nettoyage du cache Angular...")
    
    try:
        # Changer vers le répertoire Angular
        angular_dir = "C:\\Users\\c940\\Desktop\\msr2\\santerhivyduval-duval_and_ivy\\PlanRhApp"
        os.chdir(angular_dir)
        
        # Nettoyer le cache Angular
        print("1. Suppression du dossier .angular...")
        subprocess.run(["rmdir", "/s", "/q", ".angular"], shell=True, capture_output=True)
        
        print("2. Suppression du dossier node_modules/.cache...")
        subprocess.run(["rmdir", "/s", "/q", "node_modules\\.cache"], shell=True, capture_output=True)
        
        print("3. Suppression du dossier dist...")
        subprocess.run(["rmdir", "/s", "/q", "dist"], shell=True, capture_output=True)
        
        print("✅ Cache nettoyé avec succès!")
        print("\n🚀 Pour redémarrer Angular:")
        print("   npm start")
        print("\n💡 Les erreurs de compilation devraient être résolues après le redémarrage.")
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")

if __name__ == "__main__":
    clean_and_restart_angular()




