from flask import Flask, render_template, session, request, redirect, \
        url_for, g
from psycopg2 import connect
from psycopg2.extras import DictCursor

app = Flask(__name__)
app.config.from_pyfile('config.py')

#@app.route('/')
#def home():
#    return render_template('index.html')

#@app.route('/proposal/')
#def proposal():
#    return render_template('proposal.html')

#@app.route('/ER_Diagram')
#def er_diagram():
    #return render_template('univent_er_diagram.pdf')
