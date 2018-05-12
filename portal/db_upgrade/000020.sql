ALTER TABLE etl_practice
ADD federation VARCHAR(500)
;

CREATE INDEX idx_etl_practice_federation
ON etl_practice (federation)
;

