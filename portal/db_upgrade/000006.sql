CREATE TABLE role (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   name VARCHAR(80) NOT NULL
    ,   description VARCHAR(255) NOT NULL
)
;

CREATE UNIQUE INDEX idx_role_name
ON role (name)
;

CREATE TABLE user (
        id INTEGER PRIMARY KEY AUTO_INCREMENT
    ,   email VARCHAR(255) NOT NULL
    ,   password VARCHAR(255) NOT NULL
    ,   first_name VARCHAR(255) NOT NULL
    ,   last_name VARCHAR(255) NOT NULL
    ,   active BOOLEAN NOT NULL
    ,   confirmed_at DATETIME NULL
    ,   last_login_at DATETIME NULL
    ,   current_login_at DATETIME NULL
    ,   last_login_ip VARCHAR(50) NULL
    ,   current_login_ip VARCHAR(50) NULL
    ,   login_count INTEGER NULL
    )
;

CREATE UNIQUE INDEX idx_user_email
ON user (email)
;

CREATE TABLE roles_users (
        user_id INTEGER NOT NULL
    ,   role_id INTEGER NOT NULL
    , 	FOREIGN KEY (user_id) REFERENCES user(id)
    , 	FOREIGN KEY (role_id) REFERENCES role(id)
)
;

CREATE INDEX idx_roles_users_role_id
ON roles_users (user_id)
;

CREATE INDEX idx_roles_users_user_id
ON roles_users (role_id)
;

