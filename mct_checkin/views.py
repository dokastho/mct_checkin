from logging import LoggerAdapter
import mct_checkin
import flask
from threading import Thread


@mct_checkin.app.route("/")
def show_index():
    """render index page"""
    with mct_checkin.app.app_context():
        # logname must exist in session
        context = {
            "logname": "",
            "attendance": False
        }
        
        logname = mct_checkin.model.check_session()
        attendance = mct_checkin.model.check_attendance(logname)
        
        if logname:
            context["logname"] = logname
        if attendance:
            context["attendance"] = attendance

    return flask.render_template("index.html", **context)


@mct_checkin.app.route("/submit/", methods=["POST"])
def check_in():
    """view for submitting checkin form."""
    
    logname = flask.request.form.get('logname')
    
    flask.session["logname"] = logname
    mct_checkin.insert_attendance(logname)
    
    return flask.redirect("/")

@mct_checkin.app.route("/attendance/")
def show_attendance():
    """Display attendance for past rides."""

    attendance = mct_checkin.model.get_attendance_history()

    context = {}

    # sort by half hours
    s: set()
    for ts, uniqname in attendance.values():
        # TODO: datetime data type
        new_ts = mct_checkin.model.round_nearest(ts)

        if new_ts not in context:
            context[new_ts] = set()

        context[new_ts].insert(uniqname)

    flask.render_template("attendance.html", context)
    
    
# @mct_checkin.app.route("/logout/", methods=["POST"])
@mct_checkin.app.route("/logout/")
def logout():
    """view for logging out."""
    flask.session.clear()
    
    return flask.redirect("/")
    