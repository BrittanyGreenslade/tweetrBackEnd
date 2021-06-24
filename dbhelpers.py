# Woah so DRY! Look at this, helper functions that can help you run DB queries
import dbconnect
import traceback
from flask import Response, request
import json
import mariadb
# The same comments apply to all the helper functions in here!
# except:
#     do exceptions for db here
# https://mariadb-corporation.github.io/mariadb-connector-python/module.html#exceptions


def run_select_statement(sql, params):
    # Do the normal open and variable setup
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None
    # Try to run the command based on the SQL and params passed in
    try:
        cursor.execute(sql, params)
        result = cursor.fetchall()
    # TODO Do a better job of catching more specific errors! Might need to find a way to return error-specific results
    # integrity error can't happen here?
    # except mariadb.IntegrityError:
    #     traceback.print_exc()
    #     result = Response("Unsuccessful - please try again",
    #                       mimetype='text/plain', status=400)
    except mariadb.ProgrammingError:
        traceback.print_exc()
        # if there's an error in SQL statement
        result = Response("Database error", mimetype='text/plain', status=500)
    except:
        traceback.print_exc()

        print("DO BETTER ERROR CATCHING")

    # Close the resources
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # Return the result
    return result


def run_insert_statement(sql, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None
    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.lastrowid
    except mariadb.IntegrityError:
        traceback.print_exc()
        result = Response("Duplicate entry!",
                          mimetype='text/plain', status=400)
    except:
        traceback.print_exc()
        print("DO BETTER ERROR CATCHING")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    return result


def run_delete_statement(sql, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.rowcount
    except:
        traceback.print_exc()
        print("DO BETTER ERROR CATCHING")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    return result


def run_update_statement(sql, params):
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    result = None

    try:
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.rowcount
    except:
        traceback.print_exc()
        print("DO BETTER ERROR CATCHING")

    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    return result
