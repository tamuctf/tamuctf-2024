import sqlite3
from sqlite3 import Error
import time

# Connect to db
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


# execute sql statement
def sql(conn, command):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(command)
    except Error as e:
        print(e)

# read query
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")


def main():
    database = "important.db"
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        username text NOT NULL,
                                        password text NOT NULL,
                                        email text,
                                        favorite_cereal text,
                                        creation_date integer
                                    ); """
    
    x = int(time.time())

    sql_create_user1 = """INSERT INTO users (id, username, password, email, favorite_cereal, creation_date) VALUES 
                                    (0, 'admin', 'gigem{{c3r3aL_t0o_sWe3t_t0d2y}}', 'admin@admin.com', 'Frosted Flakes', {0});
                                    """.format(x)

    sql_create_user2 = """INSERT INTO users (id, username, password, email, favorite_cereal, creation_date) VALUES 
                                    (1, 'guest', 'password', 'guest@guest.com', 'Cinnamon Toast Crunch', {0}); 
                                    """.format(x)

    q1 = """
        SELECT *
        FROM users;
    """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create users table
        sql(conn, sql_create_users_table)
        conn.commit()

        # create user guest
        sql(conn, sql_create_user1)
        conn.commit()

        # create user admin
        sql(conn, sql_create_user2)
        conn.commit()

        # query users table
        results = read_query(conn, q1)
        for result in results:
            print(result)

        conn.close()
        print("Success!")
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()
