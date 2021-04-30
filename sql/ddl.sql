drop table if exists agencies CASCADE;
drop table if exists implementers CASCADE;
drop table if exists project_statuses CASCADE;
drop table if exists rfmps CASCADE;
drop table if exists counties CASCADE;
drop table if exists cpas CASCADE;
drop table if exists service_areas CASCADE;
drop table if exists fpts CASCADE;
drop table if exists projects CASCADE;
drop table if exists project_fpts CASCADE;
drop table if exists project_elements CASCADE;
drop table if exists projects_project_elements CASCADE;
drop table if exists programs CASCADE;
drop table if exists projects_programs CASCADE;
drop table if exists project_funding CASCADE;
drop table if exists habitat_units CASCADE;
drop table if exists habitat_parcels CASCADE;
drop table if exists habitat_outcomes CASCADE;
drop table if exists mitigation_types CASCADE;
drop table if exists mitigation_parcels CASCADE;
drop table if exists project_mitigation CASCADE;
drop table if exists project_commitments CASCADE;
drop table if exists credit_approver CASCADE;
drop table if exists bank_credits CASCADE;
drop table if exists credit_commitments CASCADE;
drop table if exists mandates CASCADE;
drop table if exists mitigation_needs CASCADE;
drop table if exists habitat_types CASCADE;
drop table if exists cosmos_targets CASCADE;

--agency options
create table if not exists agencies (
    id serial primary key,
    agency_name text
);

--implementers
create table  if not exists implementers (
    id serial primary key,
    agency integer references agencies,
    last_name text,
    first_name text,
    email text

);

--project status options
create table if not exists project_statuses (
    id serial primary key,
    project_status text
);

--RFMP options
create table if not exists rfmps (
    id serial primary key,
    rfmp_name text
);

--County options
create table if not exists counties (
    id serial primary key,
    county_name text
);

--CPA options
create table if not exists cpas (
    id serial primary key,
    cpa_name text
);

--Service Area options
create table if not exists service_areas (
    id serial primary key,
    service_area_name text
);


--Do we need a fpts table? what data would it store not already in project_details
create table if not exists fpts (
    id integer primary key
);

--project details
create table if not exists projects (
    id serial primary key,
    project_name text,
    implementer integer references implementers,  --can there be more than one implementer of a project?
    project_status integer references project_statuses,
    project_completion_date date,
    rfmp integer references rfmps,
    county integer references counties,
    cpa integer references cpas,
    coordinates point,
    waterbody text,
    service_area integer references service_areas,
    total_project_acres numeric,
    project_map_file_location text, --do we have this?
    service_area_map_file_location text, --do we have this?
    project_cost numeric

);

--1:1 projects and fpts entries
create table if not exists project_fpts (
    project_id integer references projects,
    fpts_id integer references fpts,
    primary key (project_id, fpts_id)
);

--project element options (levee setback, restoration)
create table if not exists project_elements (
    id serial primary key,
    project_elements text
);

--M:M projects and project elements
create table if not exists projects_project_elements (
    project_id integer references projects,
    project_elements integer references project_elements,
    primary key (project_id, project_elements)
);

--programs
create table if not exists programs (
    program_id serial primary key,
    program_name text
);

--M:M for projects and programs
create table if not exists projects_programs (
    project_id integer references projects,
    program_id integer references programs,
    primary key (project_id, program_id)
);

--project funding
create table if not exists project_funding (
    id serial primary key,
    project_id integer references projects,
    funding_source text,
    funding_amount numeric
);

--options for habitat units
create table if not exists habitat_units (
    id serial primary key,
    unit text
);

--options for habitat types
create table if not exists habitat_types (
    id serial primary key,
    habitat_type text
);

--spatially explicit habitat parcels
create table if not exists habitat_parcels (
    id serial primary key,
    project_id integer references projects,
    acres numeric
);

--habitat outcomes (pivot by habitat type options for data collection)
create table if not exists habitat_outcomes (
    id serial primary key,
    parcel_id integer references habitat_parcels,
    verified boolean,
    quantity numeric,
    unit integer references habitat_units,
    habitat_type integer references habitat_types
);

--options for mitigation types
create table if not exists mitigation_types (
    id serial primary key,
    mitigation_type text
);

-- spatially explict mitigation parcels
create table if not exists mitigation_parcels (
    id serial primary key,
    project_id integer references projects,
    acres numeric
);

--mitigation created or required by forecasted projects (mitigation credits are bundled)
create table if not exists project_mitigation (
    id serial primary key,
    parcel_id integer references mitigation_parcels,
    mitigation_type integer references mitigation_types,
    quantity numeric,  -- negative for needs, positive for creates
    unit integer references habitat_units  --confirm we dont need mitigation units
);

--predetermined commitments of mitigation created by projects (projects commit bundled credits on a parcel)
create table if not exists project_commitments (
    id integer primary key,
    parcel_id integer references mitigation_parcels,
    proportion numeric,
    committed_to text
);

--permitting agency approving mitigation credits (M:1; agency approves individual credit types on parcels)
create table if not exists credit_approver (
    credit_id integer references project_mitigation,
    agency integer references agencies,
    primary key (credit_id, agency)
);

--purchased mitigation credits
create table if not exists bank_credits (
    id serial primary key,
    purchase_date date,
    bank_name text,
    quantity numeric,
    credit_type integer references mitigation_types
);

--committed mitigation credits
create table if not exists credit_commitments (
    id serial primary key,
    committed_to text,
    project_id integer references projects
);

--mandates and drivers
create table if not exists mandates (
    id serial primary key,
    mandate_name text
);

--impacts (i.e., sources of past mitigation need that have a mandate)
create table if not exists impacts (
    id serial primary key,
    impact_name text
    -- relate to projects somehow?
);

--mitigation needs
create table if not exists mitigation_needs (
    id serial primary key,
    mandate integer references mandates,
    impact text,
    quantity numeric,
    unit integer references habitat_units,
    mitigation_type integer references mitigation_types,
    needed_by date
);

/*
Multiple agencies (e.g., USFWS, CDFW) may require differing mitigation per impact,
and require mitigation be obtained on different schedules. The higher of the quantities 
required, at the minimum of the need by dates, should be used for planning purposes.

To resolve mitigation needs over time, 
1. SELECT quantity, mitigation_type, needed_by FROM mitigation_needs GROUP BY impact
2. Pivot by mitigation_type (values=quantity), join needed_by, and calculate a new 
column with the cumulative difference of quantity to get a mitigation schedule
by mitigation_type (requires testing).
*/

--cosmos targets
create table if not exists cosmos_targets(
    id serial primary key,
    quantity numeric,
    unit integer references habitat_units,
    target_type integer references habitat_types
);
