CREATE VIEW etl_portal_practice AS
SELECT
	project_id,
	GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'practice_code' THEN VALUE ELSE NULL END) AS practice_code,
	GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'practice_name' THEN VALUE ELSE NULL END) AS practice_name,
	GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'ccg' THEN VALUE ELSE NULL END) AS ccg,
	GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'practice_address' THEN VALUE ELSE NULL END) AS practice_address,
	GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'pract_town' THEN VALUE ELSE NULL END) AS pract_town,
	GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'city' THEN VALUE ELSE NULL END) AS city,
	GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'county' THEN VALUE ELSE NULL END) AS county,
	GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'postcode' THEN VALUE ELSE NULL END) AS postcode,
	GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'federation' THEN VALUE ELSE NULL END) AS federation,
	GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'partners' THEN VALUE ELSE NULL END) AS partners,
	COALESCE(GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'genvasc_initiated' THEN VALUE ELSE NULL END), 0) AS genvasc_initiated,
	COALESCE(GROUP_CONCAT(DISTINCT CASE WHEN field_name = 'status' THEN VALUE ELSE NULL END), 0) AS status
FROM redcap_data rd
WHERE
		project_id IN (29, 53)
	AND field_name IN (
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
