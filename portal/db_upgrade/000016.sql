CREATE TABLE etl_delegationLog (
    practice_code VARCHAR(50) NOT NULL,
    instance INTEGER NOT NULL,
    name VARCHAR(500) NOT NULL,
    role VARCHAR(500),
    gcp_training BOOLEAN,
    gv_trained BOOLEAN,
    on_delegation_log_yn BOOLEAN,
    gv_start_del_log DATETIME,
    gv_end_del_log DATETIME,
    rsn_not_on_del_log VARCHAR(500),
    gv_phone_a VARCHAR(100),
    gv_phone_b VARCHAR(100),
    contact_email_add VARCHAR(500),
    primary_contact_yn BOOLEAN,
    PRIMARY KEY (practice_code, instance)
)
;
