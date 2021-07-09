from flask import Response, request
from datetime import date
import dbhelpers
import string
import random


def get_user_id(login_token):
    user_id = dbhelpers.run_select_statement(
        "SELECT user_id FROM user_session WHERE login_token = ?", [login_token])
    if user_id != None:
        user_id = int(user_id[0][0])
    return user_id

# id_one different in select for post/get users so needed it to be {}
# id_two changes in get followers vs follows (described in get follows fn)


def select_tweet_like_info(tweet_id, id_one):
    tweet_like_info = dbhelpers.run_select_statement(
        f"SELECT tl.user_id, u.username, tl.tweet_id FROM tweet_likes tl INNER JOIN users u ON tl.user_id = u.id WHERE tl.{id_one} = ?", [tweet_id, ])
    return tweet_like_info


def select_follows(user_id, id_one, id_two, id_three):
    select_follows = dbhelpers.run_select_statement(
        f"SELECT u.email, u.username, u.bio, u.birthdate, u.image_url, {id_one} FROM user_follows uf INNER JOIN users u ON uf.{id_two} = u.id WHERE uf.{id_three} = ?", [user_id, ])
    return select_follows


def select_comments(tweet_id, id_one):
    comments = dbhelpers.run_select_statement(
        f"SELECT c.user_id, u.username, c.content, c.created_at, c.id, c.tweet_id FROM comments c INNER JOIN users u ON c.user_id = u.id WHERE c.{id_one} = ?", [tweet_id, ])
    return comments


def select_comment_like_info(comment_id, id_one):
    comment_like_info = dbhelpers.run_select_statement(
        f"SELECT cl.user_id, u.username, cl.comment_id FROM comment_likes cl INNER JOIN users u ON cl.user_id = u.id WHERE cl.{id_one} = ?", [comment_id])
    return comment_like_info

# check if user_id exists (get/args only)


def check_user_id(request):
    # .get returns none if key not provided
    # but this doesn't allow for the key being spelled wrong/keyError
    # this will be an error that the client deals with when the're not getting the right return
    user_id = request.args.get('userId')
    if user_id != None:
        user_id = int(user_id)
    return user_id
# check if tweet_id exists(get/args only)


def createSalt():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters_and_digits) for i in range(10))
    return result_str


def check_tweet_id(request):
    tweet_id = request.args.get('tweetId')
    if tweet_id != None:
        tweet_id = int(tweet_id)
    return tweet_id

# check if comment_id exists(get/args only)


def check_comment_id(request):
    comment_id = request.args.get('commentId')
    if comment_id != None:
        comment_id = int(comment_id)
    return comment_id


def birthdate_validity(birthdate):
    if birthdate != "":
        birthdate = date.fromisoformat(birthdate)
        # this converts the bday input string to a number so can do math
        if birthdate <= date.fromisoformat("1900-01-01") or birthdate >= date.today():
            result = Response("Invalid birthdate input",
                              mimetype='text/plain', status=400)
        else:
            result = birthdate
    else:
        result = Response("Invalid birthdate input",
                          mimetype='text/plain', status=400)
    return result
