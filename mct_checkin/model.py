"""auth_server model (database) API."""
from datetime import timedelta
import time
import flask
import mct_checkin
import sqlite3
import pathlib


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in flask.g:
        db_filename = mct_checkin.app.config['DATABASE_FILENAME']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory
        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")
    return flask.g.sqlite_db


@mct_checkin.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()


@mct_checkin.app.before_request
def make_session_permanent():
    flask.session.permanent = True
    mct_checkin.app.permanent_session_lifetime = timedelta(minutes=5)
    
    
def check_session():
    """Check if logname exists in session."""
    if 'logname' not in flask.session:
        return False
    return flask.session['logname']



def insert_attendance(logname):
    """commit attendance to db."""

    database = get_db()
    cur = database.execute(
        "INSERT INTO participants "
        "(uniqname)"
        "VALUES(?)",
        (logname,)
    )
    cur.fetchone()
    
def get_attendance_history():
    """fetch all distinct attendance history."""

    database = get_db()
    cur = database.execute(
        "SELECT * "
        "FROM participants "
        "ORDER BY ts"
    )
    attendance = cur.fetchall()
    return attendance


import datetime

def round_minutes(dt, direction, resolution):
    new_minute = (dt.minute // resolution + (1 if direction == 'up' else 0)) * resolution

    return dt + datetime.timedelta(minutes=new_minute - dt.minute), abs(new_minute - dt.minute)

def round_nearest(ts: datetime.datetime, resolution=30):
    f = '%Y-%m-%d %H:%M:%S'
    
    dt = datetime.datetime.strptime(ts, f)

    min_delta = 1e6
    new_time = None
    for direction in 'up', 'down':
        new_t, delta = round_minutes(dt, direction, resolution)
        if delta < min_delta:
            new_time = new_t
            min_delta = delta

    return new_time