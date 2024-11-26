 # Django Project

# Get Started:

#### first initialize .env file and then run below commands:

create virtual environment an install requirements:
```
python -m venv venv
pip install -r requirements.txt
```

initialize database:
```
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./accounts/fixture.json
```

run server:
```
python manage.py runserver
```

# Run With Docker:

```
sudo docker compose -f docker-compose.yml build --up
```

