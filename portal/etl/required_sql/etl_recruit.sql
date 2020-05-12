ALTER VIEW genvasc_gp_portal.etl_recruit AS
select
    cs.name AS status,
    cids.nhs_number_1 AS nhs_number,
    gen.genvasc_id_10 AS study_id,
    gpCustom.practice_code_7 AS practice_code,
    con.first_name AS first_name,
    con.last_name AS last_name,
    con.birth_date AS date_of_birth,
    con.id AS civicrm_contact_id,
    cas.id AS civicrm_case_id,
    cas.start_date AS recruited_date,
    inv.invoice_year_107 AS invoice_year,
    inv.invoice_quarter_108 AS invoice_quarter,
    inv.reimbursed_status_114 AS reimbursed_status
from civicrmlive_docker4716.civicrm_case cas
left join civicrmlive_docker4716.civicrm_option_value cs
	on cs.value = cas.status_id
	and cs.option_group_id = 27
join civicrmlive_docker4716.civicrm_case_contact cc
	on cc.case_id = cas.id
join civicrmlive_docker4716.civicrm_contact con
	on con.id = cc.contact_id
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
left join civicrmlive_docker4716.civicrm_value_genvasc_recruitment_data_5 gen
	on gen.entity_id = cas.id
left join civicrmlive_docker4716.civicrm_value_genvasc_invoice_data_25 inv
	on inv.entity_id = cas.id
where
    cas.case_type_id = 3
    and length(trim(coalesce(cids.nhs_number_1, ''))) > 0
    and con.birth_date is not null
;