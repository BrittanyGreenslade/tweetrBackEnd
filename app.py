from flask import Flask, request, Response
import dbhelpers
import json
import sys
import users
app = Flask(__name__)


@app.get("/api/users")
def get_users():
    return users.get_users(request)
    # print(user_json)


@app.post("/api/users")
def new_user():
    return users.create_user(request)


@app.patch("/api/users")
def update_user():
    return users.update_user(request)


@app.delete("/api/users")
def delete_user():
    return users.delete_user(request)

# @app.post("/api/login")
# @app.delete("/api/login")


# @app.get("/api/follows")
# @app.post("/api/follows")
# @app.delete("/api/follows")

# @app.get("/api/followers")

# @app.get("/api/tweets")
# @app.post("/api/tweets")
# @app.patch("/api/tweets")
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
