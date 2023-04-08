# A simple Flask app demonstrating form processing.


# request must be imported to access form data.
from flask import Flask, render_template, session, request


app = Flask(__name__)
app.config.from_pyfile('config.py')


# By default, decorated methods are only called when HTTP GET is used.
# Form submission uses HTTP POST.
@app.route('/', methods = ['POST', 'GET'])
def process():
    if 'name' not in session:
        session['name'] = ''

    if request.method == 'POST':
        # Form data is accessed via the request.form dict.
        # Keys here correspond to the name attributes of the form's
        # input elements.
        if request.form['button'] == 'reset':
            session['name'] = ''
        else:
            session['name'] = request.form['name']

    return render_template('form.html')


if __name__ != '__main__':
    application = app
