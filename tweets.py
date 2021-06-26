from flask import Response
import dbhelpers
import traceback
import json
import helpers


def get_tweets(request):
    try:
        user_id = helpers.check_user_id(request)
    except ValueError:
        traceback.print_exc()
        return Response("Please enter a valid user ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=422)
    if user_id != None and user_id != "":
        tweets = dbhelpers.run_select_statement(
            "SELECT t.id, u.username, t.content, t.created_at, t.image_url, u.image_url FROM tweets t INNER JOIN users u ON t.user_id = u.id WHERE t.user_id = ?", [user_id])
    else:
        tweets = dbhelpers.run_select_statement(
            "SELECT t.id, u.username, t.content, t.created_at, t.image_url, u.image_url FROM tweets t INNER JOIN users u ON t.user_id = u.id", [])
    if type(tweets) == Response:
        return tweets
    tweet_dictionaries = []
    tweet_json = None
    if len(tweets) != 0:
        for tweet in tweets:
            tweet_dictionaries.append({"userId": user_id, "tweetId": tweet[0], "username": tweet[1], "content": tweet[2],
                                      "createdAt": tweet[3], "tweetImageUrl": tweet[4], "userImageUrl": tweet[5]})
        tweet_json = json.dumps(tweet_dictionaries, default=str)
    else:
        return Response("Post data unavailable", mimetype='text/plain', status=400)
    if tweet_json != None:
        return Response(tweet_json, mimetype='application/json', status=200)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)


def post_tweet(request):
    try:
        login_token = request.json['loginToken']
        content = request.json['content']
        image_url = request.json.get('imageUrl')
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    user_id = dbhelpers.run_select_statement(
        "SELECT user_id FROM user_session WHERE login_token = ?", [login_token])
        #TODO add in if dbhelpers returns a response
    if len(user_id) != 0:
        user_id = int(user_id[0][0])
        sql = "INSERT INTO tweets(user_id, content"
        params = [user_id, content]
        if image_url != None:
            sql += ", image_url) VALUES(?, ?, ?)"
            params.append(image_url)
        else:
            sql += ") VALUES(?, ?)"
        sql += " WHERE user_id = ?"
        params.append(user_id)
        last_row_id = dbhelpers.run_insert_statement(sql, params)
        if last_row_id != None:
            return Response("Post created!", mimetype='text/plain', status=201)
        else:
            return Response("Error creating post", mimetype='text/plain', status=401)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)


def edit_tweet(request):
    try:
        login_token = request.json['loginToken']
        content = request.json['content']
        image_url = request.json.get('imageUrl')
        tweet_id = request.json['tweetId']
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    sql = "UPDATE tweets t INNER JOIN user_session us ON us.user_id = t.user_id SET t.content = ?"
    params = [content]
    if image_url != None:
        sql += ", t.image_url = ?"
        params.append(image_url)
    sql += " WHERE t.id = ? and login_token = ?"
    params.append(tweet_id)
    params.append(login_token)
    rows = dbhelpers.run_update_statement(sql, params)
    if rows == 1:
        return Response("Post updated!", mimetype='text/plain', status=200)
    else:
        return Response("Error updating post", mimetype='text/plain', status=500)


def delete_tweet(request):
    try:
        login_token = request.json['loginToken']
        tweet_id = request.json['tweetId']
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
    rows = dbhelpers.run_delete_statement(
        "DELETE t FROM tweets t INNER JOIN user_session us ON t.user_id = us.user_id WHERE t.id = ? AND us.login_token = ?", [tweet_id, login_token])
    if rows == 1:
        return Response("Tweet deleted!", mimetype='text/plain', status=200)
    else:
        return Response("Please try again", mimetype='text/plain', status=500)
