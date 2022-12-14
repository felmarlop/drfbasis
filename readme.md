Basis application with Django Rest Framework
============================================

Installation and Setup
----------------------

### Install PostgreSQL
https://gist.github.com/ibraheem4/ce5ccd3e4d7a65589ce84f2a3b7c23a3
- Create the user 'FMartin'.
- Create the database 'greatsphinx'.

*Note*: Restart postgreSQL<br>
*Is the server running locally and accepting connections on that socket?*

```bash
# In postgreSQL folder /usr/local/var/postgre
rm postmaster.pid
brew services restart postgresql
```

### Install requirements
*Note*: Create a virtual environment with **python3** before
``` bash
python3 -m venv /path/to/new/virtual/environment
pip install -r requirements.txt

```

### Run with runserver
``` bash
python manage.py runserver 8891
```

*Note*: To run and expose the service using **ngrok**, set the following environment variable:
```bash
export NGROK=True
export HOST_URL='<public_url>'
```

Useful documentation
----------------------
- [Python | Django & Rest](https://medium.com/django-rest)
- [Django rest framework doc](https://www.django-rest-framework.org/)
- [DRF JSON web tokens](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
   

