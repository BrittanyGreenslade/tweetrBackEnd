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
        return Response("Invalid user ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=422)
    if user_id != None and user_id != "":
        tweets = dbhelpers.run_select_statement(
            "SELECT t.id, u.username, t.content, t.created_at, t.image_url, u.image_url FROM tweets t INNER JOIN users u ON t.user_id = u.id WHERE t.user_id = ?", [user_id, ])
    else:
        tweets = dbhelpers.run_select_statement(
            "SELECT t.id, u.username, t.content, t.created_at, t.image_url, u.image_url FROM tweets t INNER JOIN users u ON t.user_id = u.id", [])
    if type(tweets) == Response:
        return tweets
    tweet_dictionaries = []
    tweet_json = None
    # if len(tweets) != 0:
    for tweet in tweets:
        tweet_dictionaries.append({"userId": user_id, "tweetId": tweet[0], "username": tweet[1], "content": tweet[2],
                                   "createdAt": tweet[3], "tweetImageUrl": tweet[4], "userImageUrl": tweet[5]})
    tweet_json = json.dumps(tweet_dictionaries, default=str)
    # else:
    #     return Response("Post data unavailable", mimetype='text/plain', status=400)
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
        "SELECT user_id FROM user_session WHERE login_token = ?", [login_token, ])
    if len(user_id) != 0:
        user_id = int(user_id[0][0])
        sql = "INSERT INTO tweets(user_id, content"
        params = [user_id, content]
        if image_url != None:
            sql += ", image_url) VALUES(?, ?, ?)"
            params.append(image_url)
        else:
            sql += ") VALUES(?, ?)"
        last_row_id = None
        last_row_id = dbhelpers.run_insert_statement(sql, params)
        if type(last_row_id) == Response:
            return last_row_id
        tweet_dictionary = {}
        tweet_json = None
        if last_row_id != None:
            new_tweet = dbhelpers.run_select_statement(
                "SELECT t.id, t.user_id, t.username, t.content, t.created_at, t.image_url FROM tweets t INNER JOIN user_session us ON us.user_id = t.user_id WHERE us.login_token = ?", [login_token, ])
            if new_tweet != None:
                tweet_dictionary = {"tweetId": new_tweet[0][0], "userId": new_tweet[0][1], "username": new_tweet[0]
                                    [2], "content": new_tweet[0][3], "createdAt": new_tweet[0][4], "imageUrl": new_tweet[0][5]}
                tweet_json = json.dumps(tweet_dictionary, default=str)
            return Response(tweet_json, mimetype='application/json', status=201)
        else:
            return Response("Error creating post", mimetype='text/plain', status=401)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)


def edit_tweet(request):
    try:
        login_token = request.json['loginToken']
        content = request.json['content']
        image_url = request.json.get('imageUrl')
        tweet_id = int(request.json['tweetId'])
    except ValueError:
        traceback.print_exc()
        return Response("Invalid tweet ID", mimetype='text/plain', status=422)
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
    if type(rows) == Response:
        return rows
    updated_tweet_dictionary = {}
    updated_tweet_json = None
    if rows == 1:
        updated_tweet_dictionary = {"tweetId": tweet_id, "content": content}
        udpated_tweet_json = json.dumps(updated_tweet_dictionary, default=str)
        return Response(udpated_tweet_json, mimetype='application/json', status=200)
    else:
        return Response("Error updating post", mimetype='text/plain', status=500)


def delete_tweet(request):
    try:
        login_token = request.json['loginToken']
        tweet_id = int(request.json['tweetId'])
    except ValueError:
        traceback.print_exc()
        return Response("Invalid tweet ID", mimetype='text/plain', status=422)
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
    rows = dbhelpers.run_delete_statement(
        "DELETE t FROM tweets t INNER JOIN user_session us ON t.user_id = us.user_id WHERE t.id = ? AND us.login_token = ?", [tweet_id, login_token])
    if type(rows) == Response:
        return rows
    if rows == 1:
        return Response("Tweet deleted!", mimetype='text/plain', status=200)
    else:
        return Response("Please try again", mimetype='text/plain', status=500)
