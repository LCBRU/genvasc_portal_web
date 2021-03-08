CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `etl_practice_status` AS
SELECT
    `LCBRU_Enums`.`value` AS `id`,
    `LCBRU_Enums`.`name` AS `name`
FROM
    `redcap_genvasc`.`LCBRU_Enums`
WHERE
    (
        (
            `LCBRU_Enums`.`project_id` = 15
        )
        AND (
            `LCBRU_Enums`.`field_name` = 'status'
        )
    )