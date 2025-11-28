# 📝 Todo App - Application d'Examen

Application Flask complète avec PostgreSQL pour l'examen de conteneurisation et orchestration.

## 📁 Structure du projet

```
todo-flask/
├── app.py                  # Application Flask
├── requirements.txt        # Dépendances Python
├── Containerfile          # Build multi-stage (EXEMPLE - À ADAPTER)
├── job.nomad.hcl          # Job Nomad (EXEMPLE - À ADAPTER)
├── .gitlab-ci.yml         # Pipeline CI/CD (BONUS)
├── templates/
│   └── index.html         # Interface utilisateur
└── README.md              # Ce fichier
```

## 🚀 Démarrage rapide local (sans conteneur)

### Prérequis
- Python 3.11+
- PostgreSQL 15+

### Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer les variables d'environnement
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=tododb
export DB_USER=todouser
export DB_PASSWORD=todopass

# Créer la base de données (dans psql)
CREATE DATABASE tododb;
CREATE USER todouser WITH PASSWORD 'todopass';
GRANT ALL PRIVILEGES ON DATABASE tododb TO todouser;

# Lancer l'application
python app.py
```

L'application sera accessible sur http://localhost:5000

## 📊 Fonctionnalités de l'application

- ✅ Affichage de toutes les tâches
- ✅ Ajout de nouvelles tâches
- ✅ Marquer une tâche comme terminée/en cours
- ✅ Suppression de tâches
- ✅ Statistiques (total, terminées, en cours)
- ✅ Healthcheck endpoint (`/health`)
- ✅ Interface responsive et moderne

## 🔧 Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `DB_HOST` | Hôte PostgreSQL | `localhost` |
| `DB_PORT` | Port PostgreSQL | `5432` |
| `DB_NAME` | Nom de la BDD | `tododb` |
| `DB_USER` | Utilisateur BDD | `todouser` |
| `DB_PASSWORD` | Mot de passe BDD | `todopass` |

## 📝 Points d'attention pour l'examen

### Containerfile
- ✅ Le build multi-stage est déjà implémenté dans l'exemple
- ⚠️ **À ADAPTER** : Vous devez comprendre et potentiellement optimiser chaque étape
- ⚠️ Vérifiez la taille finale de l'image
- ⚠️ Assurez-vous que l'utilisateur non-root fonctionne

### Job Nomad
- ✅ Le job exemple utilise le mode `bridge` pour la communication
- ⚠️ **À ADAPTER** : Vous devez ajuster selon votre infrastructure
- ⚠️ Les chemins de volumes doivent exister sur votre host
- ⚠️ Vérifiez que les ports ne sont pas déjà utilisés

### Communication BDD
En mode bridge, les deux conteneurs partagent le même network namespace :
- L'application peut accéder à PostgreSQL via `127.0.0.1:5432`
- Pas besoin de service discovery complexe

### GitLab CI (BONUS)
- ⚠️ Remplacer `REGISTRY_URL` par votre registry
- ⚠️ Configurer les variables CI/CD dans GitLab
- ⚠️ Adapter les runners disponibles

## 🐛 Debugging

### L'app ne se connecte pas à la BDD
```bash
# Vérifier les logs PostgreSQL
nomad alloc logs <alloc-id> postgres

# Vérifier les logs de l'app
nomad alloc logs <alloc-id> webapp

# Tester la connexion depuis l'app
nomad alloc exec <alloc-id> webapp env | grep DB_
```

### L'image est trop lourde
```bash
# Comparer avec une approche single-stage
podman images | grep todo-app

# Analyser les layers
podman history todo-app:latest
```

## 💡 Conseils pour l'examen

1. **Testez localement d'abord** avec `podman run`
2. **Vérifiez les logs** à chaque étape
3. **Documentez vos choix** dans le rapport
4. **N'hésitez pas à simplifier** : une app qui marche > une app complexe qui plante
5. **Le healthcheck est important** pour Nomad

## 📚 Ressources

- [Documentation Podman](https://docs.podman.io/)
- [Documentation Nomad](https://developer.hashicorp.com/nomad/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

**Bon courage pour votre examen ! 🚀**
