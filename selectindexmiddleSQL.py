import SQL
from sqlalchemy.sql import text

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


def selectCSIDayData():
    value = []
    volume = []
    date = []
    daypriceChange = []
    daychangePercent = []
    dayTurnover=[]
    engine = SQL.create_mysql_connection()
    query = text("select CSIDate, open, close, low, High, Volume, priceChange, changePercent, Turnover from csi300indexday")
    result = engine.execute(query).fetchall()

    for row in result:
        # 将日期添加到 date 数组
        date.append(str(row[0]))

        # 将 open, close, low, High 作为一个子列表添加到 value 数组
        value.append([float(row[1]), float(row[2]), float(row[3]), float(row[4])])

        # 将 Volume 添加到 volume 数组
        volume.append(int(row[5]))

        daypriceChange.append(float(row[6]))

        daychangePercent.append(float(row[7]))

        dayTurnover.append(float(row[8]))

    return date, value, volume,  daypriceChange, daychangePercent, dayTurnover

def selectCSIWeekData():
    value = []
    volume = []
    date = []
    WeekchangePercent = []
    WeekTurnover = []
    Weekturn = []

    engine = SQL.create_mysql_connection()
    query = text("select CSIDate, open, close, low, High, Volume, changePercent, Turnover, Turn from csi300indexweek")
    result = engine.execute(query).fetchall()

    for row in result:
        # 将日期添加到 date 数组
        date.append(str(row[0]))

        # 将 open, close, low, High 作为一个子列表添加到 value 数组
        value.append([float(row[1]), float(row[2]), float(row[3]), float(row[4])])

        # 将 Volume 添加到 volume 数组
        volume.append(round(int(row[5])/10000, 3))

        WeekchangePercent.append(float(row[6]))

        WeekTurnover.append(round(float(row[7])/10000, 3))

        Weekturn.append(float(row[8]))

    return date, value, volume, WeekchangePercent, WeekTurnover, Weekturn


def selectCSIMonthData():
    value = []
    volume = []
    date = []
    MonthchangePercent = []
    MonthTurnover = []
    Monthturn = []

    engine = SQL.create_mysql_connection()
    query = text("select CSIDate, open, close, low, High, Volume, changePercent, Turnover, Turn from csi300indexmonth")
    result = engine.execute(query).fetchall()

    for row in result:
        # 将日期添加到 date 数组
        date.append(str(row[0]))

        # 将 open, close, low, High 作为一个子列表添加到 value 数组
        value.append([float(row[1]), float(row[2]), float(row[3]), float(row[4])])

        # 将 Volume 添加到 volume 数组
        volume.append(round(int(row[5])/10000, 3))

        MonthchangePercent.append(float(row[6]))

        MonthTurnover.append(round(float(row[7])/10000, 3))

        Monthturn.append(float(row[8]))

    return date, value, volume, MonthchangePercent, MonthTurnover, Monthturn


def northbound():
    NorthboundDate = []
    NorthboundBuy = []
    NorthboundCumulativeBuy = []

    engine = SQL.create_mysql_connection()
    query = text("select * from northbound")
    result = engine.execute(query).fetchall()

    for row in result:
        NorthboundDate.append(str(row[0]))
        NorthboundBuy.append(str(round(row[1]/10000, 3)))
        NorthboundCumulativeBuy.append(str(round(row[2]/10000, 3)))

    return NorthboundDate, NorthboundBuy, NorthboundCumulativeBuy

def CSIPBinfo():
    CSIPBDate = []
    CSIPBValue = []
    PB = []


    engine = SQL.create_mysql_connection()
    query = text("select * from csi300indexdaypb")
    result = engine.execute(query).fetchall()

    for row in result:
        CSIPBDate.append(str(row[0]))
        CSIPBValue.append(str(row[1]))
        PB.append(float(row[2]))

    wwmiddlePB = find_median(PB)
    PBpercentile70 = find_percentile(PB, 70)
    PBpercentile30 = find_percentile(PB, 30)

    return CSIPBDate, CSIPBValue, PB, wwmiddlePB, PBpercentile30, PBpercentile70

def CSIPEinfo():
    CSIPEDate = []
    CSIPEValue = []
    PE = []


    engine = SQL.create_mysql_connection()
    query = text("select * from csi300indexdaype")
    result = engine.execute(query).fetchall()

    for row in result:
        CSIPEDate.append(str(row[0]))
        CSIPEValue.append(str(row[1]))
        PE.append(float(row[6]))

    wwmiddlePE = round(find_median(PE), 2)
    PEpercentile70 = find_percentile(PE, 70)
    PEpercentile30 = find_percentile(PE, 30)

    return CSIPEDate, CSIPEValue, PE, wwmiddlePE, PEpercentile30, PEpercentile70