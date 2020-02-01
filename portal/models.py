from datetime import datetime
from portal import db
from flask_security import UserMixin, RoleMixin


class PracticeGroup(db.Model):

    __tablename__ = 'practice_group'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "PracticeGroup",
        "polymorphic_on": type,
    }


class Federation(PracticeGroup):

    __mapper_args__ = {
        "polymorphic_identity": 'Federation',
    }


class Ccg(PracticeGroup):

    __mapper_args__ = {
        "polymorphic_identity": 'CCG',
    }


class ManagementArea(PracticeGroup):

    __mapper_args__ = {
        "polymorphic_identity": 'Management Area',
    }


class Practice(db.Model):

    __tablename__ = 'etl_practice_detail'

    project_id = db.Column(db.Integer, nullable=False)
    ccg = db.Column(db.Integer, nullable=True)
    federation = db.Column(db.Integer, nullable=True)
    code = db.Column(db.String, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    street_address = db.Column(db.String, nullable=True)
    town = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    county = db.Column(db.String, nullable=True)
    postcode = db.Column(db.String, nullable=True)
    partners = db.Column(db.String, nullable=True)
    genvasc_initiated = db.Column(db.Boolean, nullable=True)
    status = db.Column(db.Integer, nullable=True)


class PracticeGroupPractice(db.Model):

    __tablename__ = 'etl_practice_groups_practices'

    practice_group_id = db.Column(db.Integer, primary_key=True)
    practice_code = db.Column(db.String, nullable=False, primary_key=True)


class Role(db.Model, RoleMixin):
    ADMIN_ROLENAME = 'admin'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


roles_users = db.Table(
    'roles_users',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id')),
    db.Column(
        'role_id',
        db.Integer(),
        db.ForeignKey('role.id')))


practices_users = db.Table(
    'practices_users',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id'),
    ),
    db.Column(
        'practice_code',
        db.Integer(),
        db.ForeignKey('etl_practice_detail.code'),
    )
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, index=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    current_portal_user_yn = db.Column(db.Boolean)
    gv_end_del_log = db.Column(db.Date)
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(50))
    current_login_ip = db.Column(db.String(50))
    login_count = db.Column(db.Integer())
    is_imported = db.Column(db.Boolean(), default=False)
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'),
    )
    practices = db.relationship(
        'Practice',
        secondary=practices_users,
        backref=db.backref('users', lazy='dynamic'),
    )
    last_update_timestamp = db.Column(db.Integer, nullable=True)

    def is_admin(self):
        return self.has_role(Role.ADMIN_ROLENAME)

    def is_system(self):
        return self.email == 'lcbruit@uhl-tr.nhs.uk'

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name or '', self.last_name or '').strip() or self.email


class PracticeRegistration(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, db.ForeignKey(Practice.code))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    practice = db.relationship(Practice)


class Recruit(db.Model):
    __tablename__ = 'etl_recruit'

    status = db.Column(db.String(100))
    nhs_number = db.Column(db.String(20), nullable=False)
    study_id = db.Column(db.String(100))
    practice_code = db.Column(db.String(100), db.ForeignKey(Practice.code), nullable=True)
    practice = db.relationship(Practice)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date, nullable=False)
    civicrm_contact_id = db.Column(db.Integer)
    civicrm_case_id = db.Column(db.Integer, primary_key=True)
    processed_date = db.Column(db.Date)
    date_recruited = db.Column(db.Date, nullable=False)
    invoice_year = db.Column(db.Integer)
    invoice_quarter = db.Column(db.String(50))
    reimbursed_status = db.Column(db.String(50))

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name or '', self.last_name or '')

    @property
    def invoice_period(self):
        return '{} {}'.format(
            self.invoice_year or '',
            self.invoice_quarter or '',
        ).strip()


class Delegate(db.Model):

    __tablename__ = 'etl_delegate'

    practice_code = db.Column(db.String, primary_key=True)
    instance = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    role = db.Column(db.String(500))
    gcp_trained = db.Column(db.Boolean)
    gv_trained = db.Column(db.Boolean)
    on_delegation_log_yn = db.Column(db.Boolean)
    gv_start_del_log = db.Column(db.Date)
    gv_end_del_log = db.Column(db.Date)
    gv_phone_a = db.Column(db.String(100))
    gv_phone_b = db.Column(db.String(100))
    contact_email_add = db.Column(db.String(500))
    primary_contact_yn = db.Column(db.Boolean)
