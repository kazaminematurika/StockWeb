import SQL
from sqlalchemy.sql import text

def SelectStockNameTitle(StockId):
    engine = SQL.create_mysql_connection()
    query = text("select StockName from stockinfo where StockId =:stock_Id")
    with engine.connect() as connection:
        result = connection.execute(query, stock_Id=StockId)
        StockName = result.scalar()

    return StockName


def select1923StockDayData(StockId):
    closeValue = []
    date = []
    engine = SQL.create_mysql_connection()
    query = text("select StockDate, close from stockdayandpepb where StockId like :stock_Id")
    result = engine.execute(query, stock_Id=f'%{StockId}').fetchall()

    for row in result:
        # 将日期添加到 date 数组
        date.append(str(row[0]))

        closeValue.append(float(row[1]))

    return date, closeValue


def select2024StockDayData(StockId):
    closeValue2024 = []
    date = []
    engine = SQL.create_mysql_connection()
    query = text("select StockDate, close from stockday2024 where StockId =:stock_Id")
    result = engine.execute(query, stock_Id=StockId).fetchall()

    for row in result:
        # 将日期添加到 date 数组
        date.append(str(row[0]))

        closeValue2024.append(float(row[1]))

    return date, closeValue2024


def selectStockforecast(StockId):
    closeValueforecast = []
    engine = SQL.create_mysql_connection()
    query = text("select close from stockforecast where StockId =:stock_Id")
    result = engine.execute(query, stock_Id=StockId).fetchall()

    for row in result:
        closeValueforecast.append(float(row[0]))

    return closeValueforecast


def selectStockforecastAge(StockId):
    closeValueage = []
    engine = SQL.create_mysql_connection()
    query = text("select close from stockforecastAge where StockId =:stock_Id")
    result = engine.execute(query, stock_Id=StockId).fetchall()

    for row in result:
        closeValueage.append(float(row[0]))

    return closeValueage
