CREATE OR REPLACE VIEW view_parcel_outcomes AS
	SELECT habitat_parcels.id AS PARCEL_ID,
		habitat_parcels.acres,
		SUM(HABITAT_OUTCOMES.QUANTITY) AS QUANTITY,
		HABITAT_TYPES.UNIT,
		HABITAT_TYPES.HABITAT_TYPE,
		HABITAT_TYPES.LONG_FORM,
		PROJECTS.PROJECT_NICKNAME,
		CONSERVATION_PLANNING_AREAS.CPA_NAME,
		PROJECT_STATUSES.PROJECT_STATUS,
		PROJECTS.PROJECT_COMPLETION_DATE
	FROM HABITAT_OUTCOMES
	LEFT JOIN HABITAT_PARCELS ON HABITAT_OUTCOMES.PARCEL_ID = HABITAT_PARCELS.ID
	LEFT JOIN PROJECTS ON HABITAT_PARCELS.PROJECT_ID = PROJECTS.ID
	LEFT JOIN HABITAT_TYPES ON HABITAT_OUTCOMES.HABITAT_TYPE = HABITAT_TYPES.ID
	LEFT JOIN CONSERVATION_PLANNING_AREAS ON PROJECTS.CPA = CONSERVATION_PLANNING_AREAS.ID
	LEFT JOIN PROJECT_STATUSES ON PROJECTS.PROJECT_STATUS = PROJECT_STATUSES.ID
	GROUP BY HABITAT_PARCELS.ID,
		HABITAT_PARCELS.ACRES,
		PROJECTS.PROJECT_NICKNAME,
		HABITAT_TYPES.LONG_FORM,
		HABITAT_TYPES.HABITAT_TYPE,
		HABITAT_TYPES.UNIT,
		CONSERVATION_PLANNING_AREAS.CPA_NAME,
		PROJECT_STATUSES.PROJECT_STATUS,
		PROJECTS.PROJECT_COMPLETION_DATE