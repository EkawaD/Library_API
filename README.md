# Shadow Library

Exemple d'une API permettant d'administrer une bibliothèque pour le compte de Shadow

## Get started

...

## Steps to reproduce

1. Créer un fichier requirements.txt avec nos dépendances (pip freeze)
2. Créer un fichier Dockerfile pour installer nos dépendances
3. Créer un fichier docker-compose.yml avec deux services: web et db
Ici je ne définit pas d'utilisateur psql par simplicité.
4. Créer un dossier db_data pour dump la base de donnée
5. Edit settings.py in shadowlibrary avec la configuration de notre db (ne pas oublier allowed_host)
