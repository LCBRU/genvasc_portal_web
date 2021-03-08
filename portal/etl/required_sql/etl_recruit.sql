CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `etl_recruit` AS
SELECT
    `cs`.`name` AS `status`,
    `cids`.`nhs_number_1` AS `nhs_number`,
    `gen`.`genvasc_id_10` AS `study_id`,
    `gpCustom`.`practice_code_7` AS `practice_code`,
    `con`.`first_name` AS `first_name`,
    `con`.`last_name` AS `last_name`,
    `con`.`birth_date` AS `date_of_birth`,
    `con`.`id` AS `civicrm_contact_id`,
    `cas`.`id` AS `civicrm_case_id`,
    `cas`.`start_date` AS `recruited_date`,
    `inv`.`invoice_year_107` AS `invoice_year`,
    `inv`.`invoice_quarter_108` AS `invoice_quarter`,
    `inv`.`reimbursed_status_114` AS `reimbursed_status`
FROM
    (
        (
            (
                (
                    (
                        (
                            (
                                (
                                    `civicrmlive_docker4716`.`civicrm_case` `cas`
                                LEFT JOIN `civicrmlive_docker4716`.`civicrm_option_value` `cs` ON
                                    (
                                        (
                                            (
                                                `cs`.`value` = `cas`.`status_id`
                                            )
                                            AND (
                                                `cs`.`option_group_id` = 27
                                            )
                                        )
                                    )
                                )
                            JOIN `civicrmlive_docker4716`.`civicrm_case_contact` `cc` ON
                                (
                                    (
                                        `cc`.`case_id` = `cas`.`id`
                                    )
                                )
                            )
                        JOIN `civicrmlive_docker4716`.`civicrm_contact` `con` ON
                            (
                                (
                                    `con`.`id` = `cc`.`contact_id`
                                )
                            )
                        )
                    JOIN `civicrmlive_docker4716`.`civicrm_value_contact_ids_1` `cids` ON
                        (
                            (
                                `cids`.`entity_id` = `con`.`id`
                            )
                        )
                    )
                JOIN (
                        SELECT
                            DISTINCT `practiceRel`.`case_id` AS `case_id`,
                            `practiceRel`.`contact_id_b` AS `practice_id`
                        FROM
                            `civicrmlive_docker4716`.`civicrm_relationship` `practiceRel`
                        WHERE
                            (
                                (
                                    `practiceRel`.`relationship_type_id` = 24
                                )
                                AND (
                                    `practiceRel`.`is_active` = 1
                                )
                                AND (
                                    isnull(`practiceRel`.`end_date`)
                                    OR (
                                        `practiceRel`.`end_date` > curdate()
                                    )
                                )
                                AND (
                                    isnull(`practiceRel`.`start_date`)
                                    OR (
                                        `practiceRel`.`start_date` <= curdate()
                                    )
                                )
                            )
                    ) `cas_prac` ON
                    (
                        (
                            `cas_prac`.`case_id` = `cas`.`id`
                        )
                    )
                )
            JOIN `civicrmlive_docker4716`.`civicrm_value_gp_surgery_data_3` `gpCustom` ON
                (
                    (
                        `gpCustom`.`entity_id` = `cas_prac`.`practice_id`
                    )
                )
            )
        LEFT JOIN `civicrmlive_docker4716`.`civicrm_value_genvasc_recruitment_data_5` `gen` ON
            (
                (
                    `gen`.`entity_id` = `cas`.`id`
                )
            )
        )
    LEFT JOIN `civicrmlive_docker4716`.`civicrm_value_genvasc_invoice_data_25` `inv` ON
        (
            (
                `inv`.`entity_id` = `cas`.`id`
            )
        )
    )
WHERE
    (
        (
            `cas`.`case_type_id` = 3
        )
        AND (
            LENGTH(trim(COALESCE(`cids`.`nhs_number_1`, ''))) > 0
        )
        AND (
            `con`.`birth_date` IS NOT NULL
        )
    )