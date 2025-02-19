# togetherCulture
Together Culture website

# Docker

In order to dockerize this project, download the 3 files Dockerfile, compose.yml and requirements.txt from Teams. Put the files into the root directory of the project (the folder that contains manage.py). Then run the following command.

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
