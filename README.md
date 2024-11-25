 # Django Project

# Get Started:

first of all, initialize .env file and then run below commands:

```
python -m venv venv
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./accounts/fixture.json
python manage.py runserver
```

# Run With Docker:

```
sudo docker compose -f docker-compose.yml build --up
```

