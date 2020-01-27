CREATE TABLE IF NOT EXISTS lbrc_recruitment_audit (
    case_id INT NOT NULL  PRIMARY KEY,
    last_change_timestamp TIMESTAMP NOT NULL
);

DELIMITER $$

CREATE TRIGGER trg_civicrm_case_insert
    AFTER INSERT
    ON civicrm_case FOR EACH ROW
    BEGIN
	    
	   INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
	   VALUES (NEW.id, CURRENT_TIMESTAMP)
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$

CREATE TRIGGER trg_civicrm_case_update
    AFTER UPDATE
    ON civicrm_case FOR EACH ROW
    BEGIN
	    
	   INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
	   VALUES (NEW.id, CURRENT_TIMESTAMP)
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$
	
CREATE TRIGGER trg_civicrm_case_delete
    AFTER DELETE
    ON civicrm_case FOR EACH ROW
    BEGIN
	    
	   INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
	   VALUES (OLD.id, CURRENT_TIMESTAMP)
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$
	

CREATE TRIGGER trg_civicrm_value_genvasc_invoice_data_25_insert
    AFTER INSERT
    ON civicrm_value_genvasc_invoice_data_25 FOR EACH ROW
    BEGIN
	    
	   INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
	   VALUES (NEW.entity_id, CURRENT_TIMESTAMP)
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$
	
CREATE TRIGGER trg_civicrm_value_genvasc_invoice_data_25_update
    AFTER UPDATE
    ON civicrm_value_genvasc_invoice_data_25 FOR EACH ROW
    BEGIN
	    
	   INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
	   VALUES (NEW.entity_id, CURRENT_TIMESTAMP)
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$
	
CREATE TRIGGER trg_civicrm_value_genvasc_invoice_data_25_delete
    AFTER DELETE
    ON civicrm_value_genvasc_invoice_data_25 FOR EACH ROW
    BEGIN
	    
	   INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
	   VALUES (OLD.entity_id, CURRENT_TIMESTAMP)
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$
	
CREATE TRIGGER trg_civicrm_value_genvasc_recruitment_data_5_insert
    AFTER INSERT
    ON civicrm_value_genvasc_recruitment_data_5 FOR EACH ROW
    BEGIN
	    
	   INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
	   VALUES (NEW.entity_id, CURRENT_TIMESTAMP)
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$
	
CREATE TRIGGER trg_civicrm_value_genvasc_recruitment_data_5_update
    AFTER UPDATE
    ON civicrm_value_genvasc_recruitment_data_5 FOR EACH ROW
    BEGIN
	    
	   INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
	   VALUES (NEW.entity_id, CURRENT_TIMESTAMP)
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$
	
CREATE TRIGGER trg_civicrm_value_genvasc_recruitment_data_5_delete
    AFTER DELETE
    ON civicrm_value_genvasc_recruitment_data_5 FOR EACH ROW
    BEGIN
	    
	   INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
	   VALUES (OLD.entity_id, CURRENT_TIMESTAMP)
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$
	
CREATE TRIGGER trg_civicrm_contact_insert
    AFTER INSERT
    ON civicrm_contact FOR EACH ROW
    BEGIN
	    
		INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
		SELECT ccc.case_id , CURRENT_TIMESTAMP
		FROM civicrm_case_contact ccc
		JOIN civicrm_case cas
			ON cas.id = ccc.case_id
		WHERE cas.case_type_id = 3
			AND ccc.contact_id = NEW.id
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$

CREATE TRIGGER trg_civicrm_contact_update
    AFTER UPDATE
    ON civicrm_contact FOR EACH ROW
    BEGIN
	    
		INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
		SELECT ccc.case_id , CURRENT_TIMESTAMP
		FROM civicrm_case_contact ccc
		JOIN civicrm_case cas
			ON cas.id = ccc.case_id
		WHERE cas.case_type_id = 3
			AND ccc.contact_id = NEW.id
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$
	
CREATE TRIGGER trg_civicrm_contact_delete
    AFTER DELETE
    ON civicrm_contact FOR EACH ROW
    BEGIN
	    
		INSERT INTO lbrc_recruitment_audit (case_id, last_change_timestamp)
		SELECT ccc.case_id , CURRENT_TIMESTAMP
		FROM civicrm_case_contact ccc
		JOIN civicrm_case cas
			ON cas.id = ccc.case_id
		WHERE cas.case_type_id = 3
			AND ccc.contact_id = OLD.id
	   ON DUPLICATE KEY UPDATE last_change_timestamp=CURRENT_TIMESTAMP;
	    
	END$$

DELIMITER ;

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
    ,  CURRENT_TIMESTAMP AS last_update_timestamp
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
     , au.last_change_timestamp AS last_update_timestamp
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
  LEFT JOIN lbrc_recruitment_audit au
  	ON au.case_id = cas.id
  WHERE cas.case_type_id = 3 -- GENVASC_CASE_TYPE
      AND LENGTH(TRIM(COALESCE(cids.nhs_number_1, ''))) > 0
      AND con.birth_date IS NOT NULL
;