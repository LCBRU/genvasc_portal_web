#!/usr/bin/env python
import os
from contextlib import contextmanager
from portal.utils import parse_date
from dotenv import load_dotenv
from portal.database import db
from portal.etl.database import (
    etl_import_database,
    recruit_table,
    delegate_table,
    practice_table,
    practice_group_table,
    practice_groups_practices_table,
)
from portal.models import (
    Recruit,
    Delegate,
    Practice,
    PracticeGroup,
    PracticeGroupPractice,
)
from portal import create_app


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
            processed_by VARCHAR(128),
            processed_date DATE,
            date_recruited DATE,
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
                processed_date=r['processed_date'],
                date_recruited=r['recruited_date'],
                invoice_year=r['invoice_year'],
                invoice_quarter=r['invoice_quarter'],
                reimbursed_status=r['reimbursed_status'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


def import_delegates():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_delegate (
            id INT AUTO_INCREMENT,
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
            id INT AUTO_INCREMENT,
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
            genvasc_initiated BIT,
            status INT
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
                genvasc_initiated=r['genvasc_initiated'] == 1,
                status=r['status'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


def import_practice_groups():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_practice_group (
            id INT PRIMARY KEY,
            type VARCHAR(255),
            name VARCHAR(255)
        );
        """)

    db.engine.execute("""
        CREATE INDEX idx__etl_practice_group__type ON etl_practice_group(type);
        """)

    imports = []

    with etl_import_database() as r_db:
        for r in r_db.execute(practice_group_table.select()):
            imports.append(PracticeGroup(
                id=r['id'],
                type=r['type'],
                name=r['name'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


def import_practice_groups_practices():
    db.engine.execute("""
        CREATE TABLE IF NOT EXISTS etl_practice_groups_practices (
            practice_group_id INT,
            practice_code VARCHAR(255),
            PRIMARY KEY (practice_group_id, practice_code)
        );
        """)

    db.engine.execute("""
        CREATE INDEX idx__etl_practice_groups_practices__practice_code__practice_group_id ON etl_practice_groups_practices(practice_code, practice_group_id);
        """)

    imports = []

    with etl_import_database() as r_db:
        for r in r_db.execute(practice_groups_practices_table.select()):
            imports.append(PracticeGroupPractice(
                practice_group_id=r['practice_group_id'],
                practice_code=r['practice_code'],
            ))

    db.session.add_all(imports)
    db.session.flush()

    db.session.commit()


# Load environment variables from '.env' file.
load_dotenv()

app = create_app()
context = app.app_context()
context.push()

import_practice_groups()
import_practices()
import_recruits()
import_delegates()
import_practice_groups_practices()

context.pop()
