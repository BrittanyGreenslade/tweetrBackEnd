import hashlib
from flask import Response
import dbhelpers
import traceback
import json
import helpers
import secrets


def get_users(request):
    try:
        user_id = helpers.check_user_id(request)
    except ValueError:
        return Response("Invalid user ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=422)
    if user_id != None and user_id != "":
        users = dbhelpers.run_select_statement(
            "SELECT email, username, bio, birthdate, image_url, id FROM users WHERE id = ?", [user_id, ])
    else:
        users = dbhelpers.run_select_statement(
            "SELECT email, username, bio, birthdate, image_url, id FROM users", [])
    # if there's any error in dbhelpers, it will be returned here
    if type(users) == Response:
        return users
    elif users == None or users == "":
        return Response("No user data available", mimetype='text/plain', status=400)
    elif len(users) == 0 and (user_id != None or user_id != ""):
        return Response("No user data available", mimetype='text/plain', status=500)
    else:
        user_dictionaries = []
        for user in users:
            user_dictionaries.append(
                {"userId": user[5], "email": user[0], "username": user[1], "bio": user[2], "birthdate": user[3], "imageUrl": user[4]})
        user_json = json.dumps(user_dictionaries, default=str)
        return Response(user_json, mimetype='application/json', status=200)


def create_user(request):
    # if username/email exists already - this will be a db error in dbhelpers
    try:
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        salt = helpers.createSalt()
        password = salt+password
        password = hashlib.sha512(password.encode()).hexdigest()
        bio = request.json['bio']
        # this requires an input so if there's none it will key error
        birthdate = request.json['birthdate']
        # otherwise it will send it to here to check it's valid
        birthdate = helpers.birthdate_validity(birthdate)
        # response is if the birthdate is out of the acceptable range or if it's ""
        if type(birthdate) == Response:
            return birthdate
        image_url = request.json.get('imageUrl')
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    sql = "INSERT INTO users (salt, email, username, password, bio, birthdate"
    params = [salt, email, username, password, bio, birthdate]
    if image_url != None and image_url != "":
        sql += ", image_url) VALUES (?, ?, ?, ?, ?, ?, ?)"
        params.append(image_url)
    else:
        sql += ") VALUES (?, ?, ?, ?, ?, ?)"
    last_row_id = dbhelpers.run_insert_statement(sql, params)
# insert statement in dbhelpers returns none so this works without pre-setting variable - b/c I return response
# this was for if a response was returned - it was an alternative to type() == Response but there was a
# bug in it? I want to leave it here for the future so I know how to use it
#  str(type(created_user_id)) != "<class 'flask.wrappers.Response'>"
# isinstance takes 2 args - thing to check, type to check against (maybe broken)
    if type(last_row_id) == Response:
        return last_row_id
    elif last_row_id != None:
        login_token = secrets.token_urlsafe(60)
        session_id = dbhelpers.run_insert_statement(
            "INSERT INTO user_session(login_token, user_id) VALUES(?, ?)", [login_token, last_row_id])
        if type(session_id) == Response:
            return session_id
        elif session_id != None:
            new_user_dictionary = {
                "userId": last_row_id, "email": email, "username": username, "bio": bio, "birthdate": birthdate, "imageUrl": image_url, "loginToken": login_token}
            new_user_json = json.dumps(new_user_dictionary, default=str)
            return Response(new_user_json, mimetype='application/json', status=201)
        else:
            return Response("Sorry, something went wrong", mimetype='text/plain', status=500)
    else:
        return Response("User cannot be created. Please try again", mimetype='text/plain', status=500)


def update_user(request):
    salt = None
    try:
        # all .get b/c optional
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        # had to create new one so it's changed in the db
        if password != None:
            salt = helpers.createSalt()
            password = salt+password
            password = hashlib.sha512(password.encode()).hexdigest()
        bio = request.json.get('bio')
        birthdate = request.json.get('birthdate')
        # bday.get is optional so if it's input, it will send it to here to check it's valid
        if birthdate != None:
            birthdate = helpers.birthdate_validity(birthdate)
        # response is if the birthdate is out of the acceptable range or if it's None/"" - then fns stops
        if type(birthdate) == Response:
            return birthdate
        # this isn't optional
        login_token = request.json['loginToken']
        image_url = request.json.get('imageUrl')
        # if required request.json isn't entered
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Please try again", mimetype='text/plain', status=400)
    # if nothing was updated - tell them to update thing
    if email == None and username == None and password == None and bio == None and birthdate == None and image_url == None:
        return Response("Please update at least one field", mimetype='text/plain', status=400)
    else:
        params = []
        sql = "UPDATE users u INNER JOIN user_session us on u.id = us.user_id SET"
        if email != None and email != "":
            sql += " u.email = ?,"
            params.append(email)
        if username != None and username != "":
            sql += " u.username = ?,"
            params.append(username)
        if password != None and password != "":
            sql += " u.password = ?,"
            params.append(password)
        if bio != None and bio != "":
            sql += " u.bio = ?,"
            params.append(bio)
        if birthdate != None and birthdate != "":
            sql += " u.birthdate = ?,"
            params.append(birthdate)
        if image_url != None and image_url != "":
            sql += " u.image_url = ?,"
            params.append(image_url)
        if salt != None and salt != "":
            sql += " u.salt = ?,"
            params.append(salt)
        # removes the last character (comma) from the SQL statement of
        # last thing concatenated
        sql = sql[:-1]
        params.append(login_token)
        sql += " WHERE login_token = ?"
        rows = dbhelpers.run_update_statement(sql, params)
        # if there's an error in the dbhelpers statement, it's returned here
        if type(rows) == Response:
            return rows
        # rows updated should only ever be 1
        elif rows == 1:
            updated_user = dbhelpers.run_select_statement(
                "SELECT u.id, u.email, u.username, u.bio, u.birthdate, u.image_url FROM users u INNER JOIN user_session us ON u.id = us.user_id WHERE login_token = ?", [login_token, ])
            if type(updated_user) == Response:
                return updated_user
            # result of select.fetchall = list of lists and length should only be 1
            elif updated_user != None and len(updated_user) == 1:
                updated_user_dictionary = {
                    "userId": updated_user[0][0], "email": updated_user[0][1], "username": updated_user[0][2], "bio": updated_user[0][3], "birthdate": updated_user[0][4], "imageUrl": updated_user[0][5]}
                updated_user_json = json.dumps(
                    updated_user_dictionary, default=str)
                return Response(updated_user_json, mimetype='application/json', status=201)
            else:
                return Response("Error fetching data. Please refresh the page", mimetype='text/plain', status=500)
        else:
            return Response("Error updating data", mimetype='text/plain', status=500)


def delete_user(request):
    try:
        login_token = request.json['loginToken']
        password = request.json['password']
        salt = dbhelpers.get_salt_delete(login_token)
        password = salt + password
        password = hashlib.sha512(password.encode()).hexdigest()
    except KeyError:
        return Response("Please enter the required data", mimetype='application/json', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=401)
    rows = dbhelpers.run_delete_statement(
        "DELETE u FROM users u INNER JOIN user_session us ON u.id = us.user_id WHERE us.login_token = ? AND u.password = ?", [login_token, password])
    if type(rows) == Response:
        return rows
    elif rows == 1:
        return Response("User deleted!", mimetype='text/plain', status=200)
    else:
        return Response("Delete error", mimetype='text/plain', status=500)
