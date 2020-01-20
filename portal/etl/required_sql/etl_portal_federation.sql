CREATE VIEW etl_portal_federation AS

SELECT
	project_id,
	value AS federation_id,
	name
FROM LCBRU_Enums
WHERE project_id IN (29, 53)
	AND field_name = 'federation'
