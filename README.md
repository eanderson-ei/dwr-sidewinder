# EADME

A prototype habitat forecasting application for conservation targets and mitigation needs.

## Dev Setup

To contribute to development, follow steps below.

#### Connect to database

Download and install PostgreSQL and pgAdmin. The database is hosted with the app instance on Heroku. Request the database URI from me. See [here](https://eanderson-ei.github.io/ei-dev/data-management/postgres-tutorial/) for step-by-step instructions.

##### Install and Enable PostGIS

Using the Stack Builder application downloaded with Postgres, install PostGIS (under spatial databases). Do not install PostGIS into the default folder, instead navigate to the location where Postgres is installed (C:/Program Files/). 

Right click on the database in pgAdmin and select 'CREATE SCRIPT'. Clear the contents of the script and run the following (use the play button to run).

```sql
CREATE EXTENSION postgis
```

#### Install Packages

Recreate the environment from the `environments.yml` file (`conda env create -f environment.yml`).

## Resources

https://towardsdatascience.com/building-and-deploying-a-login-system-backend-using-flask-sqlalchemy-and-heroku-8b2aa6cc9ec3

https://www.youtube.com/watch?v=w25ea_I89iM

## Next Steps

1. Work with Kristen on initial data import (May 12)
2. KB inputs data (thru May 19) - enough to share with ESA
3. Debug read data from Excel
4. Share xlsx database with ESA
5. Deploy dash app and database  (May 24/25)
   1. Create database on Heroku
   2. Add PostGIS extension to Heroku (get cc to host) OR change POINT to Float type
6. Set up notebook for KB to read data from Heroku, manipulate data, and create visuals (DO NOT COMMIT TO GITHUB) (May 25/28)
7. Create wireframes (week of May 25)
8. Client feedback on wireframes with dummy data (week of June 14)
9. Update app, documentation, etc. (thru June 30)

## Tips & Tricks

### Set up database

