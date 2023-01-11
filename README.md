# Shadow Library

Exemple d'une API avec Django et django-rest-framework permettant d'administrer une bibliothèque pour le compte de Shadow

## Get started

* Pour tester cette application :  
```git clone https://github.com/EkawaD/Library_API.git app```  
```cd app```  
```docker-compose up -d```  
```docker exec -ti db psql -U postgres postgres < db_data/shadowlib.sql```  
* Postman/équivalent :
```POST 127.0.0.1/api/token```

```json
{
    "username": "shadow", 
    "password": "shadowpassword"  
}  

Replace with Admin account for securised endpoints
{  
    "username": "admin", 
    "password": "adminpassword"  
}  
```

* Save the "access" token

* Postman/équivalent :
```GET 127.0.0.1/api/book```

```json
Headears: {
    Authorization: "Bearer [token]"
}
```

## Endpoints

GET /admin, permissions: Admin
POST /api/token/, permissions: Any
POST /api/token/refresh, permissions: Any

GET /api/book/, permissions: Any
GET /api/book/1, permissions: Any
POST /api/book/, permissions: Admin
PUT/PATCH/DELETE /api/book/1, permissions: Admin
GET /api/book/1/rent, permissions: User
GET /api/book/1/return_rent, permissions: User

GET/POST /api/author, permissions: Admin
GET/PUT/PATCH/DELETE /api/author/1, permissions: Admin

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
9. ```docker exec -ti django python manage.py makemigrations```
10. ```docker exec -ti django python manage.py migrate```
11. ```docker exec -ti django python manage.py createsuperuser```
12. Créer des serializers pour nos models in api/serializers.py
13. Créer des vues pour nos models in api/views.py
14. Créer un fichier api/permissions.py pour créer des permissions personalisées
=> Si le projet doit comporter d'autres application, on pourrait séparer la logique de l'authentification/permissions dans une autre app nommé "auth"
15. Faire correspondre nos vues aux bon endpoints dans les fichiers shadowlibrary/urls.py et api/urls.py
16. Dump la base de donnée ```docker exec -ti db pg_dump -U postgres postgres > shadowlib.sql```

## TODO

* Ajouter des tests !
* Refactor duplicate logic in BookSerializer
