import random
import string
import re
import datetime
from itertools import chain
from portal import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import ForeignKeyConstraint, select, func
from sqlalchemy.orm import column_property
from portal.utils import parse_date


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


practice_groups_users = db.Table(
    'practice_groups_users',
    db.Column(
        'user_id',
        db.Integer(),
        db.ForeignKey('user.id'),
    ),
    db.Column(
        'practice_group_type',
        db.String(),
    ),
    db.Column(
        'practice_group_project_id',
        db.Integer(),
    ),
    db.Column(
        'practice_group_identifier',
        db.Integer(),
    ),
    ForeignKeyConstraint(
        ['practice_group_type', 'practice_group_project_id', 'practice_group_identifier'],
        ['etl_practice_group.type', 'etl_practice_group.project_id', 'etl_practice_group.identifier'],
    ),
)


practice_groups_practices = db.Table(
    'etl_practice_groups_practices',
    db.Column(
        'practice_code',
        db.String(),
        db.ForeignKey('etl_practice_detail.code'),
    ),
    db.Column(
        'practice_group_type',
        db.String(),
    ),
    db.Column(
        'practice_group_project_id',
        db.Integer(),
    ),
    db.Column(
        'practice_group_identifier',
        db.String(),
    ),
    ForeignKeyConstraint(
        ['practice_group_type', 'practice_group_project_id', 'practice_group_identifier'],
        ['etl_practice_group.type', 'etl_practice_group.project_id', 'etl_practice_group.identifier'],
    ),
)


class PracticeGroup(db.Model):

    __tablename__ = 'etl_practice_group'
    project_id = db.Column(db.Integer, primary_key=True, nullable=False)
    identifier = db.Column(db.String, primary_key=True, nullable=False)
    type = db.Column(db.String, primary_key=True, nullable=False)
    name = db.Column(db.String, nullable=False)

    practices = db.relationship(
        'Practice',
        secondary=practice_groups_practices,
        backref=db.backref('groups', lazy='dynamic'),
        collection_class=set,
    )

    def __str__(self):
        return f"{self.type}: {self.name}"

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


class PracticeStatus(db.Model):

    __tablename__ = 'practice_status'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String, nullable=False)


class Recruit(db.Model):
    __tablename__ = 'etl_recruit'

    status = db.Column(db.String(100))
    nhs_number = db.Column(db.String(20), nullable=False)
    study_id = db.Column(db.String(100))
    practice_code = db.Column(db.String(100), db.ForeignKey("etl_practice_detail.code"), nullable=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date, nullable=False)
    civicrm_contact_id = db.Column(db.Integer)
    civicrm_case_id = db.Column(db.Integer, primary_key=True)
    recruited_date = db.Column(db.Date, nullable=False)
    invoice_year = db.Column(db.Integer)
    invoice_quarter = db.Column(db.String(50))
    reimbursed_status = db.Column(db.String(50))
    exclusion_reason = db.Column(db.String(500))

    @property
    def exclusion_reason_stripped(self):
        re_tag = re.compile(r'(<!--.*?-->|<[^>]*>)')
        re_nbsp = re.compile(r'(&nbsp;)')
        re_amp = re.compile(r'(&amp;)')
        return re_amp.sub('&', re_nbsp.sub('', re_tag.sub('', self.exclusion_reason or ''))).strip()

    @property
    def exclusion_text(self):
        if len(self.exclusion_reason_stripped) > 0:
            return f"Excluded: {self.exclusion_reason_stripped}"
        else:
            return 'Excluded'

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name or '', self.last_name or '')

    @property
    def invoice_period(self):
        return '{} {}'.format(
            self.invoice_year or '',
            self.invoice_quarter or '',
        ).strip()


class Practice(db.Model):

    __tablename__ = 'etl_practice_detail'

    project_id = db.Column(db.Integer, nullable=False)
    ccg = db.Column(db.Integer, nullable=False)
    federation = db.Column(db.Integer, nullable=True)
    code = db.Column(db.String, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    street_address = db.Column(db.String, nullable=True)
    town = db.Column(db.String, nullable=True)
    city = db.Column(db.String, nullable=True)
    county = db.Column(db.String, nullable=True)
    postcode = db.Column(db.String, nullable=True)
    partners = db.Column(db.String, nullable=True)
    collab_ag_comp_yn = db.Column(db.Boolean, nullable=True)
    collab_ag_signed_date_str = db.Column(db.String, nullable=True)
    isa_comp_yn = db.Column(db.Boolean, nullable=True)
    isa_1_signed_date_str = db.Column(db.String, nullable=True)
    isa_1_caldicott_guard_end_str = db.Column(db.String, nullable=True)
    agree_66_comp_yn = db.Column(db.Boolean, nullable=True)
    agree_66_signed_date_1_str = db.Column(db.String, nullable=True)
    agree_66_end_date_2_str = db.Column(db.String, nullable=True)
    genvasc_initiated = db.Column(db.Boolean, nullable=True)
    status_id = db.Column(db.Integer, db.ForeignKey(PracticeStatus.value), nullable=True)
    status = db.relationship(PracticeStatus)
    recruits = db.relationship(Recruit, backref='practice', lazy=True)
    recruit_summary = db.relationship("RecruitSummary", uselist=False, back_populates="practice", lazy='joined')

    @property
    def collab_ag_signed_date(self):
        if self.collab_ag_signed_date_str:
            return parse_date(self.collab_ag_signed_date_str).date()

    @property
    def isa_1_signed_date(self):
        if self.isa_1_signed_date_str:
            return parse_date(self.isa_1_signed_date_str).date()

    @property
    def isa_1_caldicott_guard_end(self):
        if self.isa_1_caldicott_guard_end_str:
            return parse_date(self.isa_1_caldicott_guard_end_str).date()

    @property
    def agree_66_signed_date_1(self):
        if self.agree_66_signed_date_1_str:
            return parse_date(self.agree_66_signed_date_1_str).date()

    @property
    def agree_66_end_date_2(self):
        if self.agree_66_end_date_2_str:
            return parse_date(self.agree_66_end_date_2_str).date()

    @property
    def ccg_name(self):
        return {
            0 : 'NHS Leicester City CCG',
            1 : 'NHS East Leicestershire and Rutland CCG',
            2 : 'NHS West Leicestershire CCG',
            3 : 'Corby',
            4 : 'Nene',
        }[self.ccg]

    @property
    def full_address(self):
        return ', '.join([a for a in [self.street_address, self.town, self.city, self.county, self.postcode] if a])

    @property
    def has_current_isa(self):
        if (
            (self.isa_comp_yn and self.isa_1_caldicott_guard_end is None) or
            (self.isa_comp_yn and self.isa_1_caldicott_guard_end > datetime.date.today()) or
            (self.agree_66_comp_yn and self.agree_66_end_date_2 is None) or
            (self.agree_66_comp_yn and self.agree_66_end_date_2 > datetime.date.today())
        ):
            return True

        return False


class RecruitSummary(db.Model):

    __tablename__ = 'etl_recruit_summary'

    practice_code = db.Column(db.String(500), db.ForeignKey(Practice.code), primary_key=True, nullable=True)
    practice = db.relationship("Practice", back_populates="recruit_summary")
    recruited = db.Column(db.Integer)
    excluded = db.Column(db.Integer)
    excluded_percentage = db.Column(db.Float)
    withdrawn = db.Column(db.Integer)
    withdrawn_percentage = db.Column(db.Float)
    last_recruited_date = db.Column(db.Date)


class Role(db.Model, RoleMixin):
    ADMIN_ROLENAME = 'admin'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, index=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255), default=lambda: ''.join(random.choice(string.ascii_lowercase) for _ in range(20)))
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
        collection_class=set,
    )
    practices = db.relationship(
        'Practice',
        secondary=practices_users,
        backref=db.backref('users', lazy='dynamic'),
        collection_class=set,
    )
    practice_groups = db.relationship(
        'PracticeGroup',
        secondary=practice_groups_users,
        backref=db.backref('users', lazy='dynamic'),
        collection_class=set,
    )
    last_update_timestamp = db.Column(db.Integer, nullable=True)

    def get_id(self):
        return self.email
        
    @property
    def is_super(self):
        return self.is_admin or len(self.practice_groups) > 0

    @property
    def is_admin(self):
        return self.has_role(Role.ADMIN_ROLENAME)

    @property
    def is_system(self):
        return self.email == 'lcbruit@uhl-tr.nhs.uk'

    @property
    def all_practices(self):
        return set(self.practices) | set(chain.from_iterable(pg.practices for pg in self.practice_groups))

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name or '', self.last_name or '').strip() or self.email


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
    contact_email_add = db.Column(db.String(500), db.ForeignKey(User.email), nullable=True)
    user = db.relationship(User)
    primary_contact_yn = db.Column(db.Boolean)


class Message(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
