from datetime import datetime
import mct_checkin
import flask


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
        # TODO fix attendance check
        # attendance = mct_checkin.model.check_attendance(logname)
        
        if logname:
            context["logname"] = logname
        # if attendance:
        #     context["attendance"] = attendance

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

    context = {
        "attendance": {}
    }

    # sort by half hours
    s = set()
    for d in attendance:
        ts = d["ts"]
        uniqname = d["uniqname"]
        # TODO: datetime data type
        dt = mct_checkin.model.round_nearest(ts)
        
        date = dt.strftime("%m/%d")
        
        ts = dt.strftime("%H:%M %p")

        if date not in context["attendance"]:
            context["attendance"][date] = {}
            
        if ts not in context["attendance"][date]:
            context["attendance"][date][ts] = set()

        context["attendance"][date][ts].add(uniqname)

    return flask.render_template("attendance.html", **context)
    
    
# @mct_checkin.app.route("/logout/", methods=["POST"])
@mct_checkin.app.route("/logout/")
def logout():
    """view for logging out."""
    flask.session.clear()
    
    return flask.redirect("/")
    