# 🔧 Guide de Résolution des Erreurs - PlanRH

## 🚨 Erreurs Courantes et Solutions

### 1. **Erreur "response.map is not a function"**

**Cause :** Tentative d'appliquer `.map()` sur une réponse qui n'est pas un tableau.

**Solution :** Vérifier la structure de la réponse API avant d'appliquer `.map()`.

```typescript
// ❌ Incorrect
map(response => response.data || response)

// ✅ Correct
map(response => {
  if (response && response.data && Array.isArray(response.data)) {
    return response.data;
  }
  if (Array.isArray(response)) {
    return response;
  }
  return [];
})
```

### 2. **Erreur "Cannot find module"**

**Cause :** Import manquant ou chemin incorrect.

**Solutions :**
- Vérifier les imports dans les fichiers
- Utiliser `environment` au lieu d'URLs hardcodées
- Vérifier les chemins relatifs

```typescript
// ❌ Incorrect
import { environment } from '../../environment/environment';

// ✅ Correct
import { environment } from '../../environment/environment';
```

### 3. **Erreur "Property 'data' does not exist on type"**

**Cause :** TypeScript ne reconnaît pas la propriété `data` sur le type `any[]`.

**Solution :** Utiliser le bon type pour la réponse HTTP.

```typescript
// ❌ Incorrect
this.http.get<any[]>(url)

// ✅ Correct
this.http.get<any>(url)
```

### 4. **Erreur de connexion MongoDB**

**Cause :** MongoDB n'est pas démarré ou inaccessible.

**Solutions :**
1. Démarrer MongoDB :
   ```bash
   mongod
   ```

2. Vérifier la connexion :
   ```bash
   python -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); print('Connexion OK')"
   ```

3. Exécuter les scripts d'initialisation :
   ```bash
   python create_missing_tables.py
   python create_availabilities_collection.py
   ```

### 5. **Erreur "Collection does not exist"**

**Cause :** Les collections MongoDB n'ont pas été créées.

**Solution :** Exécuter les scripts d'initialisation.

```bash
cd PlanRHAPI
python create_missing_tables.py
python create_availabilities_collection.py
python create_plannings_collection.py
```

### 6. **Erreur CORS**

**Cause :** Problème de Cross-Origin Resource Sharing.

**Solution :** Vérifier la configuration CORS dans `main.py`.

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 7. **Erreur Angular "Cannot resolve dependency"**

**Cause :** Service non fourni ou import manquant.

**Solutions :**
1. Vérifier que le service est `providedIn: 'root'`
2. Vérifier les imports dans le composant
3. Redémarrer le serveur Angular

### 8. **Erreur "Cannot read property of undefined"**

**Cause :** Tentative d'accès à une propriété d'un objet undefined.

**Solution :** Utiliser l'opérateur de chaînage optionnel.

```typescript
// ❌ Incorrect
user.first_name

// ✅ Correct
user?.first_name || ''
```

## 🛠️ Scripts de Diagnostic

### Test des Endpoints API
```bash
python test_planification_endpoints.py
```

### Vérification des Collections MongoDB
```bash
python -c "from pymongo import MongoClient; client = MongoClient('localhost', 27017); db = client['planRhIA']; print('Collections:', db.list_collection_names())"
```

### Nettoyage du Cache Angular
```bash
python clean_angular_cache.py
```

## 📋 Checklist de Résolution

- [ ] MongoDB est démarré
- [ ] Collections MongoDB existent
- [ ] API FastAPI fonctionne (port 8000)
- [ ] Application Angular fonctionne (port 4200)
- [ ] Pas d'erreurs de linting
- [ ] Imports corrects
- [ ] Types TypeScript corrects
- [ ] Gestion des erreurs implémentée

## 🚀 Commandes de Démarrage

### Backend (API)
```bash
cd PlanRHAPI
uvicorn main:app --reload
```

### Frontend (Angular)
```bash
cd PlanRhApp
npm start
```

### Initialisation Base de Données
```bash
cd PlanRHAPI
python create_missing_tables.py
python create_availabilities_collection.py
```

## 💡 Conseils de Développement

1. **Toujours vérifier les types** avant d'appliquer des méthodes
2. **Utiliser la gestion d'erreurs** avec `catchError()`
3. **Tester les endpoints** avant de les utiliser dans le frontend
4. **Vérifier la structure des réponses** API
5. **Utiliser des interfaces TypeScript** pour la sécurité des types
6. **Implémenter des fallbacks** pour les cas d'erreur

## 📞 Support

En cas de problème persistant :
1. Vérifier les logs de l'API
2. Vérifier les logs du navigateur (F12)
3. Tester les endpoints individuellement
4. Vérifier la configuration de l'environnement



