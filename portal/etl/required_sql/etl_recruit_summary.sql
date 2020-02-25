ALTER VIEW genvasc_gp_portal.etl_recruit_summary AS
SELECT
	practice_code,
	recruited,
	excluded,
	withdrawn,
	last_recruited_date,
	CASE WHEN recruited > 0 THEN excluded / recruited * 100 END excluded_percentage,
	CASE WHEN recruited > 0 THEN withdrawn / recruited * 100 END withdrawn_percentage
FROM (
	select
		gpCustom.practice_code_7 AS practice_code,
		COUNT(cas.id) recruited,
		SUM(CASE WHEN cas.status_id = 9 THEN 1 ELSE 0 END) excluded,
		SUM(CASE WHEN cas.status_id = 8 THEN 1 ELSE 0 END) withdrawn,
		MAX(cas.start_date) AS last_recruited_date
	from civicrmlive_docker4716.civicrm_case cas
	join civicrmlive_docker4716.civicrm_case_contact cc
		on cc.case_id = cas.id
	join civicrmlive_docker4716.civicrm_contact con
		on con.id = cc.contact_id
		AND con.is_deleted = 0
	join civicrmlive_docker4716.civicrm_value_contact_ids_1 cids
		on cids.entity_id = con.id
	join (
	    select
	        distinct practiceRel.case_id AS case_id,
	        practiceRel.contact_id_b AS practice_id
	    from
	        civicrmlive_docker4716.civicrm_relationship practiceRel
	    where
	        	practiceRel.relationship_type_id = 24
	        and practiceRel.is_active = 1
	        and (isnull(practiceRel.end_date) or practiceRel.end_date > curdate())
	        and (isnull(practiceRel.start_date) or practiceRel.start_date <= curdate())
	    ) cas_prac
	    on cas_prac.case_id = cas.id
	join civicrmlive_docker4716.civicrm_value_gp_surgery_data_3 gpCustom
		on gpCustom.entity_id = cas_prac.practice_id
	where
	    cas.case_type_id = 3
	    AND cas.is_deleted = 0
	GROUP BY gpCustom.practice_code_7
) x
;