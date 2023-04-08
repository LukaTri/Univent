# A simple Flask app demonstrating the use of sessions, variable sections
# in a URL, and the Jinja templating language.


# Note what has to be imported.
from flask import Flask, render_template, session


# Create the application object and configure it.  ALL configuration should
# be done in config.py, so that the application file (this file) only
# contains application logic.
app = Flask(__name__)
app.config.from_pyfile('config.py')


# Decorate pageCount with two URLs, the second of which contains a
# variable (page) section.
@app.route('/')
@app.route('/<page>/')
def pageCount(page=None):
    # If necessary, create session variables.
    # session is a dict.
    if 'whichPage' not in session:
        # Which page we're on.
        session['whichPage'] = 0
        # List of page visit counts.  Index 0 is a 'dummy' value.
        session['counts'] = [0, 0, 0, 0, 0]

    try:
        page = int(page)
    except:
        # Default, if int conversion fails.
        page = 0

    # Validate page.
    if 1 <= page <= 4:
        session['whichPage'] = page
        session['counts'][page] += 1

    # Call Jinja's render_template method, which will return an HTML
    # document.  This document will eventually be passed to the web
    # browser.  HTML templates should be in the 'templates' directory.
    # whichPage is being passed as a parameter.  Note that Jinja is
    # reading counts directly from the session dict in pageCount.html.
    return render_template('pageCount.html',
                           whichPage=session['whichPage'])


@app.route('/reset')
def reset():
    # Remove session variables.  Including 'None' prevents an error
    # when the session variables aren't present in the session dict.
    session.pop('counts', None)
    session.pop('whichPage', None)
    return render_template('pageCountReset.html')


# If the application is being run by Apache's WSGI module, which expects the
# application object to be named 'application', then set application.
#
# Apache is configured to only allow connections from systems on Goucher's
# internal network.  Further, the system must be on a wired connection or
# connected to GoucherWifi.  Phoenix meets these criteria.
if __name__ != '__main__':
    application = app
