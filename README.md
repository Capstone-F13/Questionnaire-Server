Questionnaire-Server
====================

# Local development 

### To run the server

```
python manage.py runserver
```

### To dump data from models to json fixture

```
python manage.py dumpdata questionnaire_server > questionnaire_server/fixtures/initial_data.json --indent=2
```

# Remote Development on Heroku

### To reset database

```
heroku pg:reset DATABASE
``` 

### To sync database

```
heroku run python manage.py syncdb
```

### To migrate database

```
heroku run python manage.py migrate
```
