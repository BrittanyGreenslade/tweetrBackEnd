from typing import Type, ValuesView
from flask import Response
import dbhelpers
import traceback
import json
import secrets


def user_login(request):
    try:
        email = request.json['email']
        password = request.json['password']
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    login_id = -1
    try:
        user = dbhelpers.run_select_statement(
            "SELECT u.id, u.username, u.bio, u.birthdate, u.image_url FROM users u WHERE u.password = ? and u.email = ?", [password, email])
        # print(user)
        if len(user) == 1:
            user_id = int(user[0][0])
            login_token = secrets.token_urlsafe(60)
            login_id = dbhelpers.run_insert_statement(
                "INSERT INTO user_session (login_token, user_id) VALUES(?, ?)", [login_token, user_id])
    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=500)
    if login_id != -1:
        login_dictionary = {"loginToken": login_token,
                            "userId": user_id, "email": email, "username": user[0][1], "bio": user[0][2], "birthdate": user[0][3], "imageUrl": user[0][4]}
        login_json = json.dumps(login_dictionary, default=str)
        return Response(login_json, mimetype='application/json', status=201)
    else:
        return Response("Invalid login - please try again", mimetype='text/plain', status=400)


def user_logout(request):
    try:
        login_token = request.json['loginToken']
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    rows = dbhelpers.run_delete_statement(
        "DELETE us FROM user_session us WHERE us.login_token = ?", [login_token])
    if rows == 1:
        return Response("Logout success", mimetype='text/plain', status=200)
    else:
        return Response("Logout failed, please try again", mimetype='application/json', status=500)
