CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `etl_practice_groups_practices` AS
SELECT
    `x`.`practice_code` AS `practice_code`,
    'Management Area' AS `practice_group_type`,
    `x`.`project_id` AS `practice_group_project_id`,
    `x`.`project_id` AS `practice_group_identifier`
FROM
    (
        SELECT
            `rd`.`project_id` AS `project_id`,
            group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'practice_code') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `practice_code`
        FROM
            `redcap_genvasc`.`redcap_data` `rd`
        WHERE
            (
                (
                    `rd`.`project_id` IN (
                        16, 15
                    )
                )
                AND (
                    `rd`.`field_name` = 'practice_code'
                )
            )
        GROUP BY
            `rd`.`project_id`,
            `rd`.`record`
    ) `x`
WHERE
    (
        `x`.`project_id` IS NOT NULL
    )
UNION
SELECT
    `x`.`practice_code` AS `practice_code`,
    'CCG' AS `practice_group_type`,
    `x`.`project_id` AS `practice_group_project_id`,
    `x`.`ccg` AS `practice_group_identifier`
FROM
    (
        SELECT
            `rd`.`project_id` AS `project_id`,
            group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'practice_code') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `practice_code`,
            group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'ccg') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `ccg`
        FROM
            `redcap_genvasc`.`redcap_data` `rd`
        WHERE
            (
                (
                    `rd`.`project_id` IN (
                        16, 15
                    )
                )
                AND (
                    `rd`.`field_name` IN (
                        'practice_code', 'ccg'
                    )
                )
            )
        GROUP BY
            `rd`.`project_id`,
            `rd`.`record`
    ) `x`
WHERE
    (
        `x`.`ccg` IS NOT NULL
    )
UNION
SELECT
    `x`.`practice_code` AS `practice_code`,
    'Federation' AS `practice_group_type`,
    `x`.`project_id` AS `practice_group_project_id`,
    `x`.`federation` AS `practice_group_identifier`
FROM
    (
        SELECT
            `rd`.`project_id` AS `project_id`,
            group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'practice_code') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `practice_code`,
            group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'federation') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `federation`
        FROM
            `redcap_genvasc`.`redcap_data` `rd`
        WHERE
            (
                (
                    `rd`.`project_id` IN (
                        16, 15
                    )
                )
                AND (
                    `rd`.`field_name` IN (
                        'practice_code', 'federation'
                    )
                )
            )
        GROUP BY
            `rd`.`project_id`,
            `rd`.`record`
    ) `x`
WHERE
    (
        `x`.`federation` IS NOT NULL
    )