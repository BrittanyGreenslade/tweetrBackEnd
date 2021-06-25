# Woah so DRY! More helpers to keep my API endpoint code clean and free of repeated code.
# Don't forget to create your own dbcreds.py file!
import mariadb
import dbcreds
import traceback
# https://thepythonguru.com/handling-errors/

# dberror/operational/internal


def get_db_connection():
    # Create our connection to the DB and return it
    try:
        return mariadb.connect(user=dbcreds.user, password=dbcreds.password,
                               host=dbcreds.host, port=dbcreds.port, database=dbcreds.database)
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Operational Error")
        return None
    except mariadb.InternalError:
        traceback.print_exc()
        print("Internal Error")
        return None
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Database Error")
        return None
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Programming Error")
        return None
    except:
        print("Error connecting to DB!")
        traceback.print_exc()
        return None


def get_db_cursor(conn):
    # Get the cursor of the connection we have created
    try:
        return conn.cursor()
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Operational Error")
        return None
    except mariadb.InternalError:
        traceback.print_exc()
        print("Internal Error")
        return None
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Programming Error")
        return None
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Database Error")
        return None
    except:
        print("Error creating cursor on DB!")
        traceback.print_exc()
        return None


def close_db_cursor(cursor):
    # Close the passed in cursor
    if(cursor == None):
        # This means cursor is closed
        return True
    try:
        cursor.close()
        return True
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Operational Error")
        return False
    except mariadb.InternalError:
        traceback.print_exc()
        print("Internal Error")
        return False
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Programming Error")
        return False
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Database Error")
        return False
    except:
        print("Error closing cursor on DB!")
        traceback.print_exc()
        return False


def close_db_connection(conn):
    # Close the passed in connection
    if(conn == None):
        return True
    try:
        conn.close()
        return True
    except mariadb.OperationalError:
        traceback.print_exc()
        print("Operational Error")
        return False
    except mariadb.InternalError:
        traceback.print_exc()
        print("Internal Error")
        return False
    except mariadb.DatabaseError:
        traceback.print_exc()
        print("Database Error")
        return False
    except mariadb.ProgrammingError:
        traceback.print_exc()
        print("Programming Error")
        return False
    except:
        print("Error closing connection to DB!")
        traceback.print_exc()
        return False
