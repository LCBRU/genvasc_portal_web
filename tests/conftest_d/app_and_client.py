# -*- coding: utf-8 -*-

import json
import pytest
import datetime
from flask import Response
from flask.testing import FlaskClient
from bs4 import BeautifulSoup
from portal import create_app
from portal.database import db
from portal.config import TestConfig, TestConfigCRSF
from portal.etl.database import (
    practice_etl_meta,
    etl_practice_database,
    recruit_etl_meta,
)


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime) or isinstance(o, datetime.date):
            return o.isoformat()

        return json.JSONEncoder.default(self, o)


class CustomResponse(Response):
    def __init__(self, baseObject):
        self.__class__ = type(
            baseObject.__class__.__name__, (self.__class__, baseObject.__class__), {}
        )
        self.__dict__ = baseObject.__dict__
        self._soup = None

    def get_json(self):
        return json.loads(self.get_data().decode("utf8"))

    @property
    def soup(self):
        if not self._soup:
            self._soup = BeautifulSoup(self.data, "html.parser")

        return self._soup


class CustomClient(FlaskClient):
    def __init__(self, *args, **kwargs):
        super(CustomClient, self).__init__(*args, **kwargs)

    def post_json(self, *args, **kwargs):

        kwargs["data"] = json.dumps(kwargs.get("data"), cls=DateTimeEncoder)
        kwargs["content_type"] = "application/json"

        return CustomResponse(super(CustomClient, self).post(*args, **kwargs))

    def get(self, *args, **kwargs):
        return CustomResponse(super(CustomClient, self).get(*args, **kwargs))

    def post(self, *args, **kwargs):
        return CustomResponse(super(CustomClient, self).post(*args, **kwargs))


@pytest.yield_fixture(scope="function")
def app(faker):
    app = create_app(TestConfig)
    app.test_client_class = CustomClient
    context = app.test_request_context()
    context.push()
    db.create_all()

    yield app

    context.pop()


@pytest.yield_fixture(scope="function")
def client(app):
    client = app.test_client()

    yield client


@pytest.yield_fixture(scope="function")
def client_with_crsf(faker):
    app = create_app(TestConfigCRSF)
    app.test_client_class = CustomClient
    context = app.test_request_context()
    context.push()
    db.create_all()

    client = app.test_client()

    yield client

    context.pop()


@pytest.yield_fixture(scope="function")
def etl_practice_db(app):
    with etl_practice_database() as db:
        practice_etl_meta.create_all()
        yield db
