from flask import Response
import dbhelpers
import traceback
import json


def get_tweets(request):
    try:
        # .get returns none if key not provided
        user_id = request.args.get('userId')
        if user_id != None:
            user_id = int(user_id)
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
    tweet_dictionaries = []
    if len(tweets) != 0:
        for tweet in tweets:
            tweet_dictionaries.append({"userId": user_id, "tweetId": tweet[0], "username": tweet[1], "content": tweet[2],
                                      "createdAt": tweet[3], "tweetImageUrl": tweet[4], "userImageUrl": tweet[5]})
        tweet_json = json.dumps(tweet_dictionaries, default=str)
    else:
        return Response("No user data available", mimetype='text/plain', status=400)
    if tweet_json != None:
        return Response(tweet_json, mimetype='application/json', status=200)
    else:
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)
# def post_tweet():
# def edit_tweet():
# def delete_tweet():
