from sqlalchemy.sql import text
import SQL


def find_median(arr):
    # 首先对数组进行排序
    sorted_arr = sorted(arr)
    n = len(sorted_arr)

    # 如果数组长度为奇数，返回中间的元素
    if n % 2 == 1:
        return sorted_arr[n // 2]
    # 如果数组长度为偶数，返回中间两个元素的平均值
    else:
        return (sorted_arr[n // 2 - 1] + sorted_arr[n // 2]) / 2


def find_percentile(arr, percentile):
    # 首先对数组进行排序
    sorted_arr = sorted(arr)
    n = len(sorted_arr)

    # 计算分位数的位置
    index = (n - 1) * percentile / 100

    # 如果索引是整数，则直接返回对应的值
    if index.is_integer():
        return sorted_arr[int(index)]
    # 如果索引是小数，则需要进行插值
    else:
        lower_index = int(index)
        upper_index = lower_index + 1
        fraction = index - lower_index
        return sorted_arr[lower_index] + fraction * (sorted_arr[upper_index] - sorted_arr[lower_index])


def convert_to_billion(value_str):
    if "亿" in value_str:
        return float(value_str.replace("亿", ""))
    elif "万" in value_str:
        return round(float(value_str.replace("万", "")) / 10000, 6)
    return float(value_str)


# getHtmlTopData
def getStockIdToInfo(StockId):
    StockInfoArray = []
    engine = SQL.create_mysql_connection()
    query = text("select * from stockinfo where StockId = :stock_Id")
    result = engine.execute(query, stock_Id=StockId).fetchall()

    for row in result:
        StockInfoArray = list(row)

    StockInfoArray[3] = round(StockInfoArray[3]/100000000, 3)

    return StockInfoArray


def getStockIdToSelectDayData(StockId):
    # K图区域
    date = []
    value = []
    volume = []
    Turnover = []
    # 振幅 Amplitude
    Amplitude = []
    changePercent = []
    priceChange = []
    # 换手率
    TurnoverRate = []

    # PB,PE共有区域  日期
    StockPBandPEDate = []
    # PB, PE共有区域 个股收盘价
    StockCloseValue = []

    PB = []
    PE = []

    engine = SQL.create_mysql_connection()
    query = text("select StockDate, open, close, low, High, Volume,"
                 "Turnover, Amplitude, changePercent, priceChange,"
                 "TurnoverRate, pe, pb from stockdayandpepb where StockId like :stock_Id")

    result = engine.execute(query, stock_Id=f'%{StockId}').fetchall()

    for row in result:
        date.append(str(row[0]))

        StockPBandPEDate.append(str(row[0]))

        value.append([float(row[1]), float(row[2]), float(row[3]), float(row[4])])

        # 收盘价
        StockCloseValue.append(float(row[2]))

        volume.append(int(row[5]))

        # 元--->万元
        Turnover.append(round(float(row[6]) / 10000, 3))

        Amplitude.append(float(row[7]))

        changePercent.append(float(row[8]))

        priceChange.append(float(row[9]))

        TurnoverRate.append(float(row[10]))

        PE.append(float(row[11]))

        PB.append(float(row[12]))

    wwmiddlePB = find_median(PB)
    PBpercentile70 = round(find_percentile(PB, 70), 3)
    PBpercentile30 = find_percentile(PB, 30)

    wwmiddlePE = find_median(PE)
    PEpercentile70 = round(find_percentile(PE, 70), 3)
    PEpercentile30 = find_percentile(PE, 30)

    return date, value, volume, Turnover, Amplitude,\
        changePercent, priceChange, TurnoverRate,\
        StockPBandPEDate, StockCloseValue,\
        PB, wwmiddlePB, PBpercentile30, PBpercentile70,\
        PE, wwmiddlePE, PEpercentile30, PEpercentile70


def getStockIdToSelectWeekData(StockId):
    date = []
    value = []
    volume = []
    Turnover = []
    # 振幅 Amplitude
    Amplitude = []
    changePercent = []
    priceChange = []
    # 换手率
    TurnoverRate = []

    engine = SQL.create_mysql_connection()
    query = text("select StockDate, open, close, low, High, Volume,"
                 "Turnover, Amplitude, changePercent, priceChange,"
                 "TurnoverRate from stockweek where StockId like :stock_Id")

    result = engine.execute(query, stock_Id=f'%{StockId}').fetchall()

    for row in result:
        date.append(str(row[0]))

        value.append([float(row[1]), float(row[2]), float(row[3]), float(row[4])])

        volume.append(int(row[5]))

        # 元--->万元
        Turnover.append(round(float(row[6]) / 10000, 3))

        Amplitude.append(float(row[7]))

        changePercent.append(float(row[8]))

        priceChange.append(float(row[9]))

        TurnoverRate.append(float(row[10]))

    return date, value, volume, Turnover, Amplitude, changePercent, priceChange, TurnoverRate


def getStockIdToSelectMonthData(StockId):
    date = []
    value = []
    volume = []
    Turnover = []
    # 振幅 Amplitude
    Amplitude = []
    changePercent = []
    priceChange = []
    # 换手率
    TurnoverRate = []
    engine = SQL.create_mysql_connection()
    query = text("select StockDate, open, close, low, High, Volume,"
                 "Turnover, Amplitude, changePercent, priceChange,"
                 "TurnoverRate from stockmonth where StockId like :stock_Id")

    result = engine.execute(query, stock_Id=f'%{StockId}').fetchall()

    for row in result:
        date.append(str(row[0]))

        value.append([float(row[1]), float(row[2]), float(row[3]), float(row[4])])

        volume.append(int(row[5]))

        # 元--->万元
        Turnover.append(round(float(row[6])/10000, 3))

        Amplitude.append(float(row[7]))

        changePercent.append(float(row[8]))

        priceChange.append(float(row[9]))

        TurnoverRate.append(float(row[10]))

    return date, value, volume, Turnover, Amplitude, changePercent, priceChange, TurnoverRate


def getShareSumChange(StockId):
    date = []
    # 区间涨跌幅(%)折线Y2
    changePercent = []
    # 本次统计户数(柱状)
    shareholderssumthis = []
    # 户数增减(柱状)
    shareholderschangevalue = []
    # 户数增减比例(%)折线Y3
    shareholderschangepri = []
    # 人均市值(柱状)
    marketvalueper = []
    # 人均持股量(股)[柱状]
    stockper = []

    engine = SQL.create_mysql_connection()

    query = text("select reportdate, changePercent, shareholderssumthis, "
                 "shareholderschangevalue, shareholderschangepri, "
                 "marketvalueper, stockper from shareholderssum "
                 "where StockId =:stock_Id "
                 "ORDER BY reportdate ASC"
                 )

    result = engine.execute(query, stock_Id=StockId).fetchall()

    for row in result:
        # 对于每个可能为NULL的字段，使用三元运算符检查并赋值
        date.append(str(row[0]) if row[0] is not None else None)

        changePercent.append(float(row[1]) if row[1] is not None else None)

        # 当处理涉及计算的字段时，确保None值不会导致错误
        shareholderssumthis.append(round(float(row[2]) / 10, 1) if row[2] is not None else None)

        shareholderschangevalue.append(int(row[3]) if row[3] is not None else None)

        shareholderschangepri.append(float(row[4]) if row[4] is not None else None)

        # 类似地，确保None值在进行计算前被正确处理
        marketvalueper.append(round(float(row[5]) / 100, 3) if row[5] is not None else None)

        stockper.append(float(row[6]) if row[6] is not None else None)

    return date, changePercent, shareholderssumthis, shareholderschangevalue, shareholderschangepri, marketvalueper, stockper


def selectStockTotalSQL():
    StockName = []
    Totalmarketcapitalization = []

    engine = SQL.create_mysql_connection()
    query = text("select StockName, Totalmarketcapitalization from stockinfo"
                 " order by Totalmarketcapitalization desc limit 12")

    result = engine.execute(query).fetchall()

    for row in result:
        StockName.append(str(row[0]))

        Totalmarketcapitalization.append(float(row[1]))

    markValuePrize = round(sum(Totalmarketcapitalization)/34167376600320, 4)*100

    return StockName, Totalmarketcapitalization, markValuePrize


def getEquityAnnouncements(StockId):
    date = []
    changeinshare = []
    reasonsforchanges = []

    engine = SQL.create_mysql_connection()
    query = text("select reportdate, changeinshare, reasonsforchanges"
                 " from shareholderssum where StockId = :stock_Id "
                 "ORDER BY reportdate ASC")

    result = engine.execute(query, stock_Id=StockId)

    for row in result:
        date.append(str(row[0]) if row[0] is not None else None)

        changeinshare.append(int(row[1]) if row[1] is not None else None)

        reasonsforchanges.append(str(row[2]) if row[2] is not None else None)

    return date, changeinshare, reasonsforchanges

def SelectNetprofitStockSQL(StockId):
    StockDate = []
    # 净利润
    Netprofit = []
    # 净利润同比增长率
    Netprofitgrowthrate = []
    # 扣非净利润
    NotNetprofit = []
    # 扣非净利润同比增长率
    NotNetprofitgrowthrate = []

    engine = SQL.create_mysql_connection()
    query = text("select StockDate, Netprofit, Netprofitgrowthrate,\
       NotNetprofit, NotNetprofitgrowthrate from stockfinance where"
                 " stockId = :stock_Id ORDER BY StockDate ASC")

    result = engine.execute(query, stock_Id=StockId)

    for row in result:
        StockDate.append(str(row[0]))

        Netprofit.append(str(row[1]))

        value_without_percent = row[2].replace('%', '')
        Netprofitgrowthrate.append(float(value_without_percent))

        NotNetprofit.append(str(row[3]))

        value_without_percent2 = row[4].replace('%', '')
        NotNetprofitgrowthrate.append(float(value_without_percent2))

    NetprofitFloat = [convert_to_billion(value) for value in Netprofit]
    NotNetprofitFloat = [convert_to_billion(value2) for value2 in NotNetprofit]

    return StockDate, NetprofitFloat, Netprofitgrowthrate,\
        NotNetprofitFloat, NotNetprofitgrowthrate

def SelectOtherFinance(StockId):
    # 每股基本收益(元)
    Basic = []
    #每股净资产
    Netassets = []
    #每股资本公积金
    Capitalreserve = []
    #每股未分配利润
    Undistributedprofit = []
    # 每股净资产收益率
    Returnonequity = []

    engine = SQL.create_mysql_connection()
    query = text("select Basic, Netassets, Capitalreserve, \
                    Undistributedprofit, Returnonequity from \
                    stockfinance where stockId = :stock_Id \
                    order by StockDate asc ;")

    result = engine.execute(query, stock_Id=StockId)

    for row in result:
        Basic.append(float(row[0]) if row[0] is not None else None)

        Netassets.append(float(row[1]))

        Capitalreserve.append(float(row[2]))

        Undistributedprofit.append(float(row[3]))

        Returnonequity_value = row[4].replace('%', '')
        Returnonequity.append(float(Returnonequity_value))

    return Basic, Netassets, Capitalreserve, Undistributedprofit, Returnonequity


def TotalincomeFinance(StockId):
    # 营业总收入
    Totalincome = []
    # 营业总收入同比变化率
    Totalincomegrowthrate = []
    # 销售净利率
    Netprofitmargin = []
    # 毛利率
    Grosssales = []

    engine = SQL.create_mysql_connection()
    query = text("select Totalincome, Totalincomegrowthrate, \
                    Netprofitmargin, Grosssales \
                    from stockfinance where stockId = :stock_id \
                    order by StockDate asc ;")

    result = engine.execute(query, stock_id=StockId)

    for row in result:
        Totalincome.append(str(row[0]))

        TotalincomegrowthrateValue = row[1].replace('%', '')
        Totalincomegrowthrate.append(float(TotalincomegrowthrateValue))

        NetprofitmarginValue = row[2].replace('%', '')
        Netprofitmargin.append(float(NetprofitmarginValue))

        Grosssales.append(float(row[3]) if row[3] is not None else None)

    TotalincomeFloat = [convert_to_billion(value) for value in Totalincome]

    return TotalincomeFloat, Totalincomegrowthrate, Netprofitmargin, Grosssales


