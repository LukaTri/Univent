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

def multiSqlQuery(query: str, kwargs:dict):
    with getDb().cursor() as cur:
        cur.execute(query, kwargs)
        result = cur.fetchall()
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

        query = 'SELECT first_name, password, user_id FROM Users WHERE email=%(usr)s;'
        vars = {'usr' : user}
        result = sqlQuery(query, vars)
        print(result)
        
        if result != None and password == result['password']:
            session['loggedIn'] = True
            session['user'] = result[0]
            session['usr_id'] = result[2]
            session.modified = True
            return redirect(url_for('success', user=session['user']))
        else:
            return render_template('login.html')


@app.route('/success/<user>/', methods=['GET', 'POST'])
def success(user=None):
    events = []

    user_kwargs = {
        "usr_id":session['usr_id']
    }
    club_query = "SELECT club_name FROM Members m, Users s\
        WHERE %(usr_id)s = m.user_id;"
        # WHERE %(usr_id)s = %(usr_id)s;"
    
    club_result = sqlQuery(club_query, user_kwargs)
    session['club_name'] = club_result[0]

    kwargs = {
        "clubname" : session['club_name']
    }
    query = "SELECT event_name, event_date, primary_loc FROM\
        Event WHERE club_name = %(clubname)s;"
    result = multiSqlQuery(query, kwargs)

    if not result:
        result
    else:
        for i in result:
            print(i)
            print(type(i))
            events.append(i)

    return render_template('success.html', user=session['user'], events=events)

@app.route('/logout/')
def logout():
    session.clear()
    session.modified = True
    return render_template('logout.html')


@app.route('/event-registration/<user>/', methods=['POST', 'GET'])
def registration(user=None):

    user_kwargs = {
        "usr_id":session['usr_id']
    }
    club_query = "SELECT club_name FROM Members m, Users s\
        WHERE %(usr_id)s = m.user_id;"
        # WHERE %(usr_id)s = %(usr_id)s;"
    
    club_result = sqlQuery(club_query, user_kwargs)
    session['club_name'] = club_result[0]

    if request.method == 'POST':
        kwargs= {
        "eventname" : request.form['eventname'],
        "estimatedattendance" : request.form['estimatedattendance'],
        "eventdescription" : request.form['eventdescription'],
        "firstLocationPreference" : request.form['firstLocationPreference'],
        "secondLocationPreference" : request.form['secondLocationPreference'],
        "eventdate" : request.form['eventdate'],
        "starttime" : request.form['starttime'],
        "endtime" : request.form['endtime'],
        "clubname" : session['club_name'],
        }

        # eventname = request.form['eventname']
        # estimatedattendance = request.form['estimatedattendance']
        # eventdescription = request.form['eventdescription']
        # firstLocationPreference = request.form['firstLocationPreference']
        # secondLocationPreference = request.form['secondLocationPreference']
        # eventdate = request.form['eventdate']
        # starttime = request.form['starttime']
        # endtime = request.form['endtime']
        # user = session['user']
        # print(f'Event Name: {eventname}')
        # print(f'Estimated Attendance: {estimatedattendance}')
        # print(f'Event Description: {eventdescription}')
        # print(f'Primary Location: {firstLocationPreference}')
        # print(f'Secondary Location: {secondLocationPreference}')
        # print(f'Date entered: {eventdate}')
        # print(f'Start time entered: {starttime}')
        # print(f'End time entered: {endtime}')
        # print(f'The user in question: {user}')

        query = "INSERT INTO Event (\
            event_name, club_name, event_time,\
            event_date, est_attendance, event_desc,\
            primary_loc, secondary_loc)\
            VALUES(\
            %(eventname)s,\
            %(clubname)s,\
            %(starttime)s,\
            %(eventdate)s,\
            %(estimatedattendance)s,\
            %(eventdescription)s,\
            %(firstLocationPreference)s,\
            %(secondLocationPreference)s\
        ) RETURNING event_name, event_date, primary_loc;"
        results = sqlQuery(query, kwargs)
        print(results)
        return redirect(url_for('success', user=session['user']))

    return render_template('eventReg.html')

if __name__ != '__main__':
    application=app