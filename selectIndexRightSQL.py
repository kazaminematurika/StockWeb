from sqlalchemy.sql import text
import SQL

def get_stock_Industry():
    engine = SQL.create_mysql_connection()
    query = text("SELECT Industry, COUNT(stockId) FROM stockinfo GROUP BY Industry ORDER BY COUNT(stockId) DESC LIMIT 12")
    result = engine.execute(query)  # 执行查询

    industries = []  # 存储行业名称
    counts = []  # 存储股票计数

    for row in result:
        industries.append(row[0])  # 将行业名称添加到数组
        counts.append(row[1])  # 将股票计数添加到数组

    top12cupancy = round((sum(counts) / 300) * 100, 2)

    return industries, counts, top12cupancy # 返回两个数组

def marketvalue():
    engine = SQL.create_mysql_connection()
    query = text("select type, stockcount from marketvaluetype")
    result = engine.execute(query)
    markvuluetype = []
    typecount = []

    for row in result:
        markvuluetype.append(row[0])
        typecount.append(row[1])

    return markvuluetype, typecount

