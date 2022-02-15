# FastApiApp
Python API Development
---
* Set up virtual environment:
    * Windows: `python -m venv venv`
    * Mac/Linux: `python3 -m venv venv`


* Start virtual environment in terminal:
    * Windows: `venv\Scripts\activate.bat`
    * Mac/Linux: `venv/bin/activate`


* pip install requirements:
    * `pip install -r requirements.txt`


* Start Application:
    * `uvicorn app.main:app --reload`


* FastApi Application Documentation:
    * swagger: `localhost:8000/docs`
    * redoc: `localhost:8000/redoc`


* Database Management System: (DBMS):
    * Postgresql (relational database)
    * Utilize Oject Relational Mapper (ORM)
        * SQLalchemy


* Routers
    * `auth.py`
    * `post.py`
    * `user.py`
    * `vote.py`


* Authentication
    * Utilize JWT Token Authentication


* .env file
```
DATABASE_HOSTNAME=
DATABASE_PORT=
DATABASE_USERNAME=
DATABASE_PASSWORD=
DATABASE_NAME=
SECRET_KEY=
ALGORITHM=
ACCESS_TOKEN_EXPIRE_MINUTES=
```


* Heroku
```
=== fastapiapp-maximumdevops
Addons:         heroku-postgresql:hobby-dev
Auto Cert Mgmt: false
Dynos:          web: 1
Git URL:        https://git.heroku.com/fastapiapp-maximumdevops.git
Owner:          pmamueng.dev@gmail.com
Region:         us
Repo Size:      362 KB
Slug Size:      82 MB
Stack:          heroku-20
Web URL:        https://fastapiapp-maximumdevops.herokuapp.com/
```


* Docker Compose
Start docker container: ```docker-compose up -d```
DEV environment: ```docker-compose -f docker-compose-dev.yml up -d```
PROD environment: ```docker-compose -f docker-compose-prod.yml up -d``` (shouldn't be used)