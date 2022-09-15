"""auth_server model (database) API."""
from datetime import timedelta
import time
import flask
import mct_checkin
from mct_checkin.gmail import send_mail


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
    return 'logname' in mct_checkin.attendance


def send_attendance():
    """wait half an hour and send attendance."""

    # delay = 30 * 60
    delay = 1
    time.sleep(delay)
    
    # send email
    send_mail(mct_checkin.attendance)
    print("mail sent. clearing attendance...")
    # clear attendance dict
    mct_checkin.attend_lock.acquire()
    mct_checkin.attendance = []
    mct_checkin.attend_lock.release()
    print("attendance cleared.")
    


def add_attend(logname: str):
    """add someone to attendance"""
    mct_checkin.attend_lock.acquire()
    mct_checkin.attendance.append(logname)
    mct_checkin.attend_lock.release()
