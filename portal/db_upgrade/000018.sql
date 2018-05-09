CREATE TABLE administrator (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   email VARCHAR(255) NOT NULL
    )
;

CREATE UNIQUE INDEX idx_administrator_email
ON administrator (email)
;

INSERT INTO administrator
    (email)
VALUES
    ('lcbruit@uhl-tr.nhs.uk'),
    ('rab63@le.ac.uk'),
    ('christopher.greengrass@uhl-tr.nhs.uk'),
    ('Emma.Beeston@uhl-tr.nhs.uk'),
    ('Dawn.Woods@uhl-tr.nhs.uk'),
    ('fenglin.guo@nihr.ac.uk'),
    ('michelle.chalke@nihr.ac.uk'),
    ('daniel.brewer@uhl-tr.nhs.uk')
;
