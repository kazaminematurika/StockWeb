from sqlalchemy.sql import text
import SQL

engine = SQL.create_mysql_connection()

def selectUserStockId(username):
    if username != '游客':
        UserstockId = []
        query = text("select userStockId from userstocklist where username = :user_name")
        result = engine.execute(query, user_name=username).fetchall()

        for row in result:
            UserstockId.append(row[0])

        return UserstockId


def addUserStockList(username, StockId, StockName, Industry, Totalmarket):
    with engine.connect() as connection:
        with connection.begin():
            query = text("insert into userstocklist (username, userStockId, userStockName, userStockIndustry, userStockTotalmarket) VALUES"
                         "(:user_name, :stock_id, :stock_name, :in_dustry, :total_market)")
            connection.execute(query, user_name=username, stock_id=StockId, stock_name=StockName,
                               in_dustry=Industry, total_market=Totalmarket)


def selectUserAllStock(username):
    if username != '游客':
        StockId = []
        StockName = []
        Industry = []
        Totalmarket = []
        query = text("select * from userstocklist where username = :user_name")
        result = engine.execute(query, user_name=username).fetchall()

        for row in result:
            StockId.append(row[1])
            StockName.append(row[2])
            Industry.append(row[3])
            Totalmarket.append(row[4])

        return StockId, StockName, Industry, Totalmarket


def delUserStock(username, StockId):
    if username != '游客':
        with engine.connect() as connection:
            with connection.begin():
                qurey = text("delete from userstocklist where username = :user_name"
                             " and userStockId = :user_StockId")
                connection.execute(qurey, user_name=username, user_StockId=StockId)