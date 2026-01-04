#!/usr/bin/env python3

import pytest
from app import app, db


@pytest.fixture(autouse=True, scope='function')
def setup_database():
    """Create database tables before each test and drop after."""
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()


def pytest_configure(config):
    """Create all database tables once at the start of the test session."""
    with app.app_context():
        db.create_all()


def pytest_unconfigure(config):
    """Drop all database tables at the end of the test session."""
    with app.app_context():
        db.drop_all()


def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = ' '.join((pref, suf))
