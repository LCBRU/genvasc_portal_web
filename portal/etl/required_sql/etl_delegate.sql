CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `etl_delegate` AS
SELECT
    (
        `contacts`.`record`
    ) AS `practice_code`,
    `contacts`.`instance` AS `instance`,
    COALESCE(`contacts`.`name`, '') AS `name`,
    COALESCE(`roles`.`role_name`, `contacts`.`gv_role_other`) AS `role`,
    `contacts`.`gcp_trained` AS `gcp_trained`,
    `contacts`.`gv_trained` AS `gv_trained`,
    `contacts`.`on_delegation_log_yn` AS `on_delegation_log_yn`,
    `contacts`.`gv_start_del_log` AS `gv_start_del_log`,
    `contacts`.`gv_end_del_log` AS `gv_end_del_log`,
    `contacts`.`rsn_not_on_del_log` AS `rsn_not_on_del_log`,
    `contacts`.`gv_phone_a` AS `gv_phone_a`,
    `contacts`.`gv_phone_b` AS `gv_phone_b`,
    (
        lower(`contacts`.`contact_email_add`)
    ) AS `contact_email_add`,
    `contacts`.`primary_contact_yn` AS `primary_contact_yn`
FROM
    (
        (
            (
                SELECT
                    `x`.`record` AS `record`,
                    `x`.`project_id` AS `project_id`,
                    `x`.`instance` AS `instance`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'gv_contact') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `name`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'gv_role') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `role`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'gv_role_other') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `gv_role_other`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'gcp_trained') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `gcp_trained`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'gv_trained') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `gv_trained`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'on_delegation_log_yn') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `on_delegation_log_yn`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'gv_start_del_log') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `gv_start_del_log`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'gv_end_del_log') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `gv_end_del_log`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'rsn_not_on_del_log') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `rsn_not_on_del_log`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'gv_phone_a') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `gv_phone_a`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'gv_phone_b') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `gv_phone_b`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'contact_email_add') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `contact_email_add`,
                    group_concat((CASE WHEN (`x`.`field_name` = 'primary_contact_yn') THEN `x`.`value` ELSE NULL END) SEPARATOR ',') AS `primary_contact_yn`
                FROM
                    (
                        SELECT
                            DISTINCT `redcap_genvasc`.`redcap_data`.`project_id` AS `project_id`,
                            `redcap_genvasc`.`redcap_data`.`record` AS `record`,
                            `redcap_genvasc`.`redcap_data`.`field_name` AS `field_name`,
                            `redcap_genvasc`.`redcap_data`.`value` AS `value`,
                            COALESCE(`redcap_genvasc`.`redcap_data`.`instance`, 1) AS `instance`
                        FROM
                            `redcap_genvasc`.`redcap_data`
                        WHERE
                            (
                                (
                                    `redcap_genvasc`.`redcap_data`.`project_id` IN (
                                        16, 15
                                    )
                                )
                                AND (
                                    `redcap_genvasc`.`redcap_data`.`field_name` IN (
                                        'gv_contact', 'gv_role', 'gv_role_other', 'gcp_trained', 'gv_trained', 'on_delegation_log_yn', 'gv_start_del_log', 'gv_end_del_log', 'rsn_not_on_del_log', 'gv_phone_a', 'gv_phone_b', 'contact_email_add', 'primary_contact_yn'
                                    )
                                )
                            )
                    ) `x`
                GROUP BY
                    `x`.`record`,
                    `x`.`instance`
            )
        ) `contacts`
    LEFT JOIN (
            SELECT
                `x`.`project_id` AS `project_id`,
                trim(substring_index(`x`.`option_pair`, ',', 1)) AS `role_value`,
                trim(substring_index(`x`.`option_pair`, ',',-(1))) AS `role_name`
            FROM
                (
                    SELECT
                        DISTINCT `redcap_genvasc`.`redcap_metadata`.`project_id` AS `project_id`,
                        `redcap_genvasc`.`redcap_metadata`.`field_name` AS `field_name`,
                        trim(substring_index(substring_index(`redcap_genvasc`.`redcap_metadata`.`element_enum`, '\\n', `numbers`.`n`), '\\n',-(1))) AS `option_pair`
                    FROM
                        (
                            (
                                (
                                    SELECT
                                        (
                                            (
                                                (
                                                    (
                                                        (
                                                            `TWO_1`.`SeqValue` + `TWO_2`.`SeqValue`
                                                        ) + `TWO_4`.`SeqValue`
                                                    ) + `TWO_8`.`SeqValue`
                                                ) + `TWO_16`.`SeqValue`
                                            ) + `TWO_32`.`SeqValue`
                                        ) AS `n`
                                    FROM
                                        (
                                            (
                                                (
                                                    (
                                                        (
                                                            (
                                                                (
                                                                    SELECT
                                                                        0 AS `SeqValue`
                                                                )
                                                        UNION ALL
                                                            SELECT
                                                                1 AS `SeqValue`
                                                            ) `TWO_1`
                                                        JOIN (
                                                                SELECT
                                                                    0 AS `SeqValue`
                                                            UNION ALL
                                                                SELECT
                                                                    2 AS `SeqValue`
                                                            ) `TWO_2`
                                                        )
                                                    JOIN (
                                                            SELECT
                                                                0 AS `SeqValue`
                                                        UNION ALL
                                                            SELECT
                                                                4 AS `SeqValue`
                                                        ) `TWO_4`
                                                    )
                                                JOIN (
                                                        SELECT
                                                            0 AS `SeqValue`
                                                    UNION ALL
                                                        SELECT
                                                            8 AS `SeqValue`
                                                    ) `TWO_8`
                                                )
                                            JOIN (
                                                    SELECT
                                                        0 AS `SeqValue`
                                                UNION ALL
                                                    SELECT
                                                        16 AS `SeqValue`
                                                ) `TWO_16`
                                            )
                                        JOIN (
                                                SELECT
                                                    0 AS `SeqValue`
                                            UNION ALL
                                                SELECT
                                                    32 AS `SeqValue`
                                            ) `TWO_32`
                                        )
                                )
                            ) `numbers`
                        JOIN `redcap_genvasc`.`redcap_metadata` ON
                            (
                                (
                                    (
                                        char_length(`redcap_genvasc`.`redcap_metadata`.`element_enum`) - char_length(REPLACE(`redcap_genvasc`.`redcap_metadata`.`element_enum`, '\\n', ''))
                                    ) >= (
                                        `numbers`.`n` - 1
                                    )
                                )
                            )
                        )
                    WHERE
                        (
                            (
                                `redcap_genvasc`.`redcap_metadata`.`project_id` IN (
                                    16, 15
                                )
                            )
                            AND (
                                `redcap_genvasc`.`redcap_metadata`.`field_name` = 'gv_role'
                            )
                        )
                    ORDER BY
                        `redcap_genvasc`.`redcap_metadata`.`field_name`,
                        `numbers`.`n`
                ) `x`
        ) `roles` ON
        (
            (
                (
                    `roles`.`role_value` = `contacts`.`role`
                )
                AND (
                    `roles`.`project_id` = `contacts`.`project_id`
                )
            )
        )
    )