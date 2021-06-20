from flask import Flask, request, Response
from werkzeug.wrappers import response
import dbhelpers
import traceback
import json


def get_users(request):
    try:
        user_id = int(request.args['userId'])
    except ValueError:
        traceback.print_exc()
        # if you return a response here how can you see it in app.py
        return Response("Please enter a valid user ID", mimetype='text/plain', status=400)
    # except:
    #     422 (for if 'userId' key is not named)

    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=500)
    if user_id != None or user_id != "":
        users = dbhelpers.run_select_statement(
            "SELECT id AS userId, email, username, bio, birthdate, image_url AS imageUrl FROM users WHERE id = ?", [user_id])
    else:
        users = dbhelpers.run_select_statement(
            "SELECT id AS userId, email, username, bio, birthdate, image_url AS imageUrl FROM users", [])
    user_dictionaries = []
    if len(users) != 0:
        for user in users:
            user_dictionaries.append({"userId": user[0], "email": user[1], "username": user[2],
                                      "bio": user[3], "birthdate": user[4], "imageUrl": user[5]})
        user_json = json.dumps(user_dictionaries, default=str)
    else:
        return Response("No user data available", mimetype='text/plain', status=400)
    if user_json != None:
        return Response(user_json, mimetype='application/json', status=200)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)


def create_user(request):
    try:
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        bio = request.json['bio']
        birthdate = request.json['birthdate']
        # imageUrl = request.json['imageUrl']
        # created_user_id = int(
        created_user_id = dbhelpers.run_insert_statement(
            "INSERT INTO users(email, username, password, bio, birthdate) VALUES (?, ?, ?, ?, ?)", [email, username, password, bio, birthdate])

        created_user_id = int(created_user_id)
        # do a login here too
        user = dbhelpers.run_select_statement(
            "SELECT id, email, username, birthdate FROM users WHERE id = ?", [created_user_id])
        new_user_dictionary = {
            "userId": user[0][0], "email": user[0][1], "username": user[0][2], "birthdate": user[0][3]}
        new_user_json = json.dumps(new_user_dictionary, default=str)
        # created_user = dbhelpers.run_select_statement(
        #     "SELECT u.id, u.email, u.username, u.bio, u.birthdate, us.login_token FROM users u INNER JOIN user_session us ON us.user_id = u.id WHERE u.id = ?", [created_user_id])

        return Response(new_user_json, mimetype='application/json', status=200)
        # limit birthdate input

        # username = request.json['username']
        # password = request.json['password']
        # bio = request.json['bio']
        # birthdate = request.json['birthdate']
        # imageUrl = request.json['imageUrl']
    except:
        traceback.print_exc()
        # def update_user():
    # def delete_user():
