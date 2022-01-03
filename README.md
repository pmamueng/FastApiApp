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
    