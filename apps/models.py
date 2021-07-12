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
    db.Column('data_form_id', db.Integer, db.ForeignKey('fpts.data_form_id'), primary_key=True)
)

project_project_elements = db.Table(
    'project_project_elements',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('project_element', db.Integer, db.ForeignKey('project_elements.id'), primary_key=True)
)

credit_approver = db.Table(
    'credit_approver',
    db.Column('parcel_id', db.Integer, db.ForeignKey('mitigation_parcels.id'), primary_key=True),
    db.Column('agency', db.Integer, db.ForeignKey('agencies.id'), primary_key=True)
)

projects_counties = db.Table(
    'projects_counties',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('county', db.Integer, db.ForeignKey('counties.id'), primary_key=True)
)

projects_permits = db.Table(
    'projects_permits',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('permit', db.Integer, db.ForeignKey('mitigation_needs.id'), primary_key=True)
)


# next create enum tables as classes
class Agency(db.Model):
    __tablename__ = 'agencies'
    id = db.Column(db.Integer, primary_key=True)
    agency_name = db.Column(db.String, nullable=False)

    
class Implementer(db.Model):
    __tablename__ = 'implementers'
    id = db.Column(db.Integer, primary_key=True)
    agency = db.Column(db.String)
    last_name = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String)
    

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


class WaterBody(db.Model):
    __tablename__ = 'water_bodies'
    id = db.Column(db.Integer, primary_key=True)
    waterbody_name = db.Column(db.String, nullable=False)
    

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
    unit = db.Column(db.String, nullable=False)
    long_form = db.Column(db.String)


class MitigationType(db.Model):
    __tablename__ = 'mitigation_types'
    id = db.Column(db.Integer, primary_key=True)
    mitigation_type = db.Column(db.String, nullable=False)
    unit = db.Column(db.String, nullable=False)
    long_form = db.Column(db.String)
    

# create each database table as a class
class Project(db.Model):
    __tablename__ = 'projects'
    
    # columns  
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String, unique=True, nullable=False)
    project_nickname = db.Column(db.String)
    implementer = db.Column(db.Integer, db.ForeignKey('implementers.id'))
    project_status = db.Column(db.Integer, db.ForeignKey('project_statuses.id'))
    project_completion_date = db.Column(db.DateTime)
    rfmp = db.Column(db.Integer, db.ForeignKey('rfmps.id'), nullable=False)
    cpa = db.Column(db.Integer, db.ForeignKey('conservation_planning_areas.id'), nullable=False)
    coordinate_x = db.Column(db.Float)  # TODO convert to PostGIS GEOMETRY
    coordinate_y = db.Column(db.Float)
    waterbody = db.Column(db.String)
    total_project_acres = db.Column(db.Float)
    project_map_file_location = db.Column(db.String)
    project_cost_low = db.Column(db.Float)
    project_cost_high = db.Column(db.Float)
    
    # relationships
    habitat_parcels = db.relationship('HabitatParcel', backref='project', lazy=True)
    mitigation_parcels = db.relationship('MitigationParcel', backref='project', lazy=True)
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
    habitat_outcomes = db.relationship('HabitatOutcome', backref='parcel', lazy=True)


class HabitatOutcome(db.Model):
    __tablename__ = 'habitat_outcomes'
    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('habitat_parcels.id'), nullable=False)
    confidence = db.Column(db.String)
    quantity = db.Column(db.Float, nullable=False)
    habitat_type = db.Column(db.Integer, db.ForeignKey('habitat_types.id'), nullable=False)
    
    def __repr__(self):
        return f'{self.quantity} {self.unit}s of {self.benefit_type} from {self.project.project_name}'


class MitigationParcel(db.Model):
    __tablename__ = 'mitigation_parcels'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    acres = db.Column(db.Float, nullable=False)
    parcel_mitigation = db.relationship('ProjectMitigation', backref='parcel', lazy=True)
    

class ProjectMitigation(db.Model):
    __tablename__ = 'project_mitigation'
    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('mitigation_parcels.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    mitigation_type = db.Column(db.Integer, db.ForeignKey('mitigation_types.id'), nullable=False)


class CreditPurchase(db.Model):
    __tablename__ = 'credit_purchases'
    id = db.Column(db.Integer, primary_key=True)
    purchase_date = db.Column(db.DateTime)
    credit_site = db.Column(db.String, nullable=False)
    service_area_map_file_location = db.Column(db.String)


class CreditValue(db.Model):
    __tablename__ = 'credit_values'
    id = db.Column(db.Integer, primary_key=True)
    credit_id = db.Column(db.Integer, db.ForeignKey('credit_purchases.id'))
    quantity = db.Column(db.Float, nullable=False)
    mitigation_type = db.Column(db.Integer, db.ForeignKey('mitigation_types.id'), nullable=False)


class Permit(db.Model):
    __tablename__ = 'permits'
    id = db.Column(db.Integer, primary_key=True)
    permit_name = db.Column(db.String, nullable=False)


class MitigationNeed(db.Model):
    __tablename__ = 'mitigation_needs'
    id = db.Column(db.Integer, primary_key=True)
    permit = db.Column(db.Integer, db.ForeignKey('permits.id'), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    needed_by = db.Column(db.DateTime)
    mitigation_type = db.Column(db.Integer, db.ForeignKey('mitigation_types.id'), nullable=False)
    

class ProjectCommitment(db.Model):
    __tablename__ = 'project_commitments'
    id = db.Column(db.Integer, primary_key=True)
    parcel_id = db.Column(db.Integer, db.ForeignKey('mitigation_parcels.id'), nullable=False)
    proportion_committed = db.Column(db.Float)
    committed_to = db.Column(db.Integer, db.ForeignKey('permits.id'), nullable=False)


class CreditCommitment(db.Model):
    __tablename__ = 'credit_commitments'
    id = db.Column(db.Integer, primary_key=True)
    permit_id = db.Column(db.Integer, db.ForeignKey('permits.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    credit_id = db.Column(db.Integer, db.ForeignKey('credit_purchases.id'), nullable=False)
 

class FPTS(db.Model):
    __tablename__ = 'fpts'
    data_form_id = db.Column(db.Integer, primary_key=True)
    

class FundingSource(db.Model):
    __tablename__ = 'funding_sources'
    id = db.Column(db.Integer, primary_key=True)
    funding_source = db.Column(db.String, nullable=False)
    funding_available = db.Column(db.Float)
    
    
class ProjectFunding(db.Model):
    __tablename__ = 'project_funding'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    funding_source = db.Column(db.Integer, db.ForeignKey('funding_sources.id'), nullable=False)
    funding_amount = db.Column(db.Float, nullable=False)
    project_phase = db.Column(db.Integer, db.ForeignKey('project_statuses.id'))
    

class CosmosTarget(db.Model):
    __tablename__ = 'cosmos_targets'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Float)
    habitat_type = db.Column(db.Integer, db.ForeignKey('habitat_types.id'), nullable=False)
    target_date = db.Column(db.DateTime)
    cpa = db.Column(db.Integer, db.ForeignKey('conservation_planning_areas.id'), nullable=False)
