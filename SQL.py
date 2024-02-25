from sqlalchemy import create_engine

def create_mysql_connection():
    """
    创建并返回一个 SQLAlchemy 引擎，用于连接 MySQL 数据库。

    参数:
    username (str): 数据库用户名
    password (str): 数据库密码
    host (str): 数据库服务器的主机名或 IP 地址
    port (str or int): 数据库服务器的端口号
    database (str): 要连接的数据库名
    """
    username = 'root'
    password = '12345678'
    host = 'localhost'
    port = 3306
    database = 'stockdatabase'

    # 构造连接字符串
    connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"

    # 创建引擎
    engine = create_engine(connection_string)

    return engine
