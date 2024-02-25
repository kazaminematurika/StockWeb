import SQL
from sqlalchemy.sql import text


def get2019StockNameAndShare(StockId):
    ShareName = []
    Nature = []
    StockNumber = []
    Proportion = []
    OutStanding = []
    ChangeStock = []

    engine = SQL.create_mysql_connection()

    query = text(f"select * from 2019Top10 "
                 "where StockId = :stock_id "
                 " order by Top asc ;")
    result = engine.execute(query, stock_id=StockId)

    for row in result:
        ShareName.append(str(row[1]))

        Nature.append(str(row[2]))

        StockNumber.append(int(row[4]))

        Proportion.append(float(row[5]))

        OutStanding.append(str(row[6]))

        ChangeStock.append(str(row[7]) if row[7] is not None else None)

    SumProportion = round(sum(Proportion), 3)

    return ShareName, Nature, StockNumber, Proportion, OutStanding, ChangeStock, SumProportion


def get2020StockNameAndShare(StockId):
    ShareName = []
    Nature = []
    StockNumber = []
    Proportion = []
    OutStanding = []
    ChangeStock = []

    engine = SQL.create_mysql_connection()

    query = text(f"select * from 2020Top10 "
                 "where StockId = :stock_id "
                 " order by Top asc ;")
    result = engine.execute(query, stock_id=StockId)

    for row in result:
        ShareName.append(str(row[1]))

        Nature.append(str(row[2]))

        StockNumber.append(int(row[4]))

        Proportion.append(float(row[5]))

        OutStanding.append(str(row[6]))

        ChangeStock.append(str(row[7]) if row[7] is not None else None)

    SumProportion = round(sum(Proportion), 3)

    return ShareName, Nature, StockNumber, Proportion, OutStanding, ChangeStock, SumProportion


def get2021StockNameAndShare(StockId):
    ShareName = []
    Nature = []
    StockNumber = []
    Proportion = []
    OutStanding = []
    ChangeStock = []

    engine = SQL.create_mysql_connection()

    query = text(f"select * from 2021Top10 "
                 "where StockId = :stock_id "
                 " order by Top asc ;")
    result = engine.execute(query, stock_id=StockId)

    for row in result:
        ShareName.append(str(row[1]))

        Nature.append(str(row[2]))

        StockNumber.append(int(row[4]))

        Proportion.append(float(row[5]))

        OutStanding.append(str(row[6]))

        ChangeStock.append(str(row[7]) if row[7] is not None else None)

    SumProportion = round(sum(Proportion), 3)

    return ShareName, Nature, StockNumber, Proportion, OutStanding, ChangeStock, SumProportion

def get2022StockNameAndShare(StockId):
    ShareName = []
    Nature = []
    StockNumber = []
    Proportion = []
    OutStanding = []
    ChangeStock = []

    engine = SQL.create_mysql_connection()

    query = text(f"select * from 2022Top10 "
                 "where StockId = :stock_id "
                 " order by Top asc ;")
    result = engine.execute(query, stock_id=StockId)

    for row in result:
        ShareName.append(str(row[1]))

        Nature.append(str(row[2]))

        StockNumber.append(int(row[4]))

        Proportion.append(float(row[5]))

        OutStanding.append(str(row[6]))

        ChangeStock.append(str(row[7]) if row[7] is not None else None)

    SumProportion = round(sum(Proportion), 3)

    return ShareName, Nature, StockNumber, Proportion, OutStanding, ChangeStock, SumProportion


def get2023StockNameAndShare(StockId):
    ShareName = []
    Nature = []
    StockNumber = []
    Proportion = []
    OutStanding = []
    ChangeStock = []

    engine = SQL.create_mysql_connection()

    query = text(f"select * from 2023Top10 "
                 "where StockId = :stock_id "
                 " order by Top asc ;")
    result = engine.execute(query, stock_id=StockId)

    for row in result:
        ShareName.append(str(row[1]))

        Nature.append(str(row[2]))

        StockNumber.append(int(row[4]))

        Proportion.append(float(row[5]))

        OutStanding.append(str(row[6]))

        ChangeStock.append(str(row[7]) if row[7] is not None else None)

    SumProportion = round(sum(Proportion), 3)

    return ShareName, Nature, StockNumber, Proportion, OutStanding, ChangeStock, SumProportion


def getStockShareName(StockId):
    engine = SQL.create_mysql_connection()
    query = text("select StockName from stockinfo where StockId = :stock_id")

    with engine.connect() as connection:
        getStockName = connection.execute(query, stock_id=StockId)
        getStockNameValue = getStockName.scalar()

    return getStockNameValue






