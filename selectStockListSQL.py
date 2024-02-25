import SQL
from sqlalchemy.sql import text


def selectStcokListData():
    StockID = []
    StockName = []
    StockIndustry = []
    StockTotalmarketcapitalization = []

    engine = SQL.create_mysql_connection()
    query = text("select * from stockinfo")
    result = engine.execute(query).fetchall()

    for row in result:
        StockID.append(str(row[0]))

        StockName.append([str(row[1])])

        StockIndustry.append(str((row[2])))

        StockTotalmarketcapitalization.append(round(float(row[3])/100000000, 3))

    return StockID, StockName, StockIndustry, StockTotalmarketcapitalization