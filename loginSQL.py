import SQL
from sqlalchemy.sql import text

engine = SQL.create_mysql_connection()


def is_null(username, password):
    if (username == '' or password == ''):
        return True
    else:
        return False


def is_existed(username, password):
    query = text("select * from usertable where username = :user_name and password = :pass_word")
    result = engine.execute(query, user_name=username, pass_word=password).fetchall()
    if (len(result) == 0):
        return False
    else:
        return True


def exist_user(username):
    query = text("SELECT * FROM usertable WHERE username = :user_name")
    result = engine.execute(query, user_name=username).fetchall()
    if (len(result) == 0):
        return False
    else:
        return True
