CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW etl_delegate AS
select
    contacts.record AS practice_code,
    contacts.instance AS instance,
    coalesce(contacts.name,
    '') AS name,
    coalesce(roles.role_name,
    contacts.gv_role_other) AS role,
    contacts.gcp_trained AS gcp_trained,
    contacts.gv_trained AS gv_trained,
    contacts.on_delegation_log_yn AS on_delegation_log_yn,
    contacts.gv_start_del_log AS gv_start_del_log,
    contacts.gv_end_del_log AS gv_end_del_log,
    contacts.rsn_not_on_del_log AS rsn_not_on_del_log,
    contacts.gv_phone_a AS gv_phone_a,
    contacts.gv_phone_b AS gv_phone_b,
    LOWER(contacts.contact_email_add) AS contact_email_add,
    contacts.primary_contact_yn AS primary_contact_yn
from
    (((
    select
        x.record AS record,
        x.project_id AS project_id,
        x.instance AS instance,
        group_concat(
        (
            case
            when (x.field_name = 'gv_contact') then x.value
            else NULL end) separator ',') AS name,
        group_concat(
        (
            case
            when (x.field_name = 'gv_role') then x.value
            else NULL end) separator ',') AS role,
        group_concat(
        (
            case
            when (x.field_name = 'gv_role_other') then x.value
            else NULL end) separator ',') AS gv_role_other,
        group_concat(
        (
            case
            when (x.field_name = 'gcp_trained') then x.value
            else NULL end) separator ',') AS gcp_trained,
        group_concat(
        (
            case
            when (x.field_name = 'gv_trained') then x.value
            else NULL end) separator ',') AS gv_trained,
        group_concat(
        (
            case
            when (x.field_name = 'on_delegation_log_yn') then x.value
            else NULL end) separator ',') AS on_delegation_log_yn,
        group_concat(
        (
            case
            when (x.field_name = 'gv_start_del_log') then x.value
            else NULL end) separator ',') AS gv_start_del_log,
        group_concat(
        (
            case
            when (x.field_name = 'gv_end_del_log') then x.value
            else NULL end) separator ',') AS gv_end_del_log,
        group_concat(
        (
            case
            when (x.field_name = 'rsn_not_on_del_log') then x.value
            else NULL end) separator ',') AS rsn_not_on_del_log,
        group_concat(
        (
            case
            when (x.field_name = 'gv_phone_a') then x.value
            else NULL end) separator ',') AS gv_phone_a,
        group_concat(
        (
            case
            when (x.field_name = 'gv_phone_b') then x.value
            else NULL end) separator ',') AS gv_phone_b,
        group_concat(
        (
            case
            when (x.field_name = 'contact_email_add') then x.value
            else NULL end) separator ',') AS contact_email_add,
        group_concat(
        (
            case
            when (x.field_name = 'primary_contact_yn') then x.value
            else NULL end) separator ',') AS primary_contact_yn
    from
        (
        select
            distinct redcap6170_briccsext.redcap_data.project_id AS project_id,
            redcap6170_briccsext.redcap_data.record AS record,
            redcap6170_briccsext.redcap_data.field_name AS field_name,
            redcap6170_briccsext.redcap_data.value AS value,
            coalesce(redcap6170_briccsext.redcap_data.instance,
            1) AS instance
        from
            redcap6170_briccsext.redcap_data
        where
            ((redcap6170_briccsext.redcap_data.project_id in (29,
            53))
            and (redcap6170_briccsext.redcap_data.field_name in ('gv_contact',
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
            'primary_contact_yn')))) x
    group by
        x.record,
        x.instance)) contacts
left join (
    select
        x.project_id AS project_id,
        trim(substring_index(x.option_pair, ',', 1)) AS role_value,
        trim(substring_index(x.option_pair, ',',-(1))) AS role_name
    from
        (
        select
            distinct redcap6170_briccsext.redcap_metadata.project_id AS project_id,
            redcap6170_briccsext.redcap_metadata.field_name AS field_name,
            trim(substring_index(substring_index(redcap6170_briccsext.redcap_metadata.element_enum, '\\n', numbers.n), '\\n',-(1))) AS option_pair
        from
            (((
            select
                (((((TWO_1.SeqValue + TWO_2.SeqValue) + TWO_4.SeqValue) + TWO_8.SeqValue) + TWO_16.SeqValue) + TWO_32.SeqValue) AS n
            from
                (((((((
                select
                    0 AS SeqValue)
        union all
            select
                1 AS SeqValue) TWO_1
            join (
                select
                    0 AS SeqValue
            union all
                select
                    2 AS SeqValue) TWO_2)
            join (
                select
                    0 AS SeqValue
            union all
                select
                    4 AS SeqValue) TWO_4)
            join (
                select
                    0 AS SeqValue
            union all
                select
                    8 AS SeqValue) TWO_8)
            join (
                select
                    0 AS SeqValue
            union all
                select
                    16 AS SeqValue) TWO_16)
            join (
                select
                    0 AS SeqValue
            union all
                select
                    32 AS SeqValue) TWO_32))) numbers
        join redcap6170_briccsext.redcap_metadata on
            (((char_length(redcap6170_briccsext.redcap_metadata.element_enum) - char_length(replace(redcap6170_briccsext.redcap_metadata.element_enum, '\\n', ''))) >= (numbers.n - 1))))
        where
            ((redcap6170_briccsext.redcap_metadata.project_id in (29,
            53))
            and (redcap6170_briccsext.redcap_metadata.field_name = 'gv_role'))
        order by
            redcap6170_briccsext.redcap_metadata.field_name,
            numbers.n) x) roles on
    (((roles.role_value = contacts.role)
    and (roles.project_id = contacts.project_id))));