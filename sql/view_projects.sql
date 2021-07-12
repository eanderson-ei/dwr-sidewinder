CREATE OR REPLACE VIEW view_projects AS
	SELECT 
		projects.project_name,
		projects.project_nickname,
		projects.implementer,
		projects.project_status,
		rfmps.rfmp_name,
		conservation_planning_areas.cpa_name,
		projects.coordinate_x,
		projects.coordinate_y,
		projects.waterbody,
		projects.total_project_acres,
		projects.project_map_file_location,
		projects.project_cost_low,
		projects.project_cost_high
	FROM projects
	LEFT JOIN rfmps ON projects.rfmp = rfmps.id
	LEFT JOIN conservation_planning_areas ON projects.cpa = conservation_planning_areas.id;