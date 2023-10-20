from flask import Flask, request
# import dbhelpers
# import json
import sys
import users
import login
import tweets
import tweetLikes
import comments
import commentLikes
import follows
app = Flask(__name__)

# users calls


@app.get("/api/users")
def get_users():
    return users.get_users(request)


@app.post("/api/users")
def create_user():
    return users.create_user(request)


@app.patch("/api/users")
def update_user():
    return users.update_user(request)


@app.delete("/api/users")
def delete_user():
    return users.delete_user(request)
# login calls


@app.post("/api/login")
def user_login():
    return login.user_login(request)


@app.delete("/api/login")
def user_logout():
    return login.user_logout(request)


@app.get("/api/tweets")
def get_tweets():
    return tweets.get_tweets(request)


@app.post("/api/tweets")
def post_tweet():
    return tweets.post_tweet(request)


@app.patch("/api/tweets")
def edit_tweet():
    return tweets.edit_tweet(request)


@app.get("/api/following-tweets")
def following_tweets():
    return tweets.following_tweets(request)


@app.delete("/api/tweets")
def delete_tweet():
    return tweets.delete_tweet(request)


@app.get("/api/tweet-likes")
def get_tweet_likes():
    return tweetLikes.get_tweet_likes(request)


@app.post("/api/tweet-likes")
def like_tweet():
    return tweetLikes.like_tweet(request)


@app.delete("/api/tweet-likes")
def unliked_tweet():
    return tweetLikes.unlike_tweet(request)


@app.get("/api/comments")
def get_comments():
    return comments.get_comments(request)


@app.post("/api/comments")
def post_comment():
    return comments.post_comment(request)


@app.patch("/api/comments")
def edit_comment():
    return comments.edit_comment(request)


@app.delete("/api/comments")
def delete_comment():
    return comments.delete_comment(request)


@app.get("/api/comment-likes")
def get_comment_likes():
    return commentLikes.get_comment_likes(request)


@app.post("/api/comment-likes")
def like_comment():
    return commentLikes.like_comment(request)


@app.delete("/api/comment-likes")
def unlike_comment():
    return commentLikes.unlike_comment(request)


@app.get("/api/follows")
def get_following():
    # sends the string 'follow_id' and 'user_id' to be used in the SQL statements
    # NGL I borrowed this idea from Ramona's code that they showed during class (but made sense of it first)
    return follows.get_follows(request, 'follow_id', 'user_id')


@app.get("/api/followers")
def get_followers():
    # sends the string 'follow_id' and 'user_id' to be used in the SQL statements
    return follows.get_follows(request, 'user_id', 'follow_id')


@app.post("/api/follows")
def follow_user():
    return follows.follow_user(request)


@app.delete("/api/follows")
def unfollow_user():
    return follows.unfollow_user(request)


if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

if(mode == "production"):
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5018)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()
