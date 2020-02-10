CREATE VIEW etl_practice_status AS
SELECT
	value AS id,
	name
FROM redcap6170_briccsext.LCBRU_Enums
WHERE project_id IN (53)
	AND field_name = 'status'
