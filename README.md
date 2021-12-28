# FastApiApp
Python API Development
---
* Set up virtual environment:
    * Windows: `python -m venv <virtual_venv_name>`
    * Mac: `python3 -m venv <virtual_venv_name>`
    * `<virtual_venv_name>` folder should be created automatically


* Start virtual environment in terminal:
    * Windows: `<virtual_venv_name>\Scripts\activate.bat`
    * Mac: `<virtual_venv_name>/bin/activate`
    * Terminal output: `(<virtual_venv_name) C:\...`
  

* pip install FastApi:
    * `pip install fastapi[all]`
  

* Start Application:
    * `uvicorn main:app --reload`