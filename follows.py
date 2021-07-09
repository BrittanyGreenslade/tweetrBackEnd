from flask import Response
import dbhelpers
import traceback
import json
import helpers


def get_follows(request, id_one, id_two):
    try:
        user_id = int(request.args['userId'])
    except KeyError:
        # if user id isn't input
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except ValueError:
        # if user id input isn't a number
        return Response("Invalid user ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=422)
    # follows
    # formatted string that will take in 3 arguments (incl. follow id and user id), and depending
    # which is passed first, will determine whether we get followers or following users.
    # if user id is first arg, follow id second, means we're getting followers
    # if follow id is first arg (i.e what users is joined on), user id second, means we're getting following
    follows = helpers.select_follows(
        user_id, 'u.id', id_one, id_two)
    if type(follows) == Response:
        return follows
    if follows == None and follows == "":
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)
    else:
        follows_dictionaries = []
        for follow in follows:
            follows_dictionaries.append({"userId": follow[5], "email": follow[0], "username": follow[1], "bio": follow[2],
                                         "birthdate": follow[3], "imageUrl": follow[4]})
        follows_json = json.dumps(follows_dictionaries, default=str)
        return Response(follows_json, mimetype='application/json', status=200)


def follow_user(request):
    try:
        login_token = request.json['loginToken']
        follow_id = int(request.json['followId'])
    except ValueError:
        return Response("Invalid follow ID", mimetype='text/plain', status=422)
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    user_id = helpers.get_user_id(login_token)
    if len(user_id) != 0:
        user_id = int(user_id[0][0])
        last_row_id = dbhelpers.run_insert_statement(
            "INSERT INTO user_follows(user_id, follow_id) VALUES(?, ?)", [user_id, follow_id])
        if type(last_row_id) == Response:
            return last_row_id
        if last_row_id != None:
            new_follow = helpers.select_follows(
                last_row_id, 'follow_id', 'follow_id', 'id')
            # new_follow = dbhelpers.run_select_statement(
            #     "SELECT u.email, u.username, u.bio, u.birthdate, u.image_url, uf.follow_id FROM user_follows uf INNER JOIN users u ON u.id = uf.follow_id WHERE uf.id = ?", [last_row_id])
            if type(new_follow) == Response:
                return new_follow
            if new_follow != None and len(new_follow) == 1:
                follow_dictionary = {"userId": new_follow[0][5], "username": new_follow[0][1], "email": new_follow[0][0],
                                     "bio": new_follow[0][2], "birthdate": new_follow[0][3], "imageUrl": new_follow[0][4]}
                follow_json = json.dumps(follow_dictionary, default=str)
                return Response(follow_json, mimetype='application/json', status=201)
        else:
            return Response("Error following user", mimetype='text/plain', status=401)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)


def unfollow_user(request):
    try:
        login_token = request.json['loginToken']
        follow_id = int(request.json['followId'])
    except ValueError:
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
