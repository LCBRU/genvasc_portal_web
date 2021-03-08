CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `etl_practice_group` AS
SELECT
    `rp`.`project_id` AS `project_id`,
    `rp`.`project_id` AS `identifier`,
    'Management Area' AS `type`,
    `rp`.`app_title` AS `name`
FROM
    `redcap_genvasc`.`redcap_projects` `rp`
WHERE
    (
        `rp`.`project_id` IN (
            16, 15
        )
    )
UNION
SELECT
    `LCBRU_Enums`.`project_id` AS `project_id`,
    `LCBRU_Enums`.`value` AS `identifier`,
    'CCG' AS `type`,
    `LCBRU_Enums`.`name` AS `name`
FROM
    `redcap_genvasc`.`LCBRU_Enums`
WHERE
    (
        (
            `LCBRU_Enums`.`project_id` IN (
                16, 15
            )
        )
        AND (
            `LCBRU_Enums`.`field_name` = 'ccg'
        )
    )
UNION
SELECT
    `LCBRU_Enums`.`project_id` AS `project_id`,
    `LCBRU_Enums`.`value` AS `identifier`,
    'Federation' AS `type`,
    `LCBRU_Enums`.`name` AS `name`
FROM
    `redcap_genvasc`.`LCBRU_Enums`
WHERE
    (
        (
            `LCBRU_Enums`.`project_id` IN (
                16, 15
            )
        )
        AND (
            `LCBRU_Enums`.`field_name` = 'federation'
        )
    )