#!/usr/bin/env python
import os
from contextlib import contextmanager
from portal.utils import parse_date
from dotenv import load_dotenv
from portal.database import db
from portal.etl.database import (
    etl_import_database,
    recruit_table,
    recruit_summary_table,
    delegate_table,
    practice_table,
    practice_group_table,
    practice_groups_practices_table,
    practice_status_table,
    exclusion_reason_table,
)
from portal.models import (
    Recruit,
    RecruitSummary,
    Delegate,
    Practice,
    PracticeGroup,
    PracticeStatus,
    ExclusionReason,
)
from portal import create_app


def import_practice_status():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_practice_status (
            id INT PRIMARY KEY,
            name VARCHAR(255)
        );
        """)

    db.engine.execute("""
        CREATE UNIQUE INDEX idx__etl_practice_status__name ON etl_practice_status(name);
        """)

    imports = []

    with etl_import_database() as r_db:
        for r in r_db.execute(practice_status_table.select()):
            imports.append(PracticeStatus(
                id=r['id'],
                name=r['name'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


def import_recruits():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_recruit (
            status VARCHAR(255),
            nhs_number VARCHAR(255),
            study_id VARCHAR(255),
            practice_code VARCHAR(255),
            first_name VARCHAR(64),
            last_name VARCHAR(64),
            date_of_birth DATE,
            civicrm_contact_id INT,
            civicrm_case_id INT PRIMARY KEY,
            recruited_date DATE,
            invoice_year VARCHAR(255),
            invoice_quarter VARCHAR(255),
            reimbursed_status VARCHAR(255)
        );
        """)

    db.engine.execute("""
        CREATE INDEX idx__etl_recruit__nhs_number ON etl_recruit(nhs_number);
        """)

    db.engine.execute("""
        CREATE INDEX idx__etl_recruit__practice_code ON etl_recruit(practice_code);
        """)

    imports = []

    with etl_import_database() as r_db:
        for r in r_db.execute(recruit_table.select()):
            imports.append(Recruit(
                status=r['status'],
                nhs_number=r['nhs_number'],
                study_id=r['study_id'],
                practice_code=r['practice_code'],
                first_name=r['first_name'],
                last_name=r['last_name'],
                date_of_birth=r['date_of_birth'],
                civicrm_contact_id=r['civicrm_contact_id'],
                civicrm_case_id=r['civicrm_case_id'],
                recruited_date=r['recruited_date'],
                invoice_year=r['invoice_year'],
                invoice_quarter=r['invoice_quarter'],
                reimbursed_status=r['reimbursed_status'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


def import_recruit_summary():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_recruit_summary (
            practice_code VARCHAR(100),
            recruited INTEGER,
            excluded INTEGER,
            withdrawn INTEGER,
            last_recruited_date DATE,
            excluded_percentage DECIMAL(30, 4),
            withdrawn_percentage DECIMAL(30, 4)
        );
        """)

    db.engine.execute("""
        CREATE INDEX idx__etl_recruit_summary__practice_code ON etl_recruit_summary(practice_code);
        """)

    imports = []

    with etl_import_database() as r_db:
        for r in r_db.execute(recruit_summary_table.select()):
            imports.append(RecruitSummary(
                practice_code=r['practice_code'],
                recruited=r['recruited'],
                excluded=int(r['excluded']),
                withdrawn=int(r['withdrawn']),
                last_recruited_date=r['last_recruited_date'],
                excluded_percentage=r['excluded_percentage'],
                withdrawn_percentage=r['withdrawn_percentage'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


def import_delegates():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_delegate (
            practice_code VARCHAR(255),
            instance INT,
            name VARCHAR(255),
            role VARCHAR(255),
            gcp_trained BIT,
            gv_trained BIT,
            on_delegation_log_yn BIT,
            gv_start_del_log DATE,
            gv_end_del_log DATE,
            rsn_not_on_del_log VARCHAR(500),
            gv_phone_a VARCHAR(100),
            gv_phone_b VARCHAR(100),
            contact_email_add VARCHAR(100),
            primary_contact_yn BIT
        );
        """)

    db.engine.execute("""
        CREATE INDEX idx__etl_delegates__practice_code ON etl_delegate(practice_code);
        """)

    imports = []

    with etl_import_database() as r_db:
        for r in r_db.execute(delegate_table.select()):
            imports.append(Delegate(
                practice_code=r['practice_code'],
                instance=r['instance'],
                name=r['name'],
                role=r['role'],
                gcp_trained=r['gcp_trained'],
                gv_trained=r['gv_trained'],
                on_delegation_log_yn=r['on_delegation_log_yn'],
                gv_start_del_log=parse_date(r['gv_start_del_log']),
                gv_end_del_log=parse_date(r['gv_end_del_log']),
                gv_phone_a=r['gv_phone_a'],
                gv_phone_b=r['gv_phone_b'],
                contact_email_add=r['contact_email_add'],
                primary_contact_yn=r['primary_contact_yn'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


def import_practices():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_practice_detail (
            project_id INT,
            ccg INT,
            federation INT,
            code VARCHAR(255),
            name VARCHAR(255),
            street_address VARCHAR(255),
            town VARCHAR(255),
            city VARCHAR(255),
            county VARCHAR(255),
            postcode VARCHAR(255),
            partners VARCHAR(255),
            collab_ag_comp_yn BIT,
            collab_ag_signed_date_str VARCHAR(100),
            isa_comp_yn BIT,
            isa_1_signed_date_str VARCHAR(255),
            isa_1_caldicott_guard_end_str VARCHAR(255),
            agree_66_comp_yn BIT,
            agree_66_signed_date_1_str VARCHAR(255),
            agree_66_end_date_2_str VARCHAR(255),
            genvasc_initiated BIT,
            status_id INT NULL
        );
        """)

    db.engine.execute("""
        CREATE INDEX idx__etl_practice_detail__practice_code ON etl_practice_detail(code);
        """)
    db.engine.execute("""
        CREATE INDEX idx__etl_practice_detail__ccg ON etl_practice_detail(ccg);
        """)
    db.engine.execute("""
        CREATE INDEX idx__etl_practice_detail__federation ON etl_practice_detail(federation);
        """)

    imports = []

    with etl_import_database() as r_db:
        for r in r_db.execute(practice_table.select()):
            imports.append(Practice(
                project_id=r['project_id'],
                code=r['code'],
                name=r['name'],
                ccg=r['ccg'],
                street_address=r['street_address'],
                town=r['town'],
                city=r['city'],
                county=r['county'],
                postcode=r['postcode'],
                federation=r['federation'],
                partners=r['partners'],
                collab_ag_comp_yn=r['collab_ag_comp_yn'],
                collab_ag_signed_date_str=parse_date(r['collab_ag_signed_date_str']),
                isa_comp_yn=r['isa_comp_yn'],
                isa_1_signed_date_str=parse_date(r['isa_1_signed_date_str']),
                isa_1_caldicott_guard_end_str=parse_date(r['isa_1_caldicott_guard_end_str']),
                agree_66_comp_yn=r['agree_66_comp_yn'],
                agree_66_signed_date_1_str=parse_date(r['agree_66_signed_date_1_str']),
                agree_66_end_date_2_str=parse_date(r['agree_66_end_date_2_str']),
                genvasc_initiated=r['genvasc_initiated'] in ('1', 1),
                status_id=r['status_id'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


def import_practice_groups():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_practice_group (
            project_id INT,
            identifier VARCHAR(255),
            type VARCHAR(255),
            name VARCHAR(255),
            PRIMARY KEY (project_id, identifier, type)
        );
        """)

    db.engine.execute("""
        CREATE INDEX idx__etl_practice_group__type ON etl_practice_group(type);
        """)

    imports = []

    with etl_import_database() as r_db:
        for r in r_db.execute(practice_group_table.select()):
            imports.append(PracticeGroup(
                project_id=r['project_id'],
                type=r['type'],
                identifier=r['identifier'],
                name=r['name'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


def import_practice_groups_practices():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_practice_groups_practices (
            practice_group_type VARCHAR(200),
            practice_group_project_id INT,
            practice_group_identifier INT,
            practice_code VARCHAR(255),
            PRIMARY KEY (practice_group_type, practice_group_project_id, practice_group_identifier, practice_code)
        );
        """)

    with etl_import_database() as r_db:
        for r in r_db.execute(practice_groups_practices_table.select()):
            try:
                p = Practice.query.filter_by(code=r['practice_code']).one()
                pg = PracticeGroup.query.filter_by(
                    type=r['practice_group_type'],
                    project_id=r['practice_group_project_id'],
                    identifier=r['practice_group_identifier'],
                ).one()

                pg.practices.add(p)
                db.session.add(pg)
            except:
                print(r['practice_group_type'])
                print(r['practice_group_project_id'])
                print(r['practice_group_identifier'])

    db.session.commit()


def import_exclusion_reasons():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_exclusion_reason (
            civicrm_case_id INT PRIMARY KEY,
            details VARCHAR(500)
        );
        """)

    imports = []

    with etl_import_database() as r_db:
        for r in r_db.execute(exclusion_reason_table.select()):
            imports.append(ExclusionReason(
                civicrm_case_id=r['civicrm_case_id'],
                details=r['details'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


# Load environment variables from '.env' file.
load_dotenv()

app = create_app()
context = app.app_context()
context.push()

import_practice_status()
import_practice_groups()
import_practices()
import_recruits()
import_recruit_summary()
import_delegates()
import_practice_groups_practices()
import_exclusion_reasons()

context.pop()
