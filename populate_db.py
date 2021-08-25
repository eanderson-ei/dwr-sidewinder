from app import db
from apps.data import xlForecast
from apps.models import *

db.create_all()

F = 'data/Database of Expected Projects.xlsx'

# map xlForecast properties to SQLAlchemy classes
prop_to_class_map = {
    'agencies': Agency,
    'implementers': Implementer,
    'project_statuses': ProjectStatus,
    'rfmps': RFMP,
    'counties': County,
    'conservation_planning_areas': ConservationPlanningArea,
    'water_bodies': WaterBody,
    'project_elements': ProjectElement,
    'programs': Program,
    'habitat_types': HabitatType,
    'mitigation_types': MitigationType,
    'projects': Project,
    'habitat_parcels': HabitatParcel,
    'habitat_outcomes': HabitatOutcome,
    'mitigation_parcels': MitigationParcel,
    'project_mitigation': ProjectMitigation,
    'credit_purchases': CreditPurchase,
    'permits': Permit,
    'mitigation_needs': MitigationNeed,
    'project_commitments': ProjectCommitment,    
    'credit_commitments': CreditCommitment,
    'fpts': FPTS,
    'funding_source': FundingSource,
    'project_funding': ProjectFunding,
    'cosmos_targets': CosmosTarget
    }

prop_to_table_map = {
    'projects_programs': projects_programs,
    'project_fpts': project_fpts,
    'projects_project_elements': project_project_elements,
    'credit_approvers': credit_approver,
    'projects_counties': projects_counties,
    'projects_permits': projects_permits
}

# load data
data = xlForecast(F)

# insert data to database
for prop, tbl_class in prop_to_class_map.items():
    print(prop)
    for row in getattr(data, prop).to_dict('records'):
        db.session.add(tbl_class(**row))
    db.session.commit()
    
for prop, tbl_name in prop_to_table_map.items():
    print(prop)
    for row in getattr(data, prop).to_dict('records'):
        db.session.execute(tbl_name.insert().values(**row))
    db.session.commit()
