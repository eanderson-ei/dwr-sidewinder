# README

A prototype habitat forecasting application for conservation targets and mitigation needs.

[Plotly HTML Reports](https://plotly.com/python/v3/html-reports/)

[DataPane](https://datapane.com/accounts/signup/)

TODO

* Add RFMP, CPA for Winter Island Tidal Habitat Restoration
* Funding sources for project_funding
* 
* Limit outcomes to 100% and show actual add'l quantity as annotation to the right of the graph
* Wire date slider to filter projects by completion date
* Zoom map to CPA after selection
* Add mitigation page
* Update 

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



## Views

Projects 

Habitat Outcomes

Mitigation Needs

## Tips & Tricks

Row header in Excel file must be the same as the column name in the database

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

### Update database



If `db.drop_all()` is not working, in the database query editor use

```SQL
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

Then create the database again (see above).

Make sure that you either (1) from app import server or (2) set up Procfile as gunicorn: web index:app.server (I like the second since it is confusing to import something that is not used directly by index.py)

### Maps

To convert a shapefile to a GeoJSON, use `geopandas`:

```python
import geopandas as gpd
shp = gpd.read_file('shapefile.shp')
shp = shp.to_crs(epsg='4236')  # converts to WGS84 for web display
shp.to_file('geojson.json', driver="GeoJSON")
```



