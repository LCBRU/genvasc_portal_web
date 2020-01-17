CREATE VIEW etl_portal_ccg AS

SELECT
	project_id,
	value AS ccg_id,
	name
FROM LCBRU_Enums
WHERE project_id IN (29, 53)
	AND field_name = 'ccg'
