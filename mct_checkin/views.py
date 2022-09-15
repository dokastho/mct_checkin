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
    
    # start the timer to submit if necessary
    mct_checkin.attend_lock.acquire()
    if len(mct_checkin.attendance) == 0:
        t = Thread(target=mct_checkin.send_attendance, args=())
        t.start()
    mct_checkin.attend_lock.release()
    
    logname = flask.request.form.get('logname')
    
    flask.session["logname"] = logname
    mct_checkin.add_attend(logname)
    
    return flask.redirect("/")
    
    
# @mct_checkin.app.route("/logout/", methods=["POST"])
@mct_checkin.app.route("/logout/")
def logout():
    """view for logging out."""
    flask.session.clear()
    
    return flask.redirect("/")
    