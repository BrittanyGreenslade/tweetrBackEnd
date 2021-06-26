from flask import Response
import dbhelpers
import traceback
import json


def get_follows(request):
    try:
        user_id = request.json['userId']
    except ValueError:
        traceback.print_exc()
        return Response("Invalid user ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=422)
    if user_id != None and user_id != "":
        follows = dbhelpers.run_select_statement(
            "SELECT u.email, u.username, u.bio, u.birthdate, u.image_url FROM user_follows uf INNER JOIN users u ON uf.user_id = u.id WHERE uf.user_id = ?", [user_id])
    else:
        follows = dbhelpers.run_select_statement(
            "SELECT u.email, u.username, u.bio, u.birthdate, u.image_url FROM user_follows uf INNER JOIN users u ON uf.user_id = u.id", [])
    if type(follows) == Response:
        return follows
    follows_dictionaries = []
    follows_json = None
    if len(follows) != 0:
        for follow in follows:
            follows_dictionaries.append({"userId": user_id, "email": follow[0], "username": follow[1], "bio": follow[2],
                                         "birthdate": follow[3], "imageUrl": follow[4]})
        follows_json = json.dumps(follows_dictionaries, default=str)
    else:
        return Response("Follow data unavailable", mimetype='text/plain', status=400)
    if follows_json != None:
        return Response(follows_json, mimetype='application/json', status=200)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)


def follow_user(request):
    try:
        login_token = request.json['loginToken']
        follow_id = request.json['followId']
    except ValueError:
        traceback.print_exc()
        return Response("Invalid follow ID", mimetype='text/plain', status=422)
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    user_id = dbhelpers.run_select_statement(
        "SELECT user_id FROM user_session WHERE login_token = ?", [login_token])
    if type(user_id) == Response:
        return user_id
    if len(user_id) != 0:
        user_id = int(user_id[0][0])
        last_row_id = dbhelpers.run_insert_statement(
            "INSERT INTO user_follows(user_id, follow_id) VALUES(?, ?)", [user_id, follow_id])
        if last_row_id != None:
            return Response("Follow success!", mimetype='text/plain', status=201)
        else:
            return Response("Error following user", mimetype='text/plain', status=401)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)


def unfollow_user(request):
    try:
        login_token = request.json['loginToken']
        follow_id = request.json['followId']
    except ValueError:
        traceback.print_exc()
        return Response("Invalid follow ID", mimetype='text/plain', status=422)
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
    rows = dbhelpers.run_delete_statement(
        "DELETE uf FROM user_follows uf INNER JOIN user_session us ON uf.user_id = us.user_id WHERE uf.follow_id = ? AND us.login_token = ?", [follow_id, login_token])
    if type(rows) == Response:
        return rows
    if rows == 1:
        return Response("Unfollow success!", mimetype='text/plain', status=200)
    else:
        return Response("Please try again", mimetype='text/plain', status=500)


def get_followers(request):
    try:
        user_id = request.json['userId']
    except ValueError:
        traceback.print_exc()
        return Response("Invalid user ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=422)
    if user_id != None and user_id != "":
        followers = dbhelpers.run_select_statement(
            "SELECT u.email, u.username, u.bio, u.birthdate, u.image_url FROM user_follows uf INNER JOIN users u ON uf.user_id = u.id WHERE uf.follow_id = ?", [user_id])
    if type(followers) == Response:
        return followers
    followers_dictionaries = []
    followers_json = None
    if len(followers) != 0:
        for follower in followers:
            followers_dictionaries.append({"userId": user_id, "email": follower[0], "username": follower[1], "bio": follower[2],
                                           "birthdate": follower[3], "imageUrl": follower[4]})
        followers_json = json.dumps(followers_dictionaries, default=str)
    else:
        return Response("Follow data unavailable", mimetype='text/plain', status=400)
    if followers_json != None:
        return Response(followers_json, mimetype='application/json', status=200)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)
