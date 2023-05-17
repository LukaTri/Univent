from flask import Flask, render_template, session, request, redirect, url_for, g
from psycopg2 import connect
from psycopg2.extras import DictCursor
import datetime
import re

app = Flask(__name__)
app.config.from_pyfile("config.py")


def getDb():
    if "db" not in g:
        g.db = connect(
            dbname=app.config["UNIVENT_DB"],
            user=app.config["UNIVENT_USER"],
            password=app.config["UNIVENT_PW"],
            cursor_factory=DictCursor,
        )
    return g.db


def closeDb():
    db = g.pop("db", None)
    if db is not None:
        db.close()


def sqlQuery(query: str, kwargs: dict):
    with getDb().cursor() as cur:
        cur.execute(query, kwargs)
        result = cur.fetchone()
        getDb().commit()
    return result


def multiSqlQuery(query: str, kwargs: dict):
    with getDb().cursor() as cur:
        cur.execute(query, kwargs)
        result = cur.fetchall()
        getDb().commit()
    return result


@app.before_request
def beforeReq():
    if "loggedIn" not in session:
        session["loggedIn"] = False
        session.modified = True


@app.after_request
def afterReq(response):
    closeDb()
    return response


@app.route("/", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        if session["loggedIn"]:
            return redirect(url_for("success", user=session["user"]))
        else:
            return render_template("login.html")
    else:
        user = request.form["user"]
        password = request.form["passwd"]

        query = "SELECT first_name, password, user_id, user_type, email FROM Users WHERE email=%(usr)s;"
        vars = {"usr": user}
        result = sqlQuery(query, vars)

        if result != None and password == result["password"]:
            session["loggedIn"] = True
            session["user"] = result[0]
            session["usr_id"] = result[2]
            session["user_type"] = result[3]
            session["email"] = result[4]
            session.modified = True

            return redirect(url_for("homepage", user=session["user"]))

        else:
            return render_template("login.html")


@app.route("/success/<user>/", methods=["GET", "POST"])
def success(user=None):
    current_events = []
    past_events = []
    present = datetime.datetime.now()
    user_kwargs = {"usr_id": session["usr_id"]}
    club_query = "SELECT club_name FROM Members m, Users s\
        WHERE %(usr_id)s = m.user_id;"

    club_result = sqlQuery(club_query, user_kwargs)
    if club_result != None:
        session["club_name"] = club_result[0]

        kwargs = {"clubname": session["club_name"]}
        query = "SELECT event_name, event_date, primary_loc FROM\
            Event WHERE club_name = %(clubname)s;"
        result = multiSqlQuery(query, kwargs)

        for i in result:
            event_date = i["event_date"]

            if isinstance(event_date, datetime.date) and event_date < present.date():
                past_events.append(i)
            else:
                current_events.append(i)

    return render_template(
        "success.html",
        user=session["user"],
        user_type=session["user_type"],
        current_events=current_events,
        past_events=past_events,
    )


@app.route("/logout/")
def logout():
    session.clear()
    session.modified = True
    return render_template("logout.html")


@app.route("/event-registration/<user>/", methods=["POST", "GET"])
def registration(user=None):
    if request.method == "POST":
        kwargs = {
            "eventname": request.form["eventname"],
            "estimatedattendance": request.form["estimatedattendance"],
            "eventdescription": request.form["eventdescription"],
            "firstLocationPreference": request.form["firstLocationPreference"],
            "secondLocationPreference": request.form["secondLocationPreference"],
            "eventdate": request.form["eventdate"],
            "starttime": request.form["starttime"],
            "endtime": request.form["endtime"],
            "clubname": session["club_name"],
        }

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
        return redirect(url_for("homepage", user=session["user"]))

    return render_template("eventReg.html")


@app.route("/homepage/<user>/", methods=["GET"])
def homepage(user=None):
    # Logic for if a club member is logged in:
    if session["user_type"] == 1:
        current_events = []
        past_events = []
        club_members = []
        present = datetime.datetime.now()

        user_kwargs = {"usr_id": session["usr_id"]}
        club_query = "SELECT club_name, m.title, m.phone_number, s.email FROM Members m, Users s\
            WHERE %(usr_id)s = m.user_id;"

        club_result = sqlQuery(club_query, user_kwargs)
        if club_result != None:
            session["club_name"] = club_result[0]
            club_result["phone_number"] = re.sub(
                r"(\d{3})(\d{3})(\d{4})", r"\1-\2-\3", club_result["phone_number"]
            )

            kwargs = {"clubname": session["club_name"]}
            query = "SELECT event_name, event_date, primary_loc FROM\
                Event WHERE club_name = %(clubname)s;"
            result = multiSqlQuery(query, kwargs)

            for i in result:
                event_date = i["event_date"]

                if (
                    isinstance(event_date, datetime.date)
                    and event_date < present.date()
                ):
                    past_events.append(i)
                else:
                    current_events.append(i)


            get_members_kwargs = {"clubname":session['club_name'],
                                  "advisor":"Advisor",}
            get_members_query = """
            SELECT U.first_name, U.last_name, M.title
            FROM Users U
            JOIN Members M ON U.user_id = M.user_id
            WHERE M.title <> %(advisor)s
            AND M.club_name = %(clubname)s;
            """

            get_members_result = multiSqlQuery(get_members_query, get_members_kwargs)

            get_advisor_kwargs = {"clubname":session['club_name'],
                                  "advisor":"Advisor",}
            get_advisor_query = """
            SELECT U.first_name, U.last_name, U.email, M.phone_number
            FROM Users u
            JOIN Members M on U.user_id = M.user_id
            WHERE M.title = %(advisor)s
            AND M.club_name = %(clubname)s;
            """

            get_advisor_result = sqlQuery(get_advisor_query, get_advisor_kwargs)

            get_advisor_result["phone_number"] = re.sub(
                r"(\d{3})(\d{3})(\d{4})", r"\1-\2-\3", get_advisor_result["phone_number"]
            )

        return render_template(
            "homePage.html",
            user=session["user"],
            user_type=session["user_type"],
            current_events=current_events,
            past_events=past_events,
            member=club_result,
            non_advisors=get_members_result,
            advisors=get_advisor_result,
        )

    # Logic for if an OSE member is logged in:
    else:
        current_events = []
        past_events = []
        present = datetime.datetime.now()

        user_kwargs = {"usr_id": session["usr_id"]}
        club_query = "SELECT first_name, last_name, email FROM Users\
            WHERE %(usr_id)s = user_id;"

        ose_result = sqlQuery(club_query, user_kwargs)

        # Necessary dictionary argument
        get_club_kwargs = {"": ""}
        get_club_query = "SELECT event_name, event_date, primary_loc\
            FROM Event;"

        get_club_result = multiSqlQuery(get_club_query, get_club_kwargs)

        for i in get_club_result:
            event_date = i["event_date"]
            if isinstance(event_date, datetime.date) and event_date < present.date():
                past_events.append(i)
            else:
                current_events.append(i)

        return render_template(
            "oseHome.html",
            user=session["user"],
            user_type=session["user_type"],
            first_name=ose_result["first_name"],
            last_name=ose_result["last_name"],
            email=ose_result["email"],
            current_events=current_events,
            past_events=past_events,
        )


@app.route("/register-user/<user>/", methods=["POST", "GET"])
def register_user(user=None):
    if request.method == "POST":
        user_type = request.form["userType"]
        if user_type == "club":
            kwargs = {
                "firstname": request.form["firstname"],
                "lastname": request.form["lastname"],
                "email": request.form["email"],
                "password": request.form["password"],
                "clubname": request.form["clubname"],
                "position": request.form["position"],
                "phonenumber": request.form["phonenumber"],
                "usertype": 1,
            }

            user_query = """
            INSERT INTO Users(first_name, last_name, email, password, user_type)
            VALUES(%(firstname)s,%(lastname)s,%(email)s,%(password)s,%(usertype)s)
            RETURNING first_name, last_name, email, password, user_type;
            """

            club_query = """
            INSERT INTO Club (club_name, email)
            SELECT *
            FROM (VALUES(%(clubname)s, %(email)s))
            AS new_club(club_name, email)
            WHERE NOT EXISTS (SELECT 1
                              FROM Club
                              WHERE club_name = %(clubname)s)
            RETURNING club_name, email;
            """

            member_query = """
            WITH new_user AS (
                SELECT user_id
                FROM Users
                WHERE email = %(email)s
            )

            INSERT INTO Members (user_id, title, club_name, phone_number)
            SELECT user_id, %(position)s, %(clubname)s, %(phonenumber)s
            FROM new_user
            RETURNING user_id, title, club_name, phone_number;
            """

            register_user_result = sqlQuery(user_query, kwargs)
            register_club_result = sqlQuery(club_query, kwargs)
            register_member_result = sqlQuery(member_query, kwargs)

            return redirect(url_for("homepage", user=session["user"]))
        else:
            kwargs = {
                "firstname": request.form["firstname"],
                "lastname": request.form["lastname"],
                "email": request.form["email"],
                "password": request.form["password"],
                "usertype": 0,
            }

            user_query = """
            INSERT INTO Users(first_name, last_name, email, password, user_type)
            VALUES(%(firstname)s,%(lastname)s,%(email)s,%(password)s,%(usertype)s)
            RETURNING first_name, last_name, email, password, user_type;
            """

            register_user_result = sqlQuery(user_query, kwargs)

            return redirect(url_for("homepage", user=session["user"]))

    return render_template("clubReg.html")


if __name__ != "__main__":
    application = app
