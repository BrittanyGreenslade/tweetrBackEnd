import traceback
import dbhelpers
from flask import Response
import json
import helpers


def get_tweet_likes(request):
    try:
        tweet_id = helpers.check_tweet_id(request)
    except ValueError:
        return Response("Invalid tweet ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    if tweet_id != None and tweet_id != "":
        tweets_like_info = helpers.select_tweet_like_info(tweet_id, 'tweet_id')
    else:
        tweets_like_info = dbhelpers.run_select_statement(
            "SELECT tl.user_id, u.username, tl.tweet_id FROM tweet_likes tl INNER JOIN users u ON u.id = tl.user_id", [])
    if type(tweets_like_info) == Response:
        return tweets_like_info
    elif tweets_like_info == None or tweets_like_info == "":
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)
    else:
        tweet_likes_dictionaries = []
        for tweet_like_info in tweets_like_info:
            tweet_likes_dictionaries.append(
                {"tweetId": tweet_like_info[2], "userId": tweet_like_info[0], "username": tweet_like_info[1]})
        tweet_likes_json = json.dumps(
            tweet_likes_dictionaries, default=str)
        return Response(tweet_likes_json, mimetype='application/json', status=200)


def like_tweet(request):
    try:
        login_token = request.json['loginToken']
        tweet_id = int(request.json['tweetId'])
    except ValueError:
        return Response("Invalid tweet ID", mimetype='text/plain', status=422)
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    user_id = helpers.get_user_id(login_token)
    if user_id != None and user_id != "":
        last_row_id = dbhelpers.run_insert_statement(
            "INSERT INTO tweet_likes(user_id, tweet_id) VALUES(?, ?)", [user_id, tweet_id])
        if type(last_row_id) == Response:
            return last_row_id
        elif last_row_id != None:
            tweet_like_info = helpers.select_tweet_like_info(last_row_id, 'id')
            # tweet_like_info = dbhelpers.run_select_statement(
            #     "SELECT tl.user_id, u.username, tl.tweet_id FROM tweet_likes tl INNER JOIN users u ON tl.user_id = u.id WHERE tl.id = ?", [last_row_id])
            if type(tweet_like_info) == Response:
                return tweet_like_info
            if tweet_like_info != None and len(tweet_like_info) == 1:
                tweet_like_dictionary = {
                    "userId": tweet_like_info[0][0], "tweetId": tweet_like_info[0][2], "username": tweet_like_info[0][1]}
                tweet_like_json = json.dumps(
                    tweet_like_dictionary, default=str)
                return Response(tweet_like_json, mimetype='application/json', status=201)
        else:
            return Response("Error liking post", mimetype='text/plain', status=401)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)


def unlike_tweet(request):
    try:
        login_token = request.json['loginToken']
        tweet_id = int(request.json['tweetId'])
    except ValueError:
        return Response("Invalid tweet ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    rows = dbhelpers.run_delete_statement(
        "DELETE tl FROM tweet_likes tl INNER JOIN user_session us ON tl.user_id = us.user_id WHERE tl.tweet_id = ? AND us.login_token = ?", [tweet_id, login_token])
    if type(rows) == Response:
        return rows
    elif rows != None and rows == 1:
        return Response("Post unliked!", mimetype='text/plain', status=200)
    else:
        return Response("Error unliking post", mimetype='text/plain', status=500)
