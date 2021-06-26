import traceback
import dbhelpers
from flask import Response
import json
import helpers


def get_comment_likes(request):
    try:
        comment_id = helpers.check_comment_id(request)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid user ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    if comment_id != None and comment_id != "":
        comments_like_info = dbhelpers.run_select_statement(
            "SELECT c.user_id, u.username FROM comments c INNER JOIN users u ON u.id = c.user_id WHERE c.id = ?", [comment_id])
    else:
        comments_like_info = dbhelpers.run_select_statement(
            "SELECT c.user_id, u.username FROM comments c INNER JOIN users u ON u.id = c.user_id", [])
    comment_likes_dictionaries = []
    if type(comments_like_info) == Response:
        return comments_like_info
    comment_likes_json = None
    if len(comments_like_info) != 0:
        for comment_like_info in comments_like_info:
            comment_likes_dictionaries.append(
                {"tweetId": comment_id, "userId": comment_like_info[0], "username": comment_like_info[1]})
            comment_likes_json = json.dumps(
                comment_like_info, default=str)
    else:
        return Response("No user data available", mimetype='text/plain', status=400)
    if comment_likes_json != None:
        return Response(comment_likes_json, mimetype='application/json', status=200)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)


def like_comment(request):
    try:
        login_token = request.json['loginToken']
        comment_id = request.json['commentId']
    except ValueError:
        traceback.print_exc()
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
        if last_row_id != None:
            return Response("Comment liked!", mimetype='text/plain', status=201)
        else:
            return Response("Error liking comment", mimetype='text/plain', status=401)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)


def unlike_comment(request):
    try:
        login_token = request.json['loginToken']
        comment_id = request.json['commentId']
    except ValueError:
        traceback.print_exc()
        return Response("Invalid comment ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    rows = dbhelpers.run_delete_statement(
        "DELETE tl FROM comment_likes cl INNER JOIN user_session us ON cl.user_id = us.user_id WHERE cl.comment_id = ? AND us.login_token = ?", [comment_id, login_token])
    if type(rows) == Response:
        return rows
    if rows == 1:
        return Response("Comment unliked!", mimetype='text/plain', status=200)
    else:
        return Response("Error unliking comment", mimetype='text/plain', status=500)
