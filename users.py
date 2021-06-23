from flask import Response
import dbhelpers
import traceback
import json


def get_users(request):
    try:
        user_id = int(request.args['userId'])
    except ValueError:
        traceback.print_exc()
        return Response("Please enter a valid user ID", mimetype='text/plain', status=400)
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
    # for if the image url isn't input, if statements still work
    # image_url = None
    try:
        email = request.json['email']
        username = request.json['username']
        password = request.json['password']
        bio = request.json['bio']
        # limit birthdate input format?
        birthdate = request.json['birthdate']
        image_url = request.json.get('imageUrl')
    except:
        traceback.print_exc()
        return Response("Please enter the required data", mimetype='text/plain', status=400)

    sql = "INSERT INTO users (email, username, password, bio, birthdate"
    params = []
    if image_url != None and image_url != "":
        sql += ", image_url) VALUES (?, ?, ?, ?, ?, ?)"
        params.append(email)
        params.append(username)
        params.append(password)
        params.append(bio)
        params.append(birthdate)
        params.append(image_url)
    else:
        sql += ") VALUES (?, ?, ?, ?, ?)"
        params.append(email)
        params.append(username)
        params.append(password)
        params.append(bio)
        params.append(birthdate)
    created_user_id = -1
    user = None
    created_user_id = dbhelpers.run_insert_statement(sql, params)
    if created_user_id != -1 and created_user_id != None:
        # TODO a login here too
        user = dbhelpers.run_select_statement(
            "SELECT id, email, username, bio, birthdate, image_url FROM users WHERE id = ?", [created_user_id])
        if user != None:
            new_user_dictionary = {
                "userId": user[0][0], "email": user[0][1], "username": user[0][2], "bio": user[0][3], "birthdate": user[0][4], "imageUrl": user[0][5]}
            new_user_json = json.dumps(new_user_dictionary, default=str)
            return Response(new_user_json, mimetype='application/json', status=201)
        else:
            return Response("Something went wrong, sorry", mimetype='text/plain', status=500)
    else:
        return Response("User cannot be created. Please try again", mimetype='text/plain', status=500)


def update_user(request):
    login_token = None
    try:
        email = request.json.get('email')
        username = request.json.get('username')
        password = request.json.get('password')
        bio = request.json.get('bio')
        birthdate = request.json.get('birthdate')
        login_token = request.json['loginToken']
        image_url = request.json.get('imageUrl')
    except:
        traceback.print_exc()
        return Response("Please try again", mimetype='application/json', status=400)
    if login_token == None or login_token == "":
        return Response("Please update at least one field", mimetype='text/plain', status=400)
    else:
        # maybe need to add image url
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
            if rows == 1:
                return Response("User information updated!", mimetype='text/plain', status=200)
            else:
                return Response("Error updating data", mimetype='text/plain', status=500)


def delete_user(request):
    try:
        password = request.json['password']
        login_token = request.json['loginToken']
    except:
        traceback.print_exc()
        return Response("Please enter the required data", mimetype='application/json', status=401)
    rows = dbhelpers.run_delete_statement(
        "DELETE u, us FROM users u INNER JOIN user_session us ON u.id = us.user_id WHERE us.login_token = ? AND u.password = ?", [login_token, password])
    if rows == 1:
        return Response("User deleted!", mimetype='text/plain', status=200)
    else:
        return Response("Please try again", mimetype='text/plain', status=500)
