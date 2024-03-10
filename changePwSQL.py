import SQL
from sqlalchemy.sql import text

engine = SQL.create_mysql_connection()


def change_is_null(oldpassword, newpassword, renewpassword):
    if (oldpassword == '' or newpassword == '' or renewpassword == ''):
        return True
    else:
        return False


def oldPassword(username, oldpassword):
    query = text("select * from usertable where username = :user_name and password = :pass_word")
    result = engine.execute(query, user_name=username, pass_word=oldpassword).fetchall()
    if (len(result) == 0):
        return False
    else:
        return True

def rePassword(newPassword, renewPassword, username):
    if(newPassword != renewPassword):
        return False
    else:
        with engine.connect() as connection:
            with connection.begin():
                query = text("update usertable set password = :new_password"
                             " where username = :user_name")
                connection.execute(query, new_password=newPassword, user_name=username)
        return True
