from flask import Response
import dbhelpers
import traceback
import json
import helpers
# done


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
    elif comments == None or comments == "":
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)
    elif len(comments) == 0 and tweet_id != None or tweet_id != "":
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)
    else:
        comment_dictionaries = []
        for comment in comments:
            comment_dictionaries.append({"tweetId": comment[5], "userId": comment[0], "commentId": comment[4], "username": comment[1], "content": comment[2],
                                         "createdAt": comment[3]})
        comment_json = json.dumps(comment_dictionaries, default=str)
        return Response(comment_json, mimetype='application/json', status=200)


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
        if type(last_row_id) == Response:
            return last_row_id
        elif last_row_id != None:
            new_comment = dbhelpers.run_select_statement(
                "SELECT c.id, c.tweet_id, c. user_id, c.username, c.content, c.created_at FROM comments c WHERE c.id = ?", [last_row_id])
        if type(new_comment) == Response:
            return new_comment
        elif new_comment != None and len(new_comment) == 1:
            new_comment_dictionary = {"commentId": new_comment[0][0], "tweetId": new_comment[0][1],
                                      "userId": new_comment[0][2], "username": new_comment[0][3], "content": [0][4], "createdAt": [0][5]}
            new_comment_json = json.dumps(
                new_comment_dictionary, default=str)
            return Response(new_comment_json, mimetype='application/json', status=201)
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
        traceback.print_exc()
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    rows = dbhelpers.run_update_statement(
        "UPDATE comments c INNER JOIN user_session us ON us.user_id = c.user_id SET c.content = ? WHERE c.id = ? AND us.login_token = ?", [content, comment_id, login_token])
    if type(rows) == Response:
        return rows
    if rows != None and rows == 1:
        updated_row = dbhelpers.run_select_statement(
            "SELECT c.tweet_id, c.user_id, u.username, c.created_at FROM comments c INNER JOIN users u ON u.id = c.user_id INNER JOIN user_session us ON c.user_id = us.user_id WHERE us.login_token = ? and c.id = ?", [login_token, comment_id])
        print(updated_row)
        # do json here
        updated_comment_dictionary = {"commentId": comment_id, "tweetId": updated_row[0][0], "userId": [
            0][1], "username": [0][2], "content": content, "createdAt": [0][3]}
        updated_comment_json = json.dumps(
            updated_comment_dictionary, default=str)
        return Response(updated_comment_json, mimetype='application/json', status=201)
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
        traceback.print_exc()
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
    rows = dbhelpers.run_delete_statement(
        "DELETE c FROM comments c INNER JOIN user_session us ON c.user_id = us.user_id WHERE c.id = ? AND us.login_token = ?", [comment_id, login_token])
    if type(rows) == Response:
        return rows
    elif rows != None and rows == 1:
        return Response("Comment deleted!", mimetype='text/plain', status=200)
    else:
        return Response("Please try again", mimetype='text/plain', status=500)
