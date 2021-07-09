from flask import Response
from werkzeug.datastructures import Headers
import dbhelpers
import traceback
import json
import helpers


def get_tweets(request):
    try:
        user_id = helpers.check_user_id(request)
    except ValueError:
        return Response("Invalid user ID", mimetype='text/plain', status=422)
    except:
        traceback.print_exc()
        return Response("Something went wrong, please try again", mimetype='text/plain', status=422)
    if user_id != None and user_id != "":
        tweets = dbhelpers.run_select_statement(
            "SELECT t.id, u.username, t.content, t.created_at, t.image_url, u.image_url, t.user_id FROM tweets t INNER JOIN users u ON t.user_id = u.id WHERE t.user_id = ? ORDER BY t.created_at DESC", [user_id, ])
    else:
        tweets = dbhelpers.run_select_statement(
            "SELECT t.id, u.username, t.content, t.created_at, t.image_url, u.image_url, t.user_id FROM tweets t INNER JOIN users u ON t.user_id = u.id ORDER BY t.created_at DESC", [])
    if type(tweets) == Response:
        return tweets
    elif tweets == None or tweets == "":
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)
    else:
        tweet_dictionaries = []
        for tweet in tweets:
            tweet_dictionaries.append({"userId": tweet[6], "tweetId": tweet[0], "username": tweet[1], "content": tweet[2],
                                       "createdAt": tweet[3], "tweetImageUrl": tweet[4], "userImageUrl": tweet[5]})
        tweet_json = json.dumps(tweet_dictionaries, default=str)
        return Response(tweet_json, mimetype='application/json', status=200)


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
    # is actually user_id_list (careful with variable names for select)
    user_id = dbhelpers.run_select_statement(
        "SELECT user_id FROM user_session WHERE login_token = ?", [login_token, ])
    if user_id != None and len(user_id) != 0:
        user_id = int(user_id[0][0])
        sql = "INSERT INTO tweets(user_id, content"
        # these params are always sent
        params = [user_id, content]
        # img url optional
        if image_url != None:
            sql += ", image_url) VALUES(?, ?, ?)"
            params.append(image_url)
        else:
            sql += ") VALUES(?, ?)"
        last_row_id = dbhelpers.run_insert_statement(sql, params)
        if type(last_row_id) == Response:
            return last_row_id
        # insert statement either will return none or response
        elif last_row_id != None:
            new_tweet = dbhelpers.run_select_statement(
                "SELECT t.user_id, u.username, t.created_at, t.image_url, t.id, t.content FROM tweets t INNER JOIN users u ON u.id = t.user_id INNER JOIN user_session us ON us.user_id = t.user_id WHERE us.login_token = ? AND t.id = ?", [login_token, last_row_id])
            if type(new_tweet) == Response:
                return new_tweet
            if new_tweet != None and len(new_tweet) == 1:
                tweet_dictionary = {"tweetId": new_tweet[0][4], "userId": new_tweet[0][0], "username": new_tweet[0][1],
                                    "content": new_tweet[0][5], "createdAt": new_tweet[0][2], "imageUrl": new_tweet[0][3]}
                tweet_json = json.dumps(tweet_dictionary, default=str)
                return Response(tweet_json, mimetype='application/json', status=201)
            else:
                return Response("Error fetching data", mimetype='text/plain', status=500)
        else:
            return Response("Error creating post", mimetype='text/plain', status=401)
    else:
        return Response("User not logged in", mimetype='text/plain', status=400)


def edit_tweet(request):
    try:
        login_token = request.json['loginToken']
        content = request.json['content']
        image_url = request.json.get('imageUrl')
        tweet_id = int(request.json['tweetId'])
    except ValueError:
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
    elif rows != None and rows == 1:
        if image_url != None:
            updated_tweet_dictionary = {
                "tweetId": tweet_id, "content": content, "imageUrl": image_url}
            udpated_tweet_json = json.dumps(
                updated_tweet_dictionary, default=str)
            return Response(udpated_tweet_json, mimetype='application/json', status=200)
        else:
            updated_tweet_dictionary = {
                "tweetId": tweet_id, "content": content}
            udpated_tweet_json = json.dumps(
                updated_tweet_dictionary, default=str)
            return Response(udpated_tweet_json, mimetype='application/json', status=200)
    else:
        return Response("Error updating post", mimetype='text/plain', status=500)


def delete_tweet(request):
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
    rows = dbhelpers.run_delete_statement(
        "DELETE t FROM tweets t INNER JOIN user_session us ON t.user_id = us.user_id WHERE t.id = ? AND us.login_token = ?", [tweet_id, login_token])
    if type(rows) == Response:
        return rows
    elif rows != None and rows == 1:
        return Response("Tweet deleted!", mimetype='text/plain', status=200)
    else:
        return Response("Please try again", mimetype='text/plain', status=500)


def following_tweets(request):
    try:
        # has to be request.headers or it'll show up in the url
        # send headers instead in axr
        login_token = request.headers['loginToken']
    except KeyError:
        return Response("Please enter the required data", mimetype='text/plain', status=401)
    except:
        traceback.print_exc()
        return Response("Sorry, something went wrong", mimetype='text/plain', status=400)
    following_tweets = dbhelpers.run_select_statement(
        "SELECT t.id, u.username, t.content, t.created_at, t.image_url, u.image_url, t.user_id FROM user_follows uf INNER JOIN user_session us ON us.user_id = uf.user_id INNER JOIN tweets t ON t.user_id = uf.follow_id INNER JOIN users u ON u.id = t.user_id WHERE us.login_token = ? ORDER BY t.created_at DESC LIMIT 100", [login_token])
    if type(following_tweets) == Response:
        return following_tweets
    elif following_tweets == None or following_tweets == "":
        return Response("Sorry, something went wrong", mimetype='text/plain', status=500)
    else:
        tweet_dictionaries = []
        for tweet in following_tweets:
            tweet_dictionaries.append({"userId": tweet[6], "tweetId": tweet[0], "username": tweet[1], "content": tweet[2],
                                       "createdAt": tweet[3], "tweetImageUrl": tweet[4], "userImageUrl": tweet[5]})
        tweet_json = json.dumps(tweet_dictionaries, default=str)
        return Response(tweet_json, mimetype='application/json', status=200)
