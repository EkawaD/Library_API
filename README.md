# Shadow Library

Exemple d'une API permettant d'administrer une bibliothèque pour le compte de Shadow

## Get started

Admin account  
username : admin  
password: adminpassword  

## Steps to reproduce

0. ```django-admin startproject shadowlibrary```
1. Créer un fichier requirements.txt avec nos dépendances (pip freeze)
2. Créer un fichier Dockerfile pour installer nos dépendances
3. Créer un fichier docker-compose.yml avec deux services: web et db
=> Ici je ne définit pas d'utilisateur psql par simplicité.
4. Créer un dossier db_data pour dump la base de donnée
5. Edit settings.py in shadowlibrary avec la configuration de notre db (ne pas oublier allowed_host)
6. Créer une application django pour notre api
 ```django-admin startapp api```
7. Créer des fichier urls.py, serializers.py
8. Ajouter nos modèles (voir UML.png)
9. ```docker exec -ti shadowlibrary_web_1 python manage.py makemigrations```
10. ```docker exec -ti shadowlibrary_web_1 python manage.py migrate```
11. ```docker exec -ti shadowlibrary_web_1 python manage.py createsuperuser```
12. Create serializers for our models in serializers.py
13. Create an API Viewset for our models in views.py
