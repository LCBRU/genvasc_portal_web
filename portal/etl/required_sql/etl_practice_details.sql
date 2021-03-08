CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `etl_practice_detail` AS
SELECT
    `rd`.`project_id` AS `project_id`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'practice_code') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `code`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'practice_name') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `name`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'ccg') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `ccg`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'practice_address') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `street_address`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'pract_town') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `town`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'city') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `city`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'county') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `county`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'postcode') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `postcode`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'federation') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `federation`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'partners') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `partners`,
    (
        CASE
            WHEN (
                group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'collab_ag_comp_yn') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') = '1'
            ) THEN TRUE
            ELSE FALSE
        END
    ) AS `collab_ag_comp_yn`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'collab_ag_signed_date') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `collab_ag_signed_date_str`,
    (
        CASE
            WHEN (
                group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'isa_comp_yn') THEN (`rd`.`value` = '1') ELSE NULL END) SEPARATOR ',') = '1'
            ) THEN TRUE
            ELSE FALSE
        END
    ) AS `isa_comp_yn`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'isa_1_signed_date') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `isa_1_signed_date_str`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'isa_1_caldicott_guard_end') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `isa_1_caldicott_guard_end_str`,
    (
        CASE
            WHEN (
                group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'agree_66_comp_yn') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') = '1'
            ) THEN TRUE
            ELSE FALSE
        END
    ) AS `agree_66_comp_yn`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'agree_66_signed_date_1') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `agree_66_signed_date_1_str`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'agree_66_end_date_2') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `agree_66_end_date_2_str`,
    (
        CASE
            WHEN (
                group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'genvasc_initiated') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') = '1'
            ) THEN TRUE
            ELSE FALSE
        END
    ) AS `genvasc_initiated`,
    group_concat(DISTINCT (CASE WHEN (`rd`.`field_name` = 'status') THEN `rd`.`value` ELSE NULL END) SEPARATOR ',') AS `status_id`
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
                'practice_code', 'ccg', 'practice_name', 'practice_address', 'pract_town', 'city', 'county', 'postcode', 'federation', 'partners', 'genvasc_initiated', 'status', 'collab_ag_comp_yn', 'collab_ag_signed_date', 'isa_comp_yn', 'isa_1_signed_date', 'isa_1_caldicott_guard_end', 'agree_66_comp_yn', 'agree_66_signed_date_1', 'agree_66_end_date_2'
            )
        )
    )
GROUP BY
    `rd`.`project_id`,
    `rd`.`record`