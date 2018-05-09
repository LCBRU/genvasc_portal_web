CREATE TABLE practice_registrations_users (
        user_id INTEGER NOT NULL
    ,   practice_registration_id INTEGER NOT NULL
    , 	FOREIGN KEY (user_id) REFERENCES user(id)
    , 	FOREIGN KEY (practice_registration_id) REFERENCES practice_registration(id)
)
;

CREATE INDEX idx_practice_registrations_users_user_id
ON practice_registrations_users (user_id)
;

CREATE INDEX idx_practice_registrations_users_practice_registration_id
ON practice_registrations_users (practice_registration_id)
;

