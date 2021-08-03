CREATE OR REPLACE VIEW view_project_mitigation AS
	SELECT 
		projects.project_nickname,
		conservation_planning_areas.cpa_name,
		mitigation_types.mitigation_type,
		mitigation_types.long_form,
		mitigation_types.unit,
		sum(project_mitigation.quantity) as total_mitigation
	FROM project_mitigation
	JOIN mitigation_parcels on project_mitigation.parcel_id = mitigation_parcels.id
	JOIN projects on mitigation_parcels.project_id = projects.id
	JOIN conservation_planning_areas on projects.cpa = conservation_planning_areas.id
	JOIN mitigation_types on project_mitigation.mitigation_type = mitigation_types.id
	GROUP BY projects.project_nickname, 
		conservation_planning_areas.cpa_name,
		mitigation_types.mitigation_type,
		mitigation_types.long_form,
		mitigation_types.unit
