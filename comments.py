from flask import Response
import dbhelpers
import traceback
import json
import helpers


def get_comments(request):
    try:
        tweet_id = helpers.check_tweet_id(request)
    except ValueError:
        traceback.print_exc()
        return Response("Invalid tweet ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=422)
    if tweet_id != None and tweet_id != "":
        comments = dbhelpers.run_select_statement(
            "SELECT c.user_id, u.username, c.content, c.created_at, c.id, c.tweet_id FROM comments c INNER JOIN users u ON c.user_id = u.id WHERE c.tweet_id = ?", [tweet_id, ])
    else:
        comments = dbhelpers.run_select_statement(
            "SELECT c.user_id, u.username, c.content, c.created_at, c.id, c.tweet_id FROM comments c INNER JOIN users u ON c.user_id = u.id", [])
    if type(comments) == Response:
        return comments
    elif len(comments) >= 0 and comments != None:
        comment_dictionaries = []
        for comment in comments:
            comment_dictionaries.append({"tweetId": comment[5], "userId": comment[0], "commentId": comment[4], "username": comment[1], "content": comment[2],
                                         "createdAt": comment[3]})
        comment_json = json.dumps(comment_dictionaries, default=str)
        return Response(comment_json, mimetype='application/json', status=200)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)


def post_comment(request):
    try:
        login_token = request.json['loginToken']
        content = request.json['content']
        tweet_id = int(request.json['tweetId'])
    except ValueError:
        traceback.print_exc()
        return Response("Invalid tweet ID", mimetype='text/plain', status=422)
    except KeyError:
        traceback.print_exc()
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    user_id = dbhelpers.run_select_statement(
        "SELECT user_id FROM user_session WHERE login_token = ?", [login_token, ])
    if len(user_id) != 0 and user_id != None:
        user_id = int(user_id[0][0])
        last_row_id = dbhelpers.run_insert_statement(
            "INSERT INTO comments(user_id, content, tweet_id) VALUES(?, ?, ?)", [user_id, content, tweet_id])
        print(last_row_id)
        if type(last_row_id) == Response:
            return last_row_id
        if last_row_id != None:
            # do json here (check in other if json = None)
            return Response("Comment created!", mimetype='text/plain', status=201)
        else:
            return Response("Error creating comment", mimetype='text/plain', status=401)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)


def edit_comment(request):
    try:
        login_token = request.json['loginToken']
        content = request.json['content']
        comment_id = int(request.json['commentId'])
    except ValueError:
        traceback.print_exc()
        return Response("Invalid comment ID", mimetype='text/plain', status=422)
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    rows = dbhelpers.run_update_statement(
        "UPDATE comments c INNER JOIN user_session us ON us.user_id = c.user_id SET c.content = ? WHERE c.id = ? and login_token = ?", [content, comment_id, login_token])
    if type(rows) == Response:
        return rows
    if rows == 1:
        # do json here
        return Response("Comment updated!", mimetype='text/plain', status=200)
    else:
        return Response("Error updating comment", mimetype='text/plain', status=500)


def delete_comment(request):
    try:
        login_token = request.json['loginToken']
        comment_id = int(request.json['commentId'])
    except ValueError:
        traceback.print_exc()
        return Response("Invalid comment ID", mimetype='text/plain', status=422)
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
    rows = dbhelpers.run_delete_statement(
        "DELETE c FROM comments c INNER JOIN user_session us ON c.user_id = us.user_id WHERE c.id = ? AND us.login_token = ?", [comment_id, login_token])
    if type(rows) == Response:
        return rows
    if rows == 1:
        return Response("Comment deleted!", mimetype='text/plain', status=200)
    else:
        return Response("Please try again", mimetype='text/plain', status=500)
