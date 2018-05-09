CREATE UNIQUE INDEX idx_practice_registrations_users_uq1
ON practice_registrations_users (user_id, practice_registration_id)
;
