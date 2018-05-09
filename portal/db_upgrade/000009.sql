CREATE TABLE recruit (
        id VARCHAR(50) PRIMARY KEY NOT NULL
    ,   practice_registration_id INTEGER NOT NULL
    ,   user_id INTEGER NOT NULL
    ,	nhs_number VARCHAR(20) NOT NULL
    ,	date_of_birth DATE NOT NULL
    ,	date_recruited DATE NOT NULL
    ,	date_created DATETIME NOT NULL
    ,   civicrm_contact_id INTEGER NULL
    ,   civicrm_case_id INTEGER NULL
	,	CONSTRAINT fk_recruit_user FOREIGN KEY (user_id) REFERENCES user(id)
	,	CONSTRAINT fk_recruit_practice_registration FOREIGN KEY (practice_registration_id) REFERENCES practice_registration(id)
    )
;

CREATE INDEX idx_recruit_user_id
ON recruit (user_id)
;

CREATE INDEX idx_recruit_practice_registration_id
ON recruit (practice_registration_id)
;

CREATE UNIQUE INDEX idx_recruit_civicrm_case_id
ON recruit (civicrm_case_id)
;

CREATE INDEX idx_recruit_civicrm_contact_id
ON recruit (civicrm_contact_id)
;