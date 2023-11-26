## Activating Python Environment
```sh 
source /home/niall/.virtualenvs/mindfulu/bin/python/bin/activate
```

## Running migrations
```sh 
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
```

## Accessing mindfulu database
```sh 
psql
docker exec -it <container-id> psql -U admin -d mindfulu
```

## Database modifications in case of failure
`This will remove everything from the database. Migrations will need to be run again`
```sh 
mindfulu=# DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

## Run scraping tool

```sh
docker-compose exec backend python manage.py run_active_canvas_scraping```

export EMAIL_USER='your-gmail-username@gmail.com'
export EMAIL_PASSWORD='your-gmail-app-password'
```

## Accessing External Website

```sh
http://mindful-u.co.uk/login
```