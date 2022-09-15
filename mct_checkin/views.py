import mct_checkin
import flask

@mct_checkin.app.route("/")
def show_index():
    """render index page"""
    with mct_checkin.app.app_context():
        # logname must exist in session
        context = {
            "logname": ""
        }
        logname = mct_checkin.model.check_session()
        if logname:
            context["logname"] = logname

    return flask.render_template("index.html", **context)


@mct_checkin.app.route("/submit/", methods=["POST"])
def check_in():
    """view for submitting checkin form."""
    