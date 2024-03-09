import SQL
from sqlalchemy.sql import text


def add_user(username, password):
    engine = SQL.create_mysql_connection()
    # 使用 with 语句自动管理连接的生命周期
    with engine.connect() as connection:
        # 开始一个新的事务
        with connection.begin():
            query = text("INSERT INTO usertable(username, password) VALUES (:user_name, :pass_word)")
            connection.execute(query, user_name=username, pass_word=password)
        # 事务会在 with 代码块结束时自动提交

    # 连接会在 with 代码块结束时自动关闭
