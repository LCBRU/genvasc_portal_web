CREATE OR ALTER VIEW genvasc_gp_portal.etl_exclusion_reason AS
SELECT
    casa.case_id,
    GROUP_CONCAT(COALESCE(a.details, '')) details
FROM civicrmlive_docker4716.civicrm_case_activity casa
join civicrmlive_docker4716.civicrm_activity a
    on a.id = casa.activity_id 
    and a.activity_type_id = 16
    AND a.details IS NOT NULL
    AND a.is_deleted = 0
    AND a.subject LIKE '%to Excluded'
GROUP BY casa.case_id
;