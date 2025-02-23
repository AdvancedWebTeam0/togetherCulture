# togetherCulture
Together Culture website

# Coding guideline

Use snake_case for filenames, variables and functions.

# Useful info

# Docker

In order to dockerize this project, download the 3 files Dockerfile, compose.yml and requirements.txt from Teams. Put the files into the root directory of the project (the folder that contains manage.py). Then run the following command. Note that below code is just for starting the container. See the database section for how to connect to database.

```
docker compose up --build
```

This will build the image and start the application on 0.0.0.0:8000. Make sure to add the required hosts to ALLOWED_HOSTS in settings.py if there are any errors.

```
ALLOWED_HOSTS = ["0.0.0.0", "127.0.0.1"]
```

In order to test the database connection you can run the following.

```
docker compose run django-web python manage.py migrate
```

# Use Django admin page to add data to database.

Create superuser.

```
python manage.py createsuperuser
```

Now, open a web browser and go to “/djangoadmin/” on your local domain – e.g., http://127.0.0.1:8000/djangoadmin/. You should see the admin’s login screen:

# Database connection

For development, use the local database. For production use or before assigment submission, use the database server hosted on Azure. 

## Local database using docker

When you start the containers by running the command in docker section, it also runs a local database container. In order to connect to it for development purposes, change the database section in settings.py to following.

```
HOST': 'db',
```

## Local database without docker

```
HOST': '127.0.0.1',
```

## Database server

Use the following in settings.py to connect to database server.

```

```
