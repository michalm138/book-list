# Book list

### Notice
Application has been deployed on heroku:
https://michalm138-book-list.herokuapp.com/app/book/list/

### Setup:
Install all necessary modules. I recommend you to use a virtual environment.
```
pip install -r requirements.txt
```

Project uses environment variables for higher security. Create *.env* file and add following lines:
```
SECRET_KEY=django-insecure-$#f_(z0bq+5pu)2g@=@y2%2etz4y4%wcoig5zyzk4!i#0ybb^g
ALLOWED_HOSTS=127.0.0.1
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Project runs on PostgreSQL by default, so environment variables with prefix DB should according to postgres db or you can modify django settings to use another database engine.

### Running project:
After configuration make migrations to the database:
```
python manage.py makemigrations
python manage.py migrate
```

Create a super user to manage django project:
```
python manage.py createsuperuser
```

Finally you can run the project:
```
python manage.py runserver
```
