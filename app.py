from flask import Flask, render_template, redirect, url_for, request, session

import SelectStockOverviewSQL
import SelectTop10StockShareSQL
import selectIndexRightSQL
import selectIndexTopSQL
import selectStockInfoSQL
import selectStockListSQL
import selectindexmiddleSQL
import SelectCSI300ForecastSQL
import SelectStockForecastSQL
from loginSQL import is_null, is_existed, exist_user
from registerSQL import add_user
from changePwSQL import change_is_null, oldPassword, rePassword
import userStockSQL

app = Flask(__name__, static_folder='assets', template_folder='.')
app.jinja_env.globals.update(zip=zip)
app.secret_key = 'Ginka'


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # 注册发送的请求为POST请求
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_massage = "账号和密码是必填"
            return render_template('login.html', message=login_massage)
        elif is_existed(username, password):
            session['username'] = username
            return redirect(url_for('userProfile') + '?username=' + username)
        elif exist_user(username):
            login_massage = "密码错误，请输入正确密码"
            return render_template('login.html', message=login_massage)
        else:
            login_massage = "不存在该用户，请先注册"
            return render_template('login.html', message=login_massage)
    return render_template('login.html')


@app.route('/register.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if is_null(username, password):
            login_massage = "账号和密码是必填"
            return render_template('register.html', message=login_massage)
        elif exist_user(username):
            login_massage = "用户已存在，请直接登录"
            return render_template('register.html', message=login_massage)
        else:
            add_user(request.form['username'], request.form['password'])
            return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/userProfile.html', methods=['GET', 'POST'])
def userProfile():
    username = session.get('username', '游客')

    if request.method == 'POST':
        form_type = request.form.get('form_type')

        if form_type == 'change_password':
            OldPassword = request.form['oldpassword']
            NewPassword = request.form['newpassword']
            RenewPassword = request.form['renewpassword']


            if change_is_null(OldPassword, NewPassword, RenewPassword):
                changemes = "密码输入框都需要填写"
                return render_template('userProfile.html', message=changemes, username=username)
            elif not oldPassword(username, OldPassword):
                changemes = "旧密码不正确"
                return render_template('userProfile.html', message=changemes, username=username)
            elif not rePassword(NewPassword, RenewPassword, username):
                changemes = "新密码和重复新密码不匹配"
                return render_template('userProfile.html', message=changemes, username=username)
            else:
                changemes = "密码更新成功"
                # 更新session中的密码信息可能需要，根据应用逻辑调整
                # session['password'] = NewPassword
                return render_template('userProfile.html', message=changemes, username=username)

        elif form_type == 'delete_stock':
            getdeleteStock = request.form['deleteStock']
            userStockSQL.delUserStock(username, getdeleteStock)

    user_StockID, user_StockName, user_Industry, user_Totalmarket = userStockSQL.selectUserAllStock(username)
    user_stocks = [
        {"id": user_StockID[i], "name": user_StockName[i], "industry": user_Industry[i],
         "total_market_cap": user_Totalmarket[i]}
        for i in range(len(user_StockID))
    ]
    StockName, StockNamecounts, top12StockName, StockIndustry,\
        StockIndustrycounts, top12Industry = userStockSQL.selectTopStockNameAndIndustry()
    return render_template('userProfile.html', username=username, user_stocks=user_stocks,
                           StockName=StockName, StockNamecounts=StockNamecounts,
                           top12StockName=top12StockName, StockIndustry=StockIndustry,
                           StockIndustrycounts=StockIndustrycounts, top12Industry=top12Industry)


@app.route('/CSI300index.html')
def CSI300index():
    # 从根目录发送 CSI300index.html 文件
    sh_count, sh_percentage, sz_count, sz_percentage = selectIndexTopSQL.count_shsz_stock()
    pitalization = selectIndexTopSQL.Totalmarketcapitalization()
    stockindustries, stockcount, top12cupancy = selectIndexRightSQL.get_stock_Industry()
    markvuluetype, typecount = selectIndexRightSQL.marketvalue()
    csi300daydate, csi300dayvalue, csi300dayvolume, daypriceChange, daychangePercent, dayTurnover = selectindexmiddleSQL.selectCSIDayData()
    csi300weekdate, csi300weekvalue, csi300weekvolume, weekchangePercent, weekTurnover, weekturn = selectindexmiddleSQL.selectCSIWeekData()
    csi300monthdate, csi300monthvalue, csi300monthvolume, MonthchangePercent, MonthTurnover, Monthturn = selectindexmiddleSQL.selectCSIMonthData()
    NorthboundDate, NorthboundBuy, NorthboundCumulativeBuy = selectindexmiddleSQL.northbound()
    CSIPBDate, CSIPBValue, PB, wwmiddlePB, PBpercentile30, PBpercentile70 = selectindexmiddleSQL.CSIPBinfo()
    CSIPEDate, CSIPEValue, PE, wwmiddlePE, PEpercentile30, PEpercentile70 = selectindexmiddleSQL.CSIPEinfo()

    username = session.get('username', '游客')

    return render_template('CSI300index.html',
                           sh_stock_count=sh_count, sh_stock_percentage=sh_percentage,
                           sz_stock_count=sz_count, sz_stock_percentage=sz_percentage,
                           outPutpitalization=pitalization, top12cupancy=top12cupancy,
                           stockIndustries=stockindustries, stockcount=stockcount,
                           markvuluetype=markvuluetype, typecount=typecount,
                           csi300daydate=csi300daydate, csi300dayvalue=csi300dayvalue, csi300dayvolume=csi300dayvolume,
                           daypriceChange=daypriceChange, daychangePercent=daychangePercent, dayTurnover=dayTurnover,
                           csi300weekdate=csi300weekdate, csi300weekvalue=csi300weekvalue, csi300weekvolume=csi300weekvolume,
                           weekchangePercent=weekchangePercent, weekTurnover=weekTurnover, weekturn=weekturn,
                           csi300monthdate=csi300monthdate, csi300monthvalue=csi300monthvalue, csi300monthvolume=csi300monthvolume,
                           MonthchangePercent=MonthchangePercent, MonthTurnover=MonthTurnover, Monthturn=Monthturn,
                           NorthboundBuy=NorthboundBuy, NorthboundCumulativeBuy=NorthboundCumulativeBuy, NorthboundDate=NorthboundDate,
                           CSIPBDate=CSIPBDate, CSIPBValue=CSIPBValue, PB=PB, wwmiddlePB=wwmiddlePB,
                           PBpercentile30=PBpercentile30, PBpercentile70=PBpercentile70,
                           CSIPEDate=CSIPEDate, CSIPEValue=CSIPEValue, PE=PE, wwmiddlePE=wwmiddlePE,
                           PEpercentile30=PEpercentile30, PEpercentile70=PEpercentile70,
                           username=username
                           )


@app.route('/StockList.html', methods=['get', 'post'])
def StockList():
    StockID, StockName, StockIndustry, StockTotalmarketcapitalization = selectStockListSQL.selectStcokListData()
    username = session.get('username', '游客')

    stocks = [
        {"id": StockID[i], "name": StockName[i], "industry": StockIndustry[i],
         "total_market_cap": StockTotalmarketcapitalization[i]}
        for i in range(len(StockID))
    ]

    getUserStockList = userStockSQL.selectUserStockId(username)

    if request.method == 'POST':
        Stock_Id = request.form['StockId']
        Stock_Name = request.form['StockName']
        In_dustry = request.form['Industry']
        Total_market = request.form['Totalmarket']

        userStockSQL.addUserStockList(username, Stock_Id, Stock_Name, In_dustry, Total_market)
        getUserStockList = userStockSQL.selectUserStockId(username)

    return render_template('StockList.html', stocks=stocks, username=username,
                           getUserStockList=getUserStockList)


@app.route('/StockInfo.html')
def StockInfo():
    stock_name = request.args.get('StockName', '贵州茅台')
    company_name, english_name, former_abbreviation, a_share_code, \
    a_share_abbreviation, industry_sector, legal_representative, \
    registered_capital, establishment_date, listing_date, \
    official_website, email_address, contact_number, \
    fax, registered_address, office_address, \
    postal_code, main_business, business_scope,\
    organization_profile = selectStockInfoSQL.getStockInfo(stock_name)

    username = session.get('username', '游客')

    return render_template('StockInfo.html', stock_name=stock_name,
    company_name=company_name, english_name=english_name, former_abbreviation=former_abbreviation,
    a_share_code=a_share_code, a_share_abbreviation=a_share_abbreviation, industry_sector=industry_sector,
    legal_representative=legal_representative, registered_capital=registered_capital, establishment_date=establishment_date,
    listing_date=listing_date, official_website=official_website, email_address=email_address,
    contact_number=contact_number, fax=fax, registered_address=registered_address, office_address=office_address,
    postal_code=postal_code, main_business=main_business, business_scope=business_scope,
    organization_profile=organization_profile, username=username)


@app.route('/StockOverview.html')
def StockOverview():
    stock_id = request.args.get('StockId', '600519')
    TopStockId, TopStockName, TopStockIndustry, TopTotalmarketcapitalization\
        = SelectStockOverviewSQL.getStockIdToInfo(StockId=stock_id)

    Daydate, Dayvalue, Dayvolume, DayTurnover, DayAmplitude,\
        DaychangePercent, DaypriceChange, DayTurnoverRate,\
        StockPBandPEDate, StockCloseValue, \
        PB, wwmiddlePB, PBpercentile30, PBpercentile70, \
        PE, wwmiddlePE, PEpercentile30, PEpercentile70 = \
        SelectStockOverviewSQL.getStockIdToSelectDayData(StockId=stock_id)

    Weekdate, Weekvalue, Weekvolume, WeekTurnover,\
        WeekAmplitude, WeekchangePercent, WeekpriceChange,\
        WeekTurnoverRate = SelectStockOverviewSQL.getStockIdToSelectWeekData(StockId=stock_id)

    Monthdate, Monthvalue, Monthvolume, MonthTurnover,\
        MonthAmplitude, MonthchangePercent, MonthpriceChange,\
        MonthTurnoverRate = SelectStockOverviewSQL.getStockIdToSelectMonthData(StockId=stock_id)

    shareChangedate, shareChanechangePercent, shareholderssumthis,\
        shareholderschangevalue, shareholderschangepri,\
        marketvalueper, stockper = SelectStockOverviewSQL.getShareSumChange(StockId=stock_id)

    RinghtStockName, RightTotalmarketcapitalization\
        , markValuePrize = SelectStockOverviewSQL.selectStockTotalSQL()

    Ringhtdate, changeinshare, reasonsforchanges = SelectStockOverviewSQL.getEquityAnnouncements(StockId=stock_id)
    Rightactivities = zip(Ringhtdate, changeinshare, reasonsforchanges)

    profitDate, NetprofitFloat, Netprofitgrowthrate,\
        NotNetprofitFloat, NotNetprofitgrowthrate,\
        = SelectStockOverviewSQL.SelectNetprofitStockSQL(StockId=stock_id)

    Basic, Netassets, Capitalreserve, Undistributedprofit \
            ,Returnonequity = SelectStockOverviewSQL.SelectOtherFinance(StockId=stock_id)

    TotalincomeFloat, Totalincomegrowthrate,\
        Netprofitmargin, Grosssales = SelectStockOverviewSQL.TotalincomeFinance(StockId=stock_id)

    all_empty = all(not item[1] for item in Rightactivities)

    username = session.get('username', '游客')

    return render_template('StockOverview.html',
                           stock_id=stock_id, TopStockId=TopStockId,
                           TopStockName=TopStockName, TopStockIndustry=TopStockIndustry,
                           TopTotalmarketcapitalization=TopTotalmarketcapitalization,
                           Daydate=Daydate, Dayvalue=Dayvalue, Dayvolume=Dayvolume,
                           DayTurnover=DayTurnover, DayAmplitude=DayAmplitude,
                           DaychangePercent=DaychangePercent, DaypriceChange=DaypriceChange,
                           DayTurnoverRate=DayTurnoverRate,
                           StockPBandPEDate=StockPBandPEDate, StockCloseValue=StockCloseValue,
                           PB=PB, wwmiddlePB=wwmiddlePB, PBpercentile30=PBpercentile30, PBpercentile70=PBpercentile70,
                           PE=PE, wwmiddlePE=wwmiddlePE, PEpercentile30=PEpercentile30, PEpercentile70=PEpercentile70,
                           Weekdate=Weekdate, Weekvalue=Weekvalue, Weekvolume=Weekvolume,
                           WeekTurnover=WeekTurnover, WeekAmplitude=WeekAmplitude,
                           WeekchangePercent=WeekchangePercent, WeekpriceChange=WeekpriceChange,
                           WeekTurnoverRate=WeekTurnoverRate,
                           Monthdate=Monthdate, Monthvalue=Monthvalue, Monthvolume=Monthvolume,
                           MonthTurnover=MonthTurnover, MonthAmplitude=MonthAmplitude,
                           MonthchangePercent=MonthchangePercent, MonthpriceChange=MonthpriceChange,
                           MonthTurnoverRate=MonthTurnoverRate,
                           shareChangedate=shareChangedate, shareChanechangePercent=shareChanechangePercent,
                           shareholderssumthis=shareholderssumthis, shareholderschangevalue=shareholderschangevalue,
                           shareholderschangepri=shareholderschangepri, marketvalueper=marketvalueper,
                           stockper=stockper,
                           RinghtStockName=RinghtStockName, RightTotalmarketcapitalization=RightTotalmarketcapitalization,
                           markValuePrize=markValuePrize,
                           Rightactivities=Rightactivities, all_empty=all_empty,
                           profitDate=profitDate, NetprofitFloat=NetprofitFloat, Netprofitgrowthrate=Netprofitgrowthrate,
                           NotNetprofitFloat=NotNetprofitFloat, NotNetprofitgrowthrate=NotNetprofitgrowthrate,
                           Basic=Basic, Netassets=Netassets, Capitalreserve=Capitalreserve,
                           Undistributedprofit=Undistributedprofit, Returnonequity=Returnonequity,
                           TotalincomeFloat=TotalincomeFloat, Totalincomegrowthrate=Totalincomegrowthrate,
                           Netprofitmargin=Netprofitmargin, Grosssales=Grosssales, username=username
                           )


@app.route('/Top10StockShare.html')
def Top10StockShare():
    stock_id = request.args.get('StockId', '600519')

    ShareName, Nature, StockNumber, Proportion,\
        OutStanding, ChangeStock, SumProportion =\
        SelectTop10StockShareSQL.get2019StockNameAndShare(StockId=stock_id)

    ShareName20, Nature20, StockNumber20,\
        Proportion20, OutStanding20,\
        ChangeStock20, SumProportion20 = \
    SelectTop10StockShareSQL.get2020StockNameAndShare(StockId=stock_id)

    ShareName21, Nature21, StockNumber21,\
        Proportion21, OutStanding21,\
        ChangeStock21, SumProportion21 = \
    SelectTop10StockShareSQL.get2021StockNameAndShare(StockId=stock_id)

    ShareName22, Nature22, StockNumber22,\
        Proportion22, OutStanding22,\
        ChangeStock22, SumProportion22 = \
    SelectTop10StockShareSQL.get2022StockNameAndShare(StockId=stock_id)

    ShareName23, Nature23, StockNumber23,\
        Proportion23, OutStanding23,\
        ChangeStock23, SumProportion23 = \
    SelectTop10StockShareSQL.get2023StockNameAndShare(StockId=stock_id)

    getStockName = SelectTop10StockShareSQL.getStockShareName(StockId=stock_id)

    StockShareTops = [
        {"ShareName": ShareName[i], "Nature": Nature[i], "StockNumber":StockNumber[i], "Proportion": Proportion[i],
         "OutStanding": OutStanding[i], "ChangeStock":ChangeStock[i]}
        for i in range(len(StockNumber))
    ]

    StockShareTops20 = [
        {"ShareName": ShareName20[i], "Nature": Nature20[i], "StockNumber": StockNumber20[i], "Proportion": Proportion20[i],
         "OutStanding": OutStanding20[i], "ChangeStock": ChangeStock20[i]}
        for i in range(len(StockNumber20))
    ]

    StockShareTops21 = [
        {"ShareName": ShareName21[i], "Nature": Nature21[i], "StockNumber": StockNumber21[i], "Proportion": Proportion21[i],
         "OutStanding": OutStanding21[i], "ChangeStock": ChangeStock21[i]}
        for i in range(len(StockNumber21))
    ]

    StockShareTops22 = [
        {"ShareName": ShareName22[i], "Nature": Nature22[i], "StockNumber": StockNumber22[i], "Proportion": Proportion22[i],
         "OutStanding": OutStanding22[i], "ChangeStock": ChangeStock22[i]}
        for i in range(len(StockNumber22))
    ]

    StockShareTops23 = [
        {"ShareName": ShareName23[i], "Nature": Nature23[i], "StockNumber": StockNumber23[i], "Proportion": Proportion23[i],
         "OutStanding": OutStanding23[i], "ChangeStock": ChangeStock23[i]}
        for i in range(len(StockNumber23))
    ]

    username = session.get('username', '游客')

    return render_template('Top10StockShare.html', getStockName=getStockName,
                           StockShareTops=StockShareTops, SumProportion=SumProportion,
                           StockShareTops20=StockShareTops20, SumProportion20=SumProportion20,
                           StockShareTops21=StockShareTops21, SumProportion21=SumProportion21,
                           StockShareTops22=StockShareTops22, SumProportion22=SumProportion22,
                           StockShareTops23=StockShareTops23, SumProportion23=SumProportion23,
                           username=username
                           )


@app.route('/StockForecast.html')
def StockForecast():
    Date1923, closeValue1923 = SelectCSI300ForecastSQL.selectcsi300()
    Date2024, closeValue2024 = SelectCSI300ForecastSQL.select2024csi300()
    forecastClose = SelectCSI300ForecastSQL.selectcsi300forecast()
    AgeForecastClose = SelectCSI300ForecastSQL.selectcsi300forecastAge()
    Date1924 = Date1923 + Date2024

    # 为closeValue1923添加null以匹配Date1924的长度
    closeValue1923 += [None] * (len(Date1924) - len(closeValue1923))

    # 为closeValue2024和forecastClose在前面填充null
    padding_length_2024 = len(Date1924) - len(closeValue2024)
    closeValue2024 = [None] * padding_length_2024 + closeValue2024

    padding_length_forecast = len(Date1924) - len(forecastClose)
    forecastClose = [None] * padding_length_forecast + forecastClose

    padding_length_forecastAge = len(Date1924) - len(AgeForecastClose)
    AgeForecastClose = [None] * padding_length_forecastAge + AgeForecastClose

    username = session.get('username', '游客')

    return render_template('StockForecast.html',
                            Date1924=Date1924,
                            closeValue1923=closeValue1923, closeValue2024=closeValue2024,
                            forecastClose=forecastClose, AgeForecastClose=AgeForecastClose,
                            username=username)


@app.route('/StockForecast300.html')
def StockForecast300():
    stock_id = request.args.get('StockId', '600519')
    StockName = SelectStockForecastSQL.SelectStockNameTitle(StockId=stock_id)
    Date1923, closeValue1923 = SelectStockForecastSQL.select1923StockDayData(StockId=stock_id)
    Date2024, closeValue2024 = SelectStockForecastSQL.select2024StockDayData(StockId=stock_id)
    forecastClose = SelectStockForecastSQL.selectStockforecast(StockId=stock_id)
    AgeForecastClose = SelectStockForecastSQL.selectStockforecastAge(StockId=stock_id)
    Date1924 = Date1923 + Date2024

    # 为closeValue1923添加null以匹配Date1924的长度
    closeValue1923 += [None] * (len(Date1924) - len(closeValue1923))

    # 为closeValue2024和forecastClose在前面填充null
    padding_length_2024 = len(Date1924) - len(closeValue2024)
    closeValue2024 = [None] * padding_length_2024 + closeValue2024

    padding_length_forecast = len(Date1924) - len(forecastClose)
    forecastClose = [None] * padding_length_forecast + forecastClose

    padding_length_forecastAge = len(Date1924) - len(AgeForecastClose)
    AgeForecastClose = [None] * padding_length_forecastAge + AgeForecastClose

    username = session.get('username', '游客')

    return render_template('StockForecast300.html', StockName=StockName,
                           Date1924=Date1924, closeValue1923=closeValue1923,
                           closeValue2024=closeValue2024, forecastClose=forecastClose,
                           AgeForecastClose=AgeForecastClose, username=username)

if __name__ == '__main__':
    app.run()


