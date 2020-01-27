CREATE VIEW etl_portal_practice AS
SELECT
	p.project_id,
	p.practice_code,
	p.practice_name,
	p.ccg,
	p.practice_address,
	p.pract_town,
	p.city,
	p.county,
	p.postcode,
	p.federation,
	p.partners,
	p.genvasc_initiated,
	p.status,
	ts.last_update_timestamp
FROM (
	SELECT
		project_id,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'practice_code' THEN rd.value ELSE NULL END) AS practice_code,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'practice_name' THEN rd.value ELSE NULL END) AS practice_name,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'ccg' THEN rd.value ELSE NULL END) AS ccg,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'practice_address' THEN rd.value ELSE NULL END) AS practice_address,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'pract_town' THEN rd.value ELSE NULL END) AS pract_town,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'city' THEN rd.value ELSE NULL END) AS city,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'county' THEN rd.value ELSE NULL END) AS county,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'postcode' THEN rd.value ELSE NULL END) AS postcode,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'federation' THEN rd.value ELSE NULL END) AS federation,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'partners' THEN rd.value ELSE NULL END) AS partners,
		COALESCE(GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'genvasc_initiated' THEN rd.value ELSE NULL END), 0) AS genvasc_initiated,
		COALESCE(GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'status' THEN rd.value ELSE NULL END), 0) AS status
	FROM redcap_data rd
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
) p
LEFT JOIN (
	SELECT
		pk as record,
		project_id,
		MAX(COALESCE(ts, 0)) AS last_update_timestamp
	FROM redcap_log_event
	WHERE event NOT IN ('DATA_EXPORT', 'DELETE')
	    # Ignore events caused by the data import from
	    # the mobile app
	    AND page NOT IN ('DataImportController:index')
	    AND project_id IN (29, 53)
	  	AND object_type = 'redcap_data'
	GROUP BY pk, project_id
 ) ts ON ts.record = p.practice_code
 	AND ts.project_id = p.project_id
;
