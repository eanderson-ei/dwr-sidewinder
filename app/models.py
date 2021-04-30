from datetime import datetime
from db_app import db


# create many-to-many helper tables first
projects_programs = db.Table(
    'projects_programs',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), primary_key=True)
)

'''If you want to use many-to-many relationships you will need to define a helper 
table that is used for the relationship. For this helper table it is strongly 
recommended to not use a model but an actual table'''


# next create enum tables as classes
class ConservationPlanningArea(db.Model):
    __tablename__ = 'conservation_planning_areas'
    id = db.Column(db.Integer, primary_key=True)
    cpa_name = db.Column(db.String(200), nullable=False)


# create each database table as a class
class Project(db.Model):
    __tablename__ = 'projects'  
    '''by default, the tablename will be the lowercase of the class name, 
    with CamelCase converted to camel_case, so this can be omitted'''
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), unique=True, nullable=False)
    cpa = db.Column(db.Integer, db.ForeignKey('conservation_planning_areas.id'), nullable=False)
    habitat_outcomes = db.relationship('HabitatOutcome', backref='project', lazy=True)
    
    '''Relationships are queries. This will allow SQLAlchemy to construct a query
    with all habitat_outcomes associated with a project. Use project.habitat_outcomes 
    to get all habitat outcomes associated with a project. Use habitat_outcomes.project
    to get the project of the habitat_outcome being investigated.'''
    
    programs = db.relationship('Program', secondary=projects_programs, 
                               lazy = 'subquery',
                               backref=db.backref('programs', lazy=True))
    '''project.programs is loaded as a separate query upon loading a project.'''
    
    
    # how to print record
    def __repr__(self):
        return f"Project('{self.project_name}')"


class HabitatOutcome(db.Model):
    __tablename__ = 'habitat_outcomes'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)  # do not add parens to utcnow
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    benefit_type = db.Column(db.String(100), nullable=False)
    
    def __repr__(self):
        return f'{self.quantity} {self.unit}s of {self.benefit_type} from {self.project.project_name}'


class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True)
    program_name = db.Column(db.String(200), nullable=False)
    