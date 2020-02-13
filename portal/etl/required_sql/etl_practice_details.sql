ALTER VIEW etl_practice_detail AS
	SELECT
		project_id,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'practice_code' THEN rd.value ELSE NULL END) AS code,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'practice_name' THEN rd.value ELSE NULL END) AS name,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'ccg' THEN rd.value ELSE NULL END) AS ccg,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'practice_address' THEN rd.value ELSE NULL END) AS street_address,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'pract_town' THEN rd.value ELSE NULL END) AS town,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'city' THEN rd.value ELSE NULL END) AS city,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'county' THEN rd.value ELSE NULL END) AS county,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'postcode' THEN rd.value ELSE NULL END) AS postcode,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'federation' THEN rd.value ELSE NULL END) AS federation,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'partners' THEN rd.value ELSE NULL END) AS partners,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'collab_ag_comp_yn' THEN rd.value ELSE NULL END) AS collab_ag_comp_yn,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'collab_ag_signed_date' THEN rd.value ELSE NULL END) AS collab_ag_signed_date,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'isa_comp_yn' THEN rd.value ELSE NULL END) AS isa_comp_yn,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'isa_1_signed_date' THEN rd.value ELSE NULL END) AS isa_1_signed_date,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'isa_1_caldicott_guard_end' THEN rd.value ELSE NULL END) AS isa_1_caldicott_guard_end,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'agree_66_comp_yn' THEN rd.value ELSE NULL END) AS agree_66_comp_yn,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'agree_66_signed_date_1' THEN rd.value ELSE NULL END) AS agree_66_signed_date_1,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'agree_66_end_date_2' THEN rd.value ELSE NULL END) AS agree_66_end_date_2,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'genvasc_initiated' THEN rd.value ELSE NULL END) AS genvasc_initiated,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'status' THEN rd.value ELSE NULL END) AS status_id
	FROM redcap6170_briccsext.redcap_data rd
	WHERE
			project_id IN (29, 53)
		AND rd.field_name IN (
			'practice_code',
			'ccg',
			'practice_name',
			'practice_address',
			'pract_town',
			'city',
			'county',
			'postcode',
			'federation',
			'partners',
			'genvasc_initiated',
			'status',
			'collab_ag_comp_yn',
			'collab_ag_signed_date',
			'isa_comp_yn',
			'isa_1_signed_date',
			'isa_1_caldicott_guard_end',
			'agree_66_comp_yn',
			'agree_66_signed_date_1',
			'agree_66_end_date_2'
		)
	GROUP BY rd.project_id, rd.record
;
