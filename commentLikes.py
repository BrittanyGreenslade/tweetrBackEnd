import traceback
import dbhelpers
from flask import Response
import json
import helpers
# done


def get_comment_likes(request):
    try:
        comment_id = helpers.check_comment_id(request)
    except ValueError:
        return Response("Invalid comment ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    if comment_id != None and comment_id != "":
        comments_like_info = dbhelpers.run_select_statement(
            "SELECT cl.user_id, u.username, cl.comment_id FROM comment_likes cl INNER JOIN users u ON u.id = cl.user_id WHERE cl.comment_id = ?", [comment_id, ])
    else:
        comments_like_info = dbhelpers.run_select_statement(
            "SELECT cl.user_id, u.username, cl.comment_id FROM comment_likes cl INNER JOIN users u ON u.id = cl.user_id", [])
    if type(comments_like_info) == Response:
        return comments_like_info
    elif comments_like_info == None or comments_like_info == "":
        return Response("No data available", mimetype='text/plain', status=400)
    # elif len(comments_like_info) == 0 and (comment_id != None or comment_id != ""):
    #     return Response("No data available", mimetype='text/plain', status=500)
    else:
        comment_likes_dictionaries = []
        for comment_like_info in comments_like_info:
            comment_likes_dictionaries.append(
                {"commentId": comment_like_info[2], "userId": comment_like_info[0], "username": comment_like_info[1]})
        comment_likes_json = json.dumps(
            comment_likes_dictionaries, default=str)
        return Response(comment_likes_json, mimetype='application/json', status=200)


def like_comment(request):
    try:
        login_token = request.json['loginToken']
        comment_id = int(request.json['commentId'])
    except ValueError:
        return Response("Invalid comment ID", mimetype='text/plain', status=422)
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    user_id = helpers.get_user_id(login_token)
    if user_id != None and user_id != "":
        last_row_id = dbhelpers.run_insert_statement(
            "INSERT INTO comment_likes(user_id, comment_id) VALUES(?, ?)", [user_id, comment_id])
        if type(last_row_id) == Response:
            return last_row_id
        elif last_row_id != None:
            # do json here
            return Response("Comment liked!", mimetype='text/plain', status=201)
        else:
            return Response("Error liking comment", mimetype='text/plain', status=401)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)


def unlike_comment(request):
    try:
        login_token = request.json['loginToken']
        comment_id = int(request.json['commentId'])
    except ValueError:
        return Response("Invalid comment ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    rows = dbhelpers.run_delete_statement(
        "DELETE cl FROM comment_likes cl INNER JOIN user_session us ON cl.user_id = us.user_id WHERE cl.comment_id = ? AND us.login_token = ?", [comment_id, login_token])
    if type(rows) == Response:
        return rows
    elif rows != None and rows == 1:
        return Response("Comment unliked!", mimetype='text/plain', status=200)
    else:
        return Response("Error unliking comment", mimetype='text/plain', status=500)
