# The new objects imported here are redirect and g.  redirect is used to
# issue a redirect back to the web browser to have it request another
# app endpoint.  g is a per-request object used to store global state during
# a request.  (You've seen url_for already in your Jinja templates.)

from flask import Flask, render_template, session, request, redirect, \
                  url_for, g

# connect is used to connect to a PostgreSQL database.

from psycopg2 import connect

# DictCursor allows us to work with the results returned by fetch
# operations on a cursor as if they were stored in a dictionary, rather
# than a tuple.  tuple access via an index is still possible.

from psycopg2.extras import DictCursor


# As necessary, add variable definitions to your cs417secrets.py file.
# Remember, they should have the form
#     DBDEMO_DB = 'registration'
# These definitions will be stored in the app.config object as dictionary
# key and value pairs.  See below.

app = Flask(__name__)
app.config.from_pyfile('config.py')


# This decorator is used to register a function to be called first during
# the request.  Use it to establish session initialization.  The registered
# function should be parameterless.

@app.before_request
def beforeReq():
    if 'loggedIn' not in session:
        session['loggedIn'] = False
        session.modified = True


# This decorator is used to register a function to be called once the
# request is completed.  Use it to clean-up at the end of a request.  The
# registered function takes a response object parameter and returns a response
# object.

@app.after_request
def afterReq(response):
    closeDb()
    return response


# Get the connection to the back-end db.  If the connection doesn't yet
# exist, create it.  Note how to access your application "secrets" via
# the app.config dictionary.

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


@app.route('/')
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        # User is already logged in.  Redirect browser to the query end point.
        if session['loggedIn']:
            return redirect(url_for('query'))
        else:
            return render_template('login.html')
    # The request is a POST.
    else:
        # Get login credentials from the form.
        user = request.form['user']
        passwd = request.form['passwd']

        # Open a cursor using a context manager.  The cursor will be closed
        # when the context is exited.  Cursors are used to interact with
        # the records returned by a query.  See the documentation for the
        # Cursor class in psycopg2 for details.
        with getDb().cursor() as cur:
            # %(usr)s is a named parameter in the query string.
            # vars is a dictionary specifying the mapping from the
            # named parameters to their values.  Constructing the query
            # in this fashion allows psycopg2 to properly escape input
            # from users, preventing SQL injection attacks.
            query = 'select password from users where username=%(usr)s;'
            vars = {'usr' : user}
            cur.execute(query, vars)
            result = cur.fetchone()
            # By default, any DB operation, even a read, opens a transaction.
            # It's best to not leave an unneeded transaction hanging around,
            # so let's commit it.
            getDb().commit()

        # If user isn't in users, result will be None.  Attempt to
        # authenticate user.
        if result != None and passwd == result['password']:
            session['loggedIn'] = True
            session['user'] = user
            session.modified = True
            return render_template('query.html', user=session['user'])
        else:
            return render_template('login.html')


@app.route('/query', methods = ['POST', 'GET'])
def query():
    if not session['loggedIn']:
        return render_template('login.html')

    if request.method == 'GET':
        return render_template('query.html', user=session['user'])

    # The request is a POST.
    else:
        query = request.form['query']
        try:
            with getDb().cursor() as cur:
                # Generally, allowing a user to input an arbitrary SQL
                # statement is a VERY BAD IDEA (don't do it), but this
                # database is read-only for the user passed in the
                # connection request.
                cur.execute(query)
                results = cur.fetchall()
                getDb().commit()
            return render_template('result.html',
                                   user=session['user'],
                                   query=query, results=results)

        # The query resulted in some error.
        except:
            return render_template('result.html', user=session['user'],
                                   query= query
                                   + ', which had an error.',
                                   results = [])


@app.route('/logout')
def logout():
    # Delete all session variables.  I suppose I could keep loggedIn, but
    # the registered before_request function will handle this.
    session.clear()
    session.modified = True
    return render_template('logout.html')


if __name__ != '__main__':
    application = app
