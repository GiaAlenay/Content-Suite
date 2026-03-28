# Content-Suite

source venv/Scripts/activate

pip install -r requirements.txt
pip freeze > requirements.txt

uvicorn main:app --reload
