from flask import Response, request
from datetime import date
import dbhelpers
# select user_id for post tweet and post tweet like
import string
import random


def get_user_id(login_token):
    user_id = dbhelpers.run_select_statement(
        "SELECT user_id FROM user_session WHERE login_token = ?", [login_token])
    if len(user_id) != 0:
        user_id = int(user_id[0][0])
    else:
        user_id = None
    return user_id
# check if user_id exists (get only)


def check_user_id(request):
    # .get returns none if key not provided
    # but this doesn't allow for the key being spelled wrong/keyError
    # problem here b/c need 'none' and !=none for select
    # this will be an error that the client deals with when the're not getting the right return
    user_id = request.args.get('userId')
    if user_id != None:
        user_id = int(user_id)
    return user_id
# check if tweet_id exists(get only)


def createSalt():
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters_and_digits) for i in range(10))
    return result_str


def check_tweet_id(request):
    tweet_id = request.args.get('tweetId')
    if tweet_id != None:
        tweet_id = int(tweet_id)
    return tweet_id

# check if comment_id exists(get only)


def check_comment_id(request):
    comment_id = request.args.get('commentId')
    if comment_id != None:
        comment_id = int(comment_id)
    return comment_id

# how to force format of birthdate?


def birthdate_validity(birthdate):
    # if birthdate != None:
    birthdate = date.fromisoformat(birthdate)
    if birthdate <= date.fromisoformat("1900-01-01") or birthdate >= date.today():
        result = Response("Invalid birthdate input",
                          mimetype='text/plain', status=400)
    else:
        result = birthdate
    return result
