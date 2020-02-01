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
		COALESCE(GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'genvasc_initiated' THEN rd.value ELSE NULL END), 0) AS genvasc_initiated,
		COALESCE(GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'status' THEN rd.value ELSE NULL END), 0) AS status
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
			'status'
		)
	GROUP BY rd.project_id, rd.record
;
