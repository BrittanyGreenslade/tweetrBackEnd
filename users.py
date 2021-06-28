import hashlib
from flask import Response
import dbhelpers
import traceback
import json
import helpers
import hashlib
# import mariadb
# from datetime import date


def get_users(request):
    try:
        user_id = helpers.check_user_id(request)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid user ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=422)
    if user_id != None and user_id != "":
        # uses user_id provided above
        users = dbhelpers.run_select_statement(
            "SELECT email, username, bio, birthdate, image_url AS imageUrl FROM users WHERE id = ?", [user_id, ])
    else:
        users = dbhelpers.run_select_statement(
            "SELECT email, username, bio, birthdate, image_url AS imageUrl FROM users", [])
    user_dictionaries = []
    user_json = None
    # if there's any error in dbhelpers, it will be returned here
    if type(users) == Response:
        return users
    if len(users) != 0:
        for user in users:
            user_dictionaries.append({"userId": user_id, "email": user[0], "username": user[1],
                                      "bio": user[2], "birthdate": user[3], "imageUrl": user[4]})
            user_json = json.dumps(user_dictionaries, default=str)
    else:
        return Response("No user data available", mimetype='text/plain', status=400)
    if user_json != None:
        return Response(user_json, mimetype='application/json', status=200)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)


def create_user(request):
    birthdate = None
    # if username/email exists already - this will be a db error in dbhelpers
    try:
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        salt = helpers.createSalt()
        password = salt+password
        password = hashlib.sha512(password.encode()).hexdigest()
        bio = request.json['bio']
        birthdate = request.json['birthdate']
        birthdate = helpers.birthdate_validity(birthdate)
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
    user = None
    last_row_id = dbhelpers.run_insert_statement(sql, params)
    # insert statement in dbhelpers returns none so this works
#  str(type(created_user_id)) != "<class 'flask.wrappers.Response'>"
# isinstance takes 2 args - thing to check, type to check against (maybe broken)
    if type(last_row_id) == Response:
        return last_row_id
    if last_row_id != None:
        # login.user_login()
        # TODO a login here too
        user = dbhelpers.run_select_statement(
            "SELECT id, email, username, bio, birthdate, image_url FROM users WHERE id = ?", [last_row_id, ])
        if user != None:
            new_user_dictionary = {
                "userId": user[0][0], "email": user[0][1], "username": user[0][2], "bio": user[0][3], "birthdate": user[0][4], "imageUrl": user[0][5]}
            new_user_json = json.dumps(new_user_dictionary, default=str)
            return Response(new_user_json, mimetype='application/json', status=201)
        else:
            return Response("Sorry, something went wrong", mimetype='text/plain', status=500)
    else:
        return Response("User cannot be created. Please try again", mimetype='text/plain', status=500)


def update_user(request):
    try:
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        bio = request.json.get('bio')
        birthdate = request.json.get('birthdate')
        birthdate = helpers.birthdate_validity(birthdate)
        if type(birthdate) == Response:
            return birthdate
        login_token = request.json['loginToken']
        image_url = request.json.get('imageUrl')
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Please try again", mimetype='text/plain', status=400)

    else:
        if email == None and username == None and password == None and bio == None and birthdate == None and image_url == None:
            return Response("Please enter the required data", mimetype='text/plain', status=400)
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
            sql = sql[:-1]
            params.append(login_token)
            sql += " WHERE login_token = ?"
            rows = dbhelpers.run_update_statement(sql, params)
            if type(rows) == Response:
                return rows
            if rows == 1:
                return Response("User information updated!", mimetype='text/plain', status=200)
            else:
                return Response("Error updating data", mimetype='text/plain', status=500)


def delete_user(request):
    try:
        password = request.json['password']
        login_token = request.json['loginToken']
    except KeyError:
        return Response("Please enter the required data", mimetype='application/json', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=401)

    rows = dbhelpers.run_delete_statement(
        "DELETE u, us FROM users u INNER JOIN user_session us ON u.id = us.user_id WHERE us.login_token = ? AND u.password = ?", [login_token, password])
    if type(rows) == Response:
        return rows
    if rows == 1:
        return Response("User deleted!", mimetype='text/plain', status=200)
    else:
        return Response("Please try again", mimetype='text/plain', status=500)
