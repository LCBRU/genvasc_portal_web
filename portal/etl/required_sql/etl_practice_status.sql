ALTER VIEW etl_practice_status AS
SELECT
	value AS id,
	name
FROM redcap6170_briccsext.LCBRU_Enums
WHERE project_id= 53
	AND field_name = 'status'
