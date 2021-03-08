CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `etl_recruit_summary` AS
SELECT
    `x`.`practice_id` AS `practice_id`,
    `x`.`practice_code` AS `practice_code`,
    `x`.`recruited` AS `recruited`,
    `x`.`excluded` AS `excluded`,
    `x`.`withdrawn` AS `withdrawn`,
    `x`.`last_recruited_date` AS `last_recruited_date`,
    (
        CASE
            WHEN (
                `x`.`recruited` > 0
            ) THEN (
                (
                    `x`.`excluded` / `x`.`recruited`
                ) * 100
            )
        END
    ) AS `excluded_percentage`,
    (
        CASE
            WHEN (
                `x`.`recruited` > 0
            ) THEN (
                (
                    `x`.`withdrawn` / `x`.`recruited`
                ) * 100
            )
        END
    ) AS `withdrawn_percentage`
FROM
    (
        SELECT
            `prac`.`practice_id` AS `practice_id`,
            `prac`.`practice_code` AS `practice_code`,
            count(`prac`.`civicrm_case_id`) AS `recruited`,
            sum((CASE WHEN (`cas`.`status_id` = 9) THEN 1 ELSE 0 END)) AS `excluded`,
            sum((CASE WHEN (`cas`.`status_id` = 8) THEN 1 ELSE 0 END)) AS `withdrawn`,
            max(`cas`.`start_date`) AS `last_recruited_date`
        FROM
            (
                (
                    (
                        SELECT
                            DISTINCT `practiceRel`.`case_id` AS `civicrm_case_id`,
                            `practiceRel`.`contact_id_b` AS `practice_id`,
                            `gpCustom`.`practice_code_7` AS `practice_code`
                        FROM
                            (
                                (
                                    (
                                        `civicrmlive_docker4716`.`civicrm_relationship` `practiceRel`
                                    JOIN `civicrmlive_docker4716`.`civicrm_value_gp_surgery_data_3` `gpCustom` ON
                                        (
                                            (
                                                `gpCustom`.`entity_id` = `practiceRel`.`contact_id_b`
                                            )
                                        )
                                    )
                                JOIN `civicrmlive_docker4716`.`civicrm_case_contact` `cc` ON
                                    (
                                        (
                                            `cc`.`case_id` = `practiceRel`.`case_id`
                                        )
                                    )
                                )
                            JOIN `civicrmlive_docker4716`.`civicrm_contact` `con` ON
                                (
                                    (
                                        (
                                            `con`.`id` = `cc`.`contact_id`
                                        )
                                        AND (
                                            `con`.`is_deleted` = 0
                                        )
                                    )
                                )
                            )
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
                    )
                ) `prac`
            JOIN `civicrmlive_docker4716`.`civicrm_case` `cas` ON
                (
                    (
                        (
                            `cas`.`id` = `prac`.`civicrm_case_id`
                        )
                        AND (
                            `cas`.`is_deleted` = 0
                        )
                        AND (
                            `cas`.`case_type_id` = 3
                        )
                    )
                )
            )
        GROUP BY
            `prac`.`practice_id`,
            `prac`.`practice_code`
    ) `x`