from datetime import datetime
from app import db
from geoalchemy2 import Geometry  # maybe not available on Heroku 
# https://devcenter.heroku.com/articles/heroku-postgres-extensions-postgis-full-text-search
# https://blog.heroku.com/building_location_based_apps_with_postgis


# create many-to-many helper tables first
projects_programs = db.Table(
    'projects_programs',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('program_id', db.Integer, db.ForeignKey('programs.id'), primary_key=True)
)

project_fpts = db.Table(
    'project_fpts',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('fpts_id', db.Integer, db.ForeignKey('fpts.fpts_id'), primary_key=True)
)

project_project_statuses = db.Table(
    'project_project_statuses',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('project_elements', db.Integer, db.ForeignKey('project_elements.id'), primary_key=True)
)

credit_approver = db.Table(
    'credit_approver',
    db.Column('credit_id', db.Integer, db.ForeignKey('project_mitigation.id'), primary_key=True),
    db.Column('agency', db.Integer, db.ForeignKey('agencies.id'), primary_key=True)
)


# next create enum tables as classes
class Agency(db.Model):
    __tablename__ = 'agencies'
    id = db.Column(db.Integer, primary_key=True)
    agency_name = db.Column(db.String, nullable=False)

    
class Implementer(db.Model):
    __tablename__ = 'implementers'
    id = db.Column(db.Integer, primary_key=True)
    agency = db.Column(db.Integer, db.ForeignKey('agencies.id'), nullable=False)
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    

class ProjectStatus(db.Model):
    __tablename__ = 'project_statuses'
    id = db.Column(db.Integer, primary_key=True)
    project_status = db.Column(db.String, nullable=False)


class RFMP(db.Model):
    __tablename__ = 'rfmps'
    id = db.Column(db.Integer, primary_key=True)
    rfmp_name = db.Column(db.String, nullable=False)
    

class County(db.Model):
    __tablename__ = 'counties'
    id = db.Column(db.Integer, primary_key=True)
    county_name = db.Column(db.String, nullable=False)
    

class ConservationPlanningArea(db.Model):
    __tablename__ = 'conservation_planning_areas'
    id = db.Column(db.Integer, primary_key=True)
    cpa_name = db.Column(db.String, nullable=False)


class ServiceArea(db.Model):
    __tablename__ = 'service_areas'
    id = db.Column(db.Integer, primary_key=True)
    service_area_name = db.Column(db.String, nullable=False)
    

class ProjectElement(db.Model):
    __tablename__ = 'project_elements'
    id = db.Column(db.Integer, primary_key=True)
    project_elements = db.Column(db.String)


class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column(db.Integer, primary_key=True)
    program_name = db.Column(db.String(200), nullable=False)


class HabitatType(db.Model):
    __tablename__ = 'habitat_types'
    id = db.Column(db.Integer, primary_key=True)
    habitat_type = db.Column(db.String, nullable=False)
    

class HabitatUnit(db.Model):
    __tablename__ = 'habitat_units'
    id = db.Column(db.Integer, primary_key=True)
    habitat_unit = db.Column(db.String, nullable=False)


class MitigationType(db.Model):
    __tablename__ = 'mitigation_types'
    id = db.Column(db.Integer, primary_key=True)
    mitigation_type = db.Column(db.String, nullable=False)


# create each database table as a class
class Project(db.Model):
    __tablename__ = 'projects'
    
    # columns  
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, unique=True, nullable=False)
    implementer = db.Column(db.Integer, db.ForeignKey('implementers.id'), nullable=False)
    project_status = db.Column(db.Integer, db.ForeignKey('project_statuses.id'), nullable=False)
    project_completion_date = db.Column(db.DateTime, nullable=False)
    rfmp = db.Column(db.Integer, db.ForeignKey('rfmps.id'), nullable=False)
    county = db.Column(db.Integer, db.ForeignKey('counties.id'), nullable=False)
    cpa = db.Column(db.Integer, db.ForeignKey('conservation_planning_areas.id'), nullable=False)
    coordinates = db.Column(Geometry('POINT'))  # in prod, test PostGIS extension
    waterbody = db.Column(db.String)
    service_area = db.Column(db.Integer, db.ForeignKey('service_areas.id'), nullable=False)
    total_project_acres = db.Column(db.Float)
    project_map_file_location = db.Column(db.String)
    service_area_map_file_location = db.Column(db.String)
    project_cost = db.Column(db.Float)
    
    # relationships
    habitat_outcomes = db.relationship('HabitatOutcome', backref='project', lazy=True)
    programs = db.relationship('Program', secondary=projects_programs, 
                               lazy = 'subquery',
                               backref=db.backref('programs', lazy=True))
    
    def __repr__(self):
        return f"Project('{self.project_name}')"


class HabitatParcel(db.Model):
    __tablename__ = 'habitat_parcels'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    acres = db.Column(db.Float, nullable=False)


class HabitatOutcome(db.Model):
    __tablename__ = 'habitat_outcomes'
    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('habitat_parcels.id'), nullable=False)
    verified = db.Column(db.Boolean, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.Integer(), db.ForeignKey('habitat_units.id'), nullable=False)
    habitat_type = db.Column(db.Integer, db.ForeignKey('habitat_types.id'), nullable=False)
    
    def __repr__(self):
        return f'{self.quantity} {self.unit}s of {self.benefit_type} from {self.project.project_name}'


class MitigationParcel(db.Model):
    __tablename__ = 'mitigation_parcels'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    acres = db.Column(db.Float, nullable=False)
    

class ProjectMitigation(db.Model):
    __tablename__ = 'project_mitigation'
    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('mitigation_parcels.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.Integer, db.ForeignKey('habitat_units.id'), nullable=False)
    mitigation_type = db.Column(db.Integer, db.ForeignKey('mitigation_types.id'), nullable=False)


class ProjectCommitment(db.Model):
    __tablename__ = 'project_commitments'
    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('mitigation_parcels.id'), nullable=False)
    proportion_committed = db.Column(db.Float)
    committed_to = db.Column(db.String)


class MitigationCredit(db.Model):
    __tablename__ = 'mitigation_credits'
    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.DateTime)
    bank_name = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    credit_type = db.Column(db.Integer, db.ForeignKey('mitigation_types.id'), nullable=False)


class Mandate(db.Model):
    __tablename__ = 'mandates'
    id = db.Column(db.Integer, primary_key=True)
    mandate_name = db.Column(db.String, nullable=False)


class Impact(db.Model):
    __tablename__ = 'impacts'
    id = db.Column(db.Integer, primary_key=True)
    impact_name = db.Column(db.String)


class MitigationNeed(db.Model):
    __tablename__ = 'mitigation_needs'
    id = db.Column(db.Integer, primary_key=True)
    mandate = db.Column(db.Integer, db.ForeignKey('mandates.id'), nullable=False)
    impact = db.Column(db.Integer, db.ForeignKey('impacts.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.Integer, db.ForeignKey('habitat_units.id'), nullable=False)
    mitigation_type = db.Column(db.Integer, db.ForeignKey('mitigation_types.id'), nullable=False)
    needed_by = db.Column(db.DateTime, nullable=False)
    

class FPTS(db.Model):
    __tablename__ = 'fpts'
    id = db.Column(db.Integer, primary_key=True)
    fpts_id = db.Column(db.Integer, unique=True, nullable=False)
    

class FundingSource(db.Model):
    __tablename__ = 'funding_sources'
    id = db.Column(db.Integer, primary_key=True)
    funding_source = db.Column(db.String, nullable=False)
    funding_available = db.Column(db.Float, nullable=False)
    
    
class ProjectFunding(db.Model):
    __tablename__ = 'project_funding'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    funding_source = db.Column(db.Integer, db.ForeignKey('funding_sources.id'), nullable=False)
    funding_amount = db.Column(db.Float, nullable=False)
    

class CosmosTarget(db.Model):
    __tablename__ = 'cosmos_targets'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float, nullable=False)
    unit = db.Column(db.Integer, db.ForeignKey('habitat_units.id'), nullable=False)
    target_type = db.Column(db.Integer, db.ForeignKey('habitat_types.id'), nullable=False)
    target_date = db.Column(db.DateTime)
