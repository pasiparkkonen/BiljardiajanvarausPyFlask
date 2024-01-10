from applicationfiles import custom_error, views, app
import pymysql, pymysql.cursors, os

#connection = None
# Get SSL certification file
ssl_file = os.getenv("AZURE_MYSQL_SSL_CA_FILE")
app.config['AZURE_MYSQL_SSL_CA_FILE'] = ssl_file

# Database connection
def connect_to_database(dbhost, dbuser, dbpassword, database):
    global connection
    # Try to connect to database
    try:
        # Local development connection
        #connection = pymysql.connect(host=dbhost, user=dbuser, password=dbpassword, db=database)
        # Azure SSL certificated connection
        connection = pymysql.connect(user=dbuser, password=dbpassword, host=dbhost, db=database, ssl={'ca':ssl_file})
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