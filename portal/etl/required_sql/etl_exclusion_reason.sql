CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `etl_exclusion_reason` AS
SELECT
    `casa`.`case_id` AS `civicrm_case_id`,
    group_concat(COALESCE(`a`.`details`, '') SEPARATOR ',') AS `details`
FROM
    (
        `civicrmlive_docker4716`.`civicrm_case_activity` `casa`
    JOIN `civicrmlive_docker4716`.`civicrm_activity` `a` ON
        (
            (
                (
                    `a`.`id` = `casa`.`activity_id`
                )
                AND (
                    `a`.`activity_type_id` = 16
                )
                AND (
                    `a`.`details` IS NOT NULL
                )
                AND (
                    `a`.`is_deleted` = 0
                )
                AND (
                    `a`.`subject` LIKE '%to Excluded'
                )
            )
        )
    )
GROUP BY
    `casa`.`case_id`