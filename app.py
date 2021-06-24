from flask import Flask, request
# import dbhelpers
# import json
import sys
import users
import login
import tweets
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


# @app.get("/api/follows")
# @app.post("/api/follows")
# @app.delete("/api/follows")

# @app.get("/api/followers")

@app.get("/api/tweets")
def get_tweets():
    return tweets.get_tweets(request)


@app.post("/api/tweets")
def post_tweet():
    return tweets.post_tweet(request)


@app.patch("/api/tweets")
def edit_tweet():
    return tweets.edit_tweet(request)
# @app.delete("/api/tweets")

# @app.get("/api/tweet-likes")
# @app.post("/api/tweet-likes")
# @app.delete("/api/tweet-likes")

# @app.get("/api/comments")
# @app.post("/api/comments")
# @app.patch("/api/comments")
# @app.delete("/api/comments")

# @app.get("/api/comment-likes")
# @app.post("/api/comment-likes")
# @app.delete("/api/comment-likes")


if(len(sys.argv) > 1):
    mode = sys.argv[1]
else:
    print("No mode argument, please pass a mode argument when invoking the file")
    exit()

if(mode == "production"):
    import bjoern  # type: ignore
    bjoern.run(app, "0.0.0.0", 5015)
elif(mode == "testing"):
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)
else:
    print("Invalid mode, please select either 'production' or 'testing'")
    exit()
