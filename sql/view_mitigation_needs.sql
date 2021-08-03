CREATE OR REPLACE VIEW view_mitigation_needs AS
	SELECT
		permits.permit_name,
		mitigation_needs.quantity,
		mitigation_types.unit,
		mitigation_types.mitigation_type,
		mitigation_types.long_form,
		mitigation_needs.needed_by
	FROM mitigation_needs
	JOIN permits on mitigation_needs.permit = permits.id
	JOIN mitigation_types on mitigation_needs.mitigation_type = mitigation_types.id;