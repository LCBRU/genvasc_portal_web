CREATE TABLE practice_registration (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   code VARCHAR(50) NOT NULL
    ,   date_created DATETIME NOT NULL
    )
;

CREATE UNIQUE INDEX idx_practice_registration_code
ON practice_registration (code)
;
