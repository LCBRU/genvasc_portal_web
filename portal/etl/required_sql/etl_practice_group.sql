ALTER VIEW etl_practice_group AS

SELECT
	project_id,
	project_id AS identifier,
	'Management Area' AS type,
	app_title AS name
FROM redcap6170_briccsext.redcap_projects rp 
WHERE project_id IN (29, 53)

UNION

SELECT
	project_id,
	value AS identifier,
	'CCG' AS type,
	name
FROM redcap6170_briccsext.LCBRU_Enums
WHERE project_id IN (29, 53)
	AND field_name = 'ccg'

UNION

SELECT
	project_id,
	value AS identifier,
	'Federation' AS type,
	name
FROM redcap6170_briccsext.LCBRU_Enums
WHERE project_id IN (29, 53)
	AND field_name = 'federation'
