# README

A prototype habitat forecasting application for conservation targets and mitigation needs.

TODO

* Add RFMP, CPA for Winter Island Tidal Habitat Restoration
* Funding sources for project_funding

## Dev Setup

To contribute to development, follow steps below.

#### Connect to database

Download and install PostgreSQL and pgAdmin. The database is hosted with the app instance on Heroku. Request the database URI from me. See [here](https://eanderson-ei.github.io/ei-dev/data-management/postgres-tutorial/) for step-by-step instructions.

##### Install and Enable PostGIS

Using the Stack Builder application downloaded with Postgres, install PostGIS (under spatial databases). Do not install PostGIS into the default folder, instead navigate to the location where Postgres is installed (C:/Program Files/). 

Right click on the database in pgAdmin and select 'Query Tool'. Clear the contents of the script and run the following (use the play button to run).

```sql
CREATE EXTENSION postgis
```

#### Install Packages

Recreate the environment from the `environments.yml` file (`conda env create -f environment.yml`).

## Resources

https://towardsdatascience.com/building-and-deploying-a-login-system-backend-using-flask-sqlalchemy-and-heroku-8b2aa6cc9ec3

https://www.youtube.com/watch?v=w25ea_I89iM

## Next Steps

3. Share xlsx database with ESA
5. Deploy dash app and database  (May 24/25)
   1. Create database on Heroku
   2. Add PostGIS extension to Heroku (get cc to host) OR change POINT to Float type
8. Client feedback on wireframes with dummy data (week of June 28)
9. Update app, documentation, etc. (thru June 30)

## Tips & Tricks

Row header in Excel file must be the same as the column name in the database

If `db.drop_all()` is not working, in the database query editor use

```SQL
DROP SCHEMA public CASCADE
CREATE SCHEMA public
```

Then create the database again

```
python
>>>from apps import db
>>>from apps.models import *
>>>db.create_all()
>>>exit()
```

### Set up database

Create a database in Postgres (start with a local database for testing)

Enable PostGIS (`CREATE EXTENSION postgis`; in Query Tool on database)

In a prompt window, start a python session. Use the following to set up the database

```python
from app import db
from apps.models import *
db.create_all()
exit()
```

Use the `populate_db.py` script to populate the database. First update the database location (in `apps/__init__.py`) and Excel file location (in populate_db.py; if needed). Then run

```python
python populate_db.py
```



