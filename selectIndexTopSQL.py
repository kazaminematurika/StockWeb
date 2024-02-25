from sqlalchemy.sql import text
import SQL


def count_shsz_stock():
    """
    对以 'sh.' 开头的 stockId 进行计数，并返回结果数组。

    参数:
    engine: SQLAlchemy 数据库引擎对象
    """
    # SQL 查询
    engine = SQL.create_mysql_connection()
    query = text("SELECT COUNT(*) FROM csi300indexinfo WHERE stockId LIKE 'sh.%'")

    # 执行查询
    with engine.connect() as connection:
        result = connection.execute(query)

        # 提取结果
        sh_count = result.scalar()
        sh_percentage = round((sh_count / 300) * 100, 2)
        sz_count = 300-sh_count
        sz_percentage = 100-sh_percentage
    # 返回结果
    return sh_count, sh_percentage, sz_count, sz_percentage

def Totalmarketcapitalization():
    engine = SQL.create_mysql_connection()
    query = text("select sum(Totalmarketcapitalization) from stockinfo")
    with engine.connect() as connection:
        result = connection.execute(query)
        pitalization = result.scalar()
        newPitalization = round((pitalization / 100000000), 2)

    return newPitalization






