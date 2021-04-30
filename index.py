from db_app import app

if __name__== '__main__':
    app.run(debug=True)


# to create the tables from the model in your database, type this in python
# from the root (local dev)
''' 
from app import db
db.create_all()
'''

# after deployment
'''
heroku run python
from app import db
db.create_all()
exit()
'''

# login to database remotely after deployment
'''
pg: psql --app <app_name>
select * from feedback  # example of accessing data from the database
'''

# add data
'''
from app import Project, Habitat_Outcomes
project_1 = Project(project_name = '')
db.session.add(project_1)
db.session.commit()
'''

# delete everything
'''
db.drop_all()
'''