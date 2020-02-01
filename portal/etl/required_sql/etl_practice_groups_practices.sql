CREATE VIEW etl_practice_groups_practices AS

SELECT
	practice_code,
	(project_id * 1000000) + (0 * 1000) + project_id AS practice_group_id
FROM (
	SELECT
		project_id,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'practice_code' THEN rd.value ELSE NULL END) AS practice_code
	FROM redcap6170_briccsext.redcap_data rd
	WHERE
			project_id IN (29, 53)
		AND rd.field_name IN (
			'practice_code'
		)
	GROUP BY rd.project_id, rd.record
) x
WHERE x.project_id IS NOT NULL

UNION

SELECT
	practice_code,
	(project_id * 1000000) + (1 * 1000) + ccg AS practice_group_id
FROM (
	SELECT
		project_id,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'practice_code' THEN rd.value ELSE NULL END) AS practice_code,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'ccg' THEN rd.value ELSE NULL END) AS ccg
	FROM redcap6170_briccsext.redcap_data rd
	WHERE
			project_id IN (29, 53)
		AND rd.field_name IN (
			'practice_code',
			'ccg'
		)
	GROUP BY rd.project_id, rd.record
) x
WHERE x.ccg IS NOT NULL

UNION

SELECT
	practice_code,
	(project_id * 1000000) + (2 * 1000) + federation AS practice_group_id
FROM (
	SELECT
		project_id,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'practice_code' THEN rd.value ELSE NULL END) AS practice_code,
		GROUP_CONCAT(DISTINCT CASE WHEN rd.field_name = 'federation' THEN rd.value ELSE NULL END) AS federation
	FROM redcap6170_briccsext.redcap_data rd
	WHERE
			project_id IN (29, 53)
		AND rd.field_name IN (
			'practice_code',
			'federation'
		)
	GROUP BY rd.project_id, rd.record
) x
WHERE x.federation IS NOT NULL

;
