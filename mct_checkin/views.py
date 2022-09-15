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
        attendance = mct_checkin.model.check_attendance()
        
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
    flask.session["attendance"] = True
    
    return flask.redirect("/")
    
    
# @mct_checkin.app.route("/logout/", methods=["POST"])
@mct_checkin.app.route("/logout/")
def logout():
    """view for logging out."""
    flask.session.clear()
    
    return flask.redirect("/")
    