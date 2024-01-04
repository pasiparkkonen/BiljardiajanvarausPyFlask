from applicationfiles import custom_error, views
import pymysql, pymysql.cursors

#connection = None

# Database connection
def connect_to_database(dbhost, dbuser, dbpassword, database):
    global connection
    # Try to connect to database
    try:
        connection = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, db=database)
        return connection
    except pymysql.Error as error:
        error_message = f"Database connection error: {error}"
        custom_error.handle_error(error_message)
        return None
    finally:
        error_message = None

def close_connection():
    global connection
    if connection is not None:
        connection.close()