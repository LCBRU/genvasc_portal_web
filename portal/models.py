import datetime
import uuid
from portal import db
from flask_security import UserMixin, RoleMixin


class Practice(db.Model):

    __tablename__ = 'etl_practice'

    code = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ccg_name = db.Column(db.String, nullable=True)
    address = db.Column(db.String, nullable=True)
    delegates = db.relationship(
        "Delegate",
        back_populates="practice")


class Role(db.Model, RoleMixin):
    ADMIN_ROLENAME = 'admin'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, *args, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description')


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


practice_registrations_users = db.Table(
    'practice_registrations_users',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id')),
    db.Column(
        'practice_registration_id',
        db.Integer(),
        db.ForeignKey('practice_registration.id')))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    last_login_at = db.Column(db.DateTime())
    current_login_at = db.Column(db.DateTime())
    last_login_ip = db.Column(db.String(50))
    current_login_ip = db.Column(db.String(50))
    login_count = db.Column(db.Integer())
    roles = db.relationship(
        'Role',
        secondary=roles_users,
        backref=db.backref('users', lazy='dynamic'))
    practices = db.relationship(
        'PracticeRegistration',
        secondary=practice_registrations_users,
        backref=db.backref('users', lazy='dynamic'))

    def __init__(self, *args, **kwargs):
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.active = 0

    def is_admin(self):
        return self.has_role(Role.ADMIN_ROLENAME)

    def is_system(self):
        return self.email == 'lcbruit@uhl-tr.nhs.uk'

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name or '', self.last_name or '')


class PracticeRegistration(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String, db.ForeignKey(Practice.code))
    date_created = db.Column(db.DateTime, nullable=False)
    practice = db.relationship(Practice)

    def __init__(self, *args, **kwargs):
        self.code = kwargs.get('code')
        self.date_created = datetime.datetime.now()


class StaffMember(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    practice_registration_id = db.Column(
        db.Integer,
        db.ForeignKey(PracticeRegistration.id))
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    practice_registration = db.relationship(
        PracticeRegistration,
        backref=db.backref('staff', cascade="all, delete-orphan"))

    def __init__(self, *args, **kwargs):
        self.practice_registration_id = kwargs.get('practice_registration').id
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.date_created = datetime.datetime.now()

    def full_name(self):
        return '{} {}'.format(self.first_name or '', self.last_name or '')


class Recruit(db.Model):

    id = db.Column(db.String(50), primary_key=True)
    practice_registration_id = db.Column(
        db.Integer,
        db.ForeignKey(PracticeRegistration.id))
    practice_registration = db.relationship(
        PracticeRegistration,
        backref=db.backref('recruits', cascade="all, delete-orphan"))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(
        User,
        backref=db.backref('recruits', cascade="all, delete-orphan"))
    nhs_number = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    date_recruited = db.Column(db.Date, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False)
    status = db.relationship(
        "RecruitStatus",
        uselist=False,
        back_populates="recruit")

    def __init__(self, *args, **kwargs):
        self.practice_registration_id = kwargs.get('practice_registration').id
        self.user_id = kwargs.get('user').id
        self.nhs_number = kwargs.get('nhs_number')
        self.date_of_birth = kwargs.get('date_of_birth')
        self.date_recruited = kwargs.get('date_recruited')
        self.date_created = datetime.datetime.now()
        self.id = uuid.uuid1()

    @property
    def date_of_birth_day(self):
        return self.date_of_birth.day

    @property
    def date_of_birth_month(self):
        return self.date_of_birth.month

    @property
    def date_of_birth_year(self):
        return self.date_of_birth.year


class RecruitStatus(db.Model):

    __tablename__ = 'etl_recruit_status'

    id = db.Column(db.String(50), db.ForeignKey(Recruit.id), primary_key=True)
    recruit = db.relationship(Recruit, uselist=False, back_populates="status")
    status = db.Column(db.String(100))
    study_id = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    processed_by = db.Column(db.String(500))
    processed_date = db.Column(db.Date)
    invoice_year = db.Column(db.String(50))
    invoice_quarter = db.Column(db.String(50))
    reimbursed_status = db.Column(db.String(50))

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name or '', self.last_name or '')

    @property
    def invoice_period(self):
        return '{} {}'.format(
            self.invoice_year or '',
            self.invoice_quarter or '')


class Delegate(db.Model):

    __tablename__ = 'etl_delegationLog'

    practice_code = db.Column(
        db.String,
        db.ForeignKey(Practice.code),
        primary_key=True)
    practice = db.relationship(Practice, back_populates="delegates")
    instance = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500))
    role = db.Column(db.String(500))
    gcp_training = db.Column(db.Boolean)
    gv_trained = db.Column(db.Boolean)
    on_delegation_log_yn = db.Column(db.Boolean)
    gv_start_del_log = db.Column(db.Date)
    gv_end_del_log = db.Column(db.Date)
    gv_phone_a = db.Column(db.String(100))
    gv_phone_b = db.Column(db.String(100))
    contact_email_add = db.Column(db.String(500))
    primary_contact_yn = db.Column(db.Boolean)
