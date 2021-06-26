import traceback
import dbhelpers
from flask import Response
import json
import helpers

# still working on this


def get_tweet_likes(request):
    try:
        tweet_id = helpers.check_tweet_id(request)
    except ValueError:
        traceback.print_exc()
        return Response("Please enter a valid user ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
    if tweet_id != None and tweet_id != "":
        tweets_like_info = dbhelpers.run_select_statement(
            "SELECT t.user_id, u.username FROM tweets t INNER JOIN users u ON u.id = t.user_id WHERE t.id = ?", [tweet_id])
    else:
        tweets_like_info = dbhelpers.run_select_statement(
            "SELECT t.user_id, u.username FROM tweets t INNER JOIN users u ON u.id = t.user_id", [])
    tweet_likes_dictionaries = []
    if type(tweets_like_info) == Response:
        return tweets_like_info
    tweet_likes_json = None
    if len(tweets_like_info) != 0:
        for tweet_like_info in tweets_like_info:
            tweet_likes_dictionaries.append(
                {"tweetId": tweet_id, "userId": tweet_like_info[1], "username": tweet_like_info[2]})
            tweet_likes_json = json.dumps(
                tweet_likes_dictionaries, default=str)
    else:
        return Response("No user data available", mimetype='text/plain', status=400)
    if tweet_likes_json != None:
        return Response(tweet_likes_json, mimetype='application/json', status=200)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)

# still working on this


def like_tweet(request):
    try:
        login_token = request.json['loginToken']
        tweet_id = request.json['tweetId']
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    # TODO make sure can only like if tweet exists?
    user_id = helpers.get_user_id(login_token)
    if user_id != None:
        last_row_id = dbhelpers.run_insert_statement(
            "INSERT INTO tweet_likes(user_id, tweet_id) VALUES(?, ?)", [user_id, tweet_id])
        if type(last_row_id) == Response:
            return last_row_id
        if last_row_id != None:
            return Response("Post created!", mimetype='text/plain', status=201)
        else:
            return Response("Error creating post", mimetype='text/plain', status=401)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
# still working on this


def unlike_tweet(request):
    try:
        login_token = request.json['loginToken']
        tweet_id = request.json['tweetId']
    except:
        traceback.print_exc()
    rows = dbhelpers.run_delete_statement(
        "DELETE tl FROM tweet_likes tl INNER JOIN user_session us ON tl.user_id = us.user_id WHERE tl.tweet_id = ? AND us.login_token = ?", [tweet_id, login_token])
    if rows == 1:
        return Response("Tweet deleted!", mimetype='text/plain', status=200)
    else:
        return Response("Please try again", mimetype='text/plain', status=500)
