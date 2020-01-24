CREATE VIEW etl_portal_recruits AS

SELECT DISTINCT
      gr.id AS processing_id
    , 'Awaiting processing' AS status
    , gr.nhs_number COLLATE utf8_unicode_ci AS nhs_number
    , NULL AS study_id
    , gpCustom.practice_code_7 AS practice_code
    , NULL AS first_name
    , NULL AS last_name
    , gr.dob AS date_of_birth
    , gr.contact_id AS civicrm_contact_id
    , gr.case_id AS civicrm_case_id
    , NULL AS processed_by
    , NULL AS processed_date
    , gr.date_recruited AS recruited_date
    , NULL AS invoice_year
    , NULL AS invoice_quarter
    , NULL AS reimbursed_status
FROM drupallive_docker4716.genvasc_portal_recruits gr
JOIN civicrm_value_gp_surgery_data_3 gpCustom ON gpCustom.entity_id = gr.practice_id
WHERE gr.case_id IS NULL
    AND gr.delete_reason IS NULL
    AND gr.date_processed IS NULL

UNION

SELECT DISTINCT
       NULL AS processing_id
     , cs.name AS status
     , cids.nhs_number_1 AS nhs_number
     , gen.genvasc_id_10 AS study_id
     , gpCustom.practice_code_7 AS practice_code
     , con.first_name AS first_name
     , con.last_name AS last_name
     , con.birth_date AS date_of_birth
     , con.id AS civicrm_contact_id
     , cas.id AS civicrm_case_id
     , rel_c.display_name AS processed_by
     , COALESCE(rel_r.start_date, cas.start_date) AS processed_date
     , cas.start_date AS recruited_date
     , inv.invoice_year_107 AS invoice_year
     , inv.invoice_quarter_108 AS invoice_quarter
     , inv.reimbursed_status_114 AS reimbursed_status
  FROM civicrm_case cas
  LEFT JOIN civicrm_option_value cs ON cs.value = cas.status_id
        AND cs.option_group_id = 27 -- CASE_STATUS_GROUP_ID
  JOIN civicrm_case_contact cc ON cc.case_id = cas.id
  JOIN civicrm_contact con ON con.id = cc.contact_id 
  JOIN civicrm_value_contact_ids_1 cids ON cids.entity_id = con.id
  JOIN civicrm_relationship practiceRel ON practiceRel.case_id = cas.id
        AND practiceRel.relationship_type_id = 24 -- RECRUITING_SITE_RELATIONSHIP_TYPE
        AND practiceRel.is_active = 1
        AND ( practiceRel.end_date IS NULL OR practiceRel.end_date > CURDATE())
        AND ( practiceRel.start_date IS NULL OR practiceRel.start_date <= CURDATE())
  JOIN civicrm_value_gp_surgery_data_3 gpCustom ON gpCustom.entity_id = practiceRel.contact_id_b
  LEFT JOIN civicrm_value_genvasc_recruitment_data_5 gen ON gen.entity_id = cas.id
  LEFT JOIN civicrm_relationship rel_r ON rel_r.case_id = cas.id
        AND rel_r.relationship_type_id = 21 -- RECRUITER_RELATIONSHIP_TYPE 
        AND rel_r.is_active = 1
        AND ( rel_r.end_date IS NULL OR rel_r.end_date >= CURDATE())
        AND ( rel_r.start_date IS NULL OR rel_r.start_date <= CURDATE())
  LEFT JOIN civicrm_contact rel_c ON rel_c.id = rel_r.contact_id_b
  LEFT JOIN civicrm_value_genvasc_invoice_data_25 inv ON inv.entity_id = cas.id
  WHERE cas.case_type_id = 3 -- GENVASC_CASE_TYPE
      AND LENGTH(TRIM(COALESCE(cids.nhs_number_1, ''))) > 0
      AND con.birth_date IS NOT NULL
;