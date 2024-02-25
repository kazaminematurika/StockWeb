from datetime import date

import SQL
from sqlalchemy.sql import text


def getStockInfo(StocKName):
    StockInfoArray = []
    engine = SQL.create_mysql_connection()
    query = text("select * from companyabbreviation where a_share_abbreviation = :stock_name")
    result = engine.execute(query, stock_name=StocKName).fetchall()

    for row in result:
        # 处理每行数据
        for value in row:
            # 格式化 date 类型数据为 'YYYY-MM-DD' 字符串
            if isinstance(value, date):
                value = value.strftime('%Y-%m-%d')
                # 处理 BLOB 类型数据，假设它是 UTF-8 编码的文本
            elif isinstance(value, bytes):
                try:
                    # 尝试使用 UTF-8 解码
                    value = value.decode('utf-8')
                except UnicodeDecodeError:
                    # 如果解码失败，保留原始二进制数据或采取其他措施
                    value = str(value)
            StockInfoArray.append(value)

    return StockInfoArray


