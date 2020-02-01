CREATE VIEW etl_practice_group AS

SELECT
	(project_id * 1000000) + (0 * 1000) + project_id AS id,
	'Management Area' AS type,
	app_title AS name
FROM redcap6170_briccsext.redcap_projects rp 
WHERE project_id IN (29, 53)

UNION

SELECT
	(project_id * 1000000) + (1 * 1000) + value AS id,
	'CCG' AS type,
	name
FROM redcap6170_briccsext.LCBRU_Enums
WHERE project_id IN (29, 53)
	AND field_name = 'ccg'

UNION

SELECT
	(project_id * 1000000) + (2 * 1000) + value AS id,
	'Federation' AS type,
	name
FROM redcap6170_briccsext.LCBRU_Enums
WHERE project_id IN (29, 53)
	AND field_name = 'federation'
