pip install -r requirements.txt
python3.12 manage.py collectstatic --no-input --clear
python3.12 manage.py migrate