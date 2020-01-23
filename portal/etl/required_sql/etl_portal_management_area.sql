CREATE VIEW etl_portal_management_area AS

SELECT
	project_id,
	app_title AS name
FROM redcap_projects
WHERE project_id IN (29, 53)
;
