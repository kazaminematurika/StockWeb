import SQL
from sqlalchemy.sql import text


def selectcsi300():
    closeValue = []
    date = []
    engine = SQL.create_mysql_connection()
    query = text("select CSIDate, close from csi300indexday")
    result = engine.execute(query).fetchall()

    for row in result:
        # 将日期添加到 date 数组
        date.append(str(row[0]))

        closeValue.append(float(row[1]))

    return date, closeValue


def select2024csi300():
    closeValue2024 = []
    date = []
    engine = SQL.create_mysql_connection()
    query = text("select CSIDate, close from csi300indexday2024")
    result = engine.execute(query).fetchall()

    for row in result:
        # 将日期添加到 date 数组
        date.append(str(row[0]))

        closeValue2024.append(float(row[1]))

    return date, closeValue2024


def selectcsi300forecast():
    closeValueforecast = []
    engine = SQL.create_mysql_connection()
    query = text("select close from csi300forecast")
    result = engine.execute(query).fetchall()

    for row in result:
        closeValueforecast.append(float(row[0]))

    return closeValueforecast


def selectcsi300forecastAge():
    closeValueage = []
    engine = SQL.create_mysql_connection()
    query = text("select close from csi300forecastage")
    result = engine.execute(query).fetchall()

    for row in result:
        closeValueage.append(float(row[0]))

    return closeValueage