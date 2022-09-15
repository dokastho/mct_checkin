"""auth_server model (database) API."""
from datetime import timedelta
import flask
import mct_checkin


@mct_checkin.app.before_request
def make_session_permanent():
    flask.session.permanent = True
    mct_checkin.app.permanent_session_lifetime = timedelta(minutes=5)
    
    
def check_session():
    """Check if logname exists in session."""
    if 'logname' not in flask.session:
        return False
    return flask.session['logname']

def check_attendance():
    """Check if logname exists in session."""
    if 'logname' not in flask.session:
        return False
    if 'attendance' not in flask.session:
        return False
    
    return flask.session['attendance']
