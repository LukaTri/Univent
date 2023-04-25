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


def sqlQuery(query: str, kwargs:dict):
    with getDb().cursor() as cur:
        cur.execute(query, kwargs)
        result = cur.fetchone()
        getDb().commit()

    return result


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



        # with getDb().cursor() as cur:
        query = 'SELECT first_name, password FROM Users WHERE email=%(usr)s;'
        vars = {'usr' : user}
            # cur.execute(query, vars)
            # result = cur.fetchone()
        result = sqlQuery(query, vars)
        print(result)
            # getDb().commit()
        
        if result != None and password == result['password']:
            session['loggedIn'] = True
            session['user'] = result[0] 
            session.modified = True
            return redirect(url_for('success', user=session['user']))
        else:
            return render_template('login.html')


@app.route('/success/<user>/')
def success(user=None):
    return render_template('success.html', user=session['user'])

@app.route('/logout/')
def logout():
    session.clear()
    session.modified = True
    print(session)
    return render_template('logout.html')


@app.route('/event-registration/<user>/', methods=['POST', 'GET'])
def registration(user=None):

    if request.method == 'POST':
        event_name = request.form['eventname']
        est_attd = request.form['estimatedattendance']
        event_desc = request.form['eventdescription']
        first_loc_pref = request.form['firstLocationPreference']
        second_loc_pref= request.form['secondLocationPreference']
        date = request.form['eventdate']
        start_time = request.form['starttime']
        end_time = request.form['endtime']
        session_user = session['user']

        print(f'Event Name: {event_name}')
        print(f'Estimated Attendance: {est_attd}')
        print(f'Event Description: {event_desc}')
        print(f'Primary Location: {first_loc_pref}')
        print(f'Secondary Location: {second_loc_pref}')
        print(f'Date entered: {date}')
        print(f'Start time entered: {start_time}')
        print(f'End time entered: {end_time}')
        print(f'The user in question: {session_user}')

    return render_template('eventReg.html')

if __name__ != '__main__':
    application=app