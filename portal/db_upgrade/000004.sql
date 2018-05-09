CREATE TABLE staff_member (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,	practice_registration_id INTEGER NOT NULL
    ,   first_name VARCHAR(100) NOT NULL
    ,   last_name VARCHAR(100) NOT NULL
    ,   date_created DATETIME NOT NULL
	,	CONSTRAINT fk_staff_member_practice_registration FOREIGN KEY (practice_registration_id) REFERENCES practice_registration(id)
    )
;

CREATE INDEX idx_staff_member_practice_registration_id
ON staff_member (practice_registration_id)
;
