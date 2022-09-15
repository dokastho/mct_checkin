"""auth_server model (database) API."""
from datetime import timedelta
import time
import flask
import mct_checkin
from mct_checkin.gmail import send_mail
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

def check_attendance(logname):
    """Check if logname exists in session."""
    return logname in mct_checkin.attendance


def send_attendance():
    """wait half an hour and send attendance."""

    # delay = 30 * 60
    delay = 1
    time.sleep(delay)
    
    # send email
    send_mail(mct_checkin.attendance)
    print("clearing attendance...")
    # clear attendance dict
    # mct_checkin.attend_lock.acquire()
    # mct_checkin.attendance = []
    # mct_checkin.attend_lock.release()
    print("attendance cleared.")
    


def add_attend(logname: str):
    """add someone to attendance"""
    mct_checkin.attend_lock.acquire()
    if logname in mct_checkin.attendance:
        print(f'{logname} already in attendannce')
    else:
        mct_checkin.attendance.append(logname)
    mct_checkin.attend_lock.release()
