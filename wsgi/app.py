from flask import Flask, render_template, session, request, redirect, \
        url_for, g
from psycopg2 import connect
from psycopg2.extras import DictCursor

app = Flask(__name__)
app.config.from_pyfile('config.py')

def getDb():
    if 'db' not in g:
        g.db = connect(dbname=app.config['UNIVENT_DB'],
                       user=app.config['UNIVENT_USER'],
                       password=app.config['UNIVENT_PW'],
                       cursor_factory=DictCursor)
    return g.db

def closeDb():
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.before_request
def beforeReq():
    if 'loggedIn' not in session:
        session['loggedIn'] = False
        session.modified = True


@app.after_request
def afterReq(response):
    closeDb()
    return response


@app.route('/', methods=['POST', 'GET'])
def login():
    print(session)
    if request.method == 'GET':
        if session['loggedIn']:
            return redirect(url_for('success', user=session['user']))
        else:
            return render_template('login.html')
    else: 
        # Get the username and password input from HTML
        user = request.form['user']
        password = request.form['passwd']
        print(f'User Entered: {user}\nPassword Entered: {password}')

        with getDb().cursor() as cur:
            query = 'SELECT password FROM Users WHERE user_id=%(usr)s;'
            vars = {'usr' : user}
            cur.execute(query, vars)
            result = cur.fetchone()
            getDb().commit()
        
        if result != None and password == result['password']:
            session['loggedIn'] = True
            session['user'] = user
            session.modified = True
            return redirect(url_for('success', user=session['user']))
        else:
            return render_template('login.html')


@app.route('/success/<user>/')
def success(user=None):
    return render_template('success.html', user=session['user'])

@app.route('/logout/')
def logout():
    session.pop("user", None)
    session['loggedIn'] = False
    session.modified = True
    print(session)
    return render_template('logout.html')


@app.route('/event-registration/', methods=['POST', 'GET'])
def registration():
    return render_template('eventReg.html')