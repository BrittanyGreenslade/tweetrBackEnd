from flask import Response, request
from datetime import date


def check_user_id(request):
    # .get returns none if key not provided
    # but this doesn't allow for the key being spelled wrong/keyError
    # problem here b/c need 'none' and !=none for select
    # this will be an error that the client deals with when the're not getting the right return
    user_id = request.args.get('userId')
    if user_id != None:
        user_id = int(user_id)
    return user_id


def birthdate_validity(birthdate):
    if birthdate != None:
        birthdate = date.fromisoformat(birthdate)
        if birthdate >= date.fromisoformat("1900-01-01") or birthdate <= date.today():
            result = Response("Invalid birthdate input",
                              mimetype='text/plain', status=400)
    return result
