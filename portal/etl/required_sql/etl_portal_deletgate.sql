CREATE VIEW etl_portal_delegate AS
SELECT
    contacts.record AS practice_code,
    contacts.instance,
    COALESCE(contacts.name, '') name,
    COALESCE(roles.role_name, gv_role_other) AS role,
    contacts.gcp_trained,
    contacts.gv_trained,
    contacts.on_delegation_log_yn,
    contacts.gv_start_del_log,
    contacts.gv_end_del_log,
    contacts.rsn_not_on_del_log,
    contacts.gv_phone_a,
    contacts.gv_phone_b,
    contacts.contact_email_add,
    contacts.primary_contact_yn,
    ts.last_update_timestamp
FROM (
    SELECT
        record,
        project_id,
        instance,
        GROUP_CONCAT(CASE WHEN field_name = 'gv_contact' THEN VALUE ELSE NULL END) AS name,
        GROUP_CONCAT(CASE WHEN field_name = 'gv_role' THEN VALUE ELSE NULL END) AS role,
        GROUP_CONCAT(CASE WHEN field_name = 'gv_role_other' THEN VALUE ELSE NULL END) AS gv_role_other,
        GROUP_CONCAT(CASE WHEN field_name = 'gcp_trained' THEN VALUE ELSE NULL END) AS gcp_trained,
        GROUP_CONCAT(CASE WHEN field_name = 'gv_trained' THEN VALUE ELSE NULL END) AS gv_trained,
        GROUP_CONCAT(CASE WHEN field_name = 'on_delegation_log_yn' THEN VALUE ELSE NULL END) AS on_delegation_log_yn,
        GROUP_CONCAT(CASE WHEN field_name = 'gv_start_del_log' THEN VALUE ELSE NULL END) AS gv_start_del_log,
        GROUP_CONCAT(CASE WHEN field_name = 'gv_end_del_log' THEN VALUE ELSE NULL END) AS gv_end_del_log,
        GROUP_CONCAT(CASE WHEN field_name = 'rsn_not_on_del_log' THEN VALUE ELSE NULL END) AS rsn_not_on_del_log,
        GROUP_CONCAT(CASE WHEN field_name = 'gv_phone_a' THEN VALUE ELSE NULL END) AS gv_phone_a,
        GROUP_CONCAT(CASE WHEN field_name = 'gv_phone_b' THEN VALUE ELSE NULL END) AS gv_phone_b,
        GROUP_CONCAT(CASE WHEN field_name = 'contact_email_add' THEN VALUE ELSE NULL END) AS contact_email_add,
        GROUP_CONCAT(CASE WHEN field_name = 'primary_contact_yn' THEN VALUE ELSE NULL END) AS primary_contact_yn
    FROM    (
        SELECT DISTINCT
        	project_id,
            record,
            field_name,
            value,
            COALESCE(instance, 1) AS instance
        FROM redcap_data
        WHERE project_id IN (29, 53)
            AND field_name IN (
                'gv_contact',
                'gv_role',
                'gv_role_other',
                'gcp_trained',
                'gv_trained',
                'on_delegation_log_yn',
                'gv_start_del_log',
                'gv_end_del_log',
                'rsn_not_on_del_log',
                'gv_phone_a',
                'gv_phone_b',
                'contact_email_add',
                'primary_contact_yn'
            )
    ) x
    GROUP BY
        record,
        instance
) contacts
LEFT JOIN (
    SELECT
    	project_id,
        TRIM(SUBSTRING_INDEX(option_pair, ',', 1)) role_value,
        TRIM(SUBSTRING_INDEX(option_pair, ',', -1)) role_name
    FROM (
        SELECT DISTINCT
          project_id,
          redcap_metadata.field_name,
          TRIM(SUBSTRING_INDEX(SUBSTRING_INDEX(redcap_metadata.element_enum, '\\n', numbers.n), '\\n', -1)) option_pair
        FROM (
            SELECT
             (TWO_1.SeqValue + TWO_2.SeqValue + TWO_4.SeqValue + TWO_8.SeqValue + TWO_16.SeqValue + TWO_32.SeqValue) n
            FROM
             (SELECT 0 SeqValue UNION ALL SELECT 1 SeqValue) TWO_1
             CROSS JOIN (SELECT 0 SeqValue UNION ALL SELECT 2 SeqValue) TWO_2
             CROSS JOIN (SELECT 0 SeqValue UNION ALL SELECT 4 SeqValue) TWO_4
             CROSS JOIN (SELECT 0 SeqValue UNION ALL SELECT 8 SeqValue) TWO_8
             CROSS JOIN (SELECT 0 SeqValue UNION ALL SELECT 16 SeqValue) TWO_16
             CROSS JOIN (SELECT 0 SeqValue UNION ALL SELECT 32 SeqValue) TWO_32      
            ) numbers
            INNER JOIN redcap_metadata
                ON CHAR_LENGTH(redcap_metadata.element_enum)
                    -CHAR_LENGTH(REPLACE(redcap_metadata.element_enum, '\\n', ''))
                     >= numbers.n - 1
        WHERE project_id IN (29, 53)
            AND field_name = 'gv_role'
        ORDER BY
          field_name, n
    ) x
) roles ON roles.role_value = contacts.role AND roles.project_id = contacts.project_id
LEFT JOIN (
	SELECT
		pk as record,
		project_id,
		MAX(COALESCE(ts, 0)) AS last_update_timestamp
	FROM redcap_log_event
	WHERE event NOT IN ('DATA_EXPORT', 'DELETE')
	    # Ignore events caused by the data import from
	    # the mobile app
	    AND page NOT IN ('DataImportController:index')
	    AND project_id IN (29, 53)
	  	AND object_type = 'redcap_data'
	GROUP BY pk, project_id
 ) ts ON ts.record = contacts.record
 	AND ts.project_id = contacts.project_id
;