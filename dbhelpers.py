# Woah so DRY! Look at this, helper functions that can help you run DB queries
import dbconnect
import traceback
from flask import Response
# import json
import mariadb
# The same comments apply to all the helper functions in here!


def run_select_statement(sql, params):
    cursor = None
    conn = None
    # Do the normal open and variable setup
    # check that the connection worked
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    if conn != None or cursor != None:
        result = None
        # Try to run the command based on the SQL and params passed in
        try:
            cursor.execute(sql, params)
            result = cursor.fetchall()
        # if there's an error in SQL statement
        except mariadb.ProgrammingError:
            traceback.print_exc()
            result = Response("Programming error",
                              mimetype='text/plain', status=500)
        except mariadb.OperationalError:
            result = Response("Operational error",
                              mimetype='text/plain', status=500)
        except mariadb.InternalError:
            result = Response("Internal server error",
                              mimetype='text/plain', status=500)
        except:
            result = Response("Something went wrong, please try again",
                              mimetype='text/plain', status=500)
        # Close the resources
        dbconnect.close_db_cursor(cursor)
        dbconnect.close_db_connection(conn)
    else:
        result = Response("Connection error",
                          mimetype='text/plain', status=500)
    # Return the result
    return result


def run_insert_statement(sql, params):
    cursor = None
    conn = None
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    if conn != None or cursor != None:
        result = None
        try:
            cursor.execute(sql, params)
            conn.commit()
            result = cursor.lastrowid
        except mariadb.IntegrityError:
            traceback.print_exc()
            result = Response("Invalid entry!",
                              mimetype='text/plain', status=400)
        except mariadb.DataError:
            traceback.print_exc()
            result = Response("Input maximum reached",
                              mimetype='text/plain', status=400)
        # if there's an error in SQL statement
        except mariadb.ProgrammingError:
            traceback.print_exc()
            result = Response("Database error",
                              mimetype='text/plain', status=500)
        except mariadb.OperationalError:
            result = Response("Operational error",
                              mimetype='text/plain', status=500)
        except mariadb.InternalError:
            result = Response("Internal server error",
                              mimetype='text/plain', status=500)
        except:
            traceback.print_exc()
            result = Response("Something went wrong, please try again",
                              mimetype='text/plain', status=500)
        dbconnect.close_db_cursor(cursor)
        dbconnect.close_db_connection(conn)
    else:
        result = Response("Connection error",
                          mimetype='text/plain', status=500)
    return result


def run_delete_statement(sql, params):
    cursor = None
    conn = None
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    if conn != None or cursor != None:
        result = None
        try:
            cursor.execute(sql, params)
            conn.commit()
            result = cursor.rowcount
        except mariadb.DataError:
            traceback.print_exc()
            result = Response("Input limit maximum reached",
                              mimetype='text/plain', status=400)
        # if there's an error in SQL statement
        except mariadb.ProgrammingError:
            traceback.print_exc()
            result = Response("Database error",
                              mimetype='text/plain', status=500)
        except mariadb.OperationalError:
            result = Response("Operational error",
                              mimetype='text/plain', status=500)
        except mariadb.InternalError:
            result = Response("Internal server error",
                              mimetype='text/plain', status=500)
        except:
            traceback.print_exc()
            result = Response("Something went wrong, please try again",
                              mimetype='text/plain', status=500)
        dbconnect.close_db_cursor(cursor)
        dbconnect.close_db_connection(conn)
    else:
        result = Response("Connection error",
                          mimetype='text/plain', status=500)
    return result


def run_update_statement(sql, params):
    cursor = None
    conn = None
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    if conn != None or cursor != None:
        result = None

        try:
            cursor.execute(sql, params)
            conn.commit()
            result = cursor.rowcount
        except mariadb.IntegrityError:
            traceback.print_exc()
            result = Response("Invalid entry!",
                              mimetype='text/plain', status=400)
        except mariadb.DataError:
            traceback.print_exc()
            result = Response("Input limit maximum reached",
                              mimetype='text/plain', status=400)
        # if there's an error in SQL statement
        except mariadb.ProgrammingError:
            traceback.print_exc()
            result = Response("Programming error",
                              mimetype='text/plain', status=500)
        # if something happens to connection
        except mariadb.OperationalError:
            result = Response("Operational error",
                              mimetype='text/plain', status=500)
        # if stg happens to cursor
        except mariadb.InternalError:
            result = Response("Internal server error",
                              mimetype='text/plain', status=500)
        except:
            traceback.print_exc()
            result = Response("Something went wrong, please try again",
                              mimetype='text/plain', status=500)

        dbconnect.close_db_cursor(cursor)
        dbconnect.close_db_connection(conn)
    else:
        result = Response("Connection error",
                          mimetype='text/plain', status=500)
    return result
