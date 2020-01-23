CREATE VIEW etl_portal_user AS
SELECT
	project_id,
	practice_code,
	email,
	MAX(current_portal_user_yn) AS current_portal_user_yn,
	MAX(gv_end_del_log) AS gv_end_del_log
FROM (

	SELECT DISTINCT
		e.project_id,
		p.value AS practice_code,
		e.value AS email,
		1 AS current_portal_user_yn,
		NULL AS gv_end_del_log
	FROM    redcap_data e
	JOIN	redcap_data p
		ON p.project_id = e.project_id
		AND p.record = e.record
		AND p.field_name = 'practice_code'
	WHERE e.project_id IN (29, 53)
	    AND e.field_name IN (
	        'practice_manager_email',
	        'sen_part_email',
	        'pi_email_add'
	    )
	  
	 UNION 
	 
	 SELECT DISTINCT
		e.project_id,
		p.value AS practice_code,
		e.value AS contact_email_add,
		COALESCE(pu.value, 0) AS current_portal_user_yn,
		ed.value AS gv_end_del_log
	FROM redcap_data e
	JOIN redcap_data p
		ON p.project_id = e.project_id
		AND p.record = e.record
		AND p.field_name = 'practice_code'
	LEFT JOIN redcap_data pu
		ON pu.project_id = e.project_id
		AND pu.record = e.record
		AND COALESCE(pu.`instance`, 0) = COALESCE(e.`instance`, 0)
		AND pu.field_name = 'current_portal_user_yn'
	LEFT JOIN redcap_data ed
		ON ed.project_id = e.project_id
		AND ed.record = e.record
		AND COALESCE(ed.`instance`, 0) = COALESCE(e.`instance`, 0)
		AND pu.field_name = 'gv_end_del_log'
	WHERE e.project_id IN (29, 53)
		AND e.field_name = 'contact_email_add'
) x
GROUP BY project_id,
	practice_code,
	email
;