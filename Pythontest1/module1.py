import datetime as dt
import matplotlib.pyplot as plt
import mpl_finance as mpf
import matplotlib.ticker as ticker
import matplotlib.dates as mdates
import pymssql
import pandas as pd
import xlrd
import pyodbc
sqlresult = []

DateTime = []
Open = []
Close = []
High = []
Low = []
#Time = []
CandleVolume =[]
CandleOI = []
Timestr = []


tradedatetime = []
tradeprice = []
tradeposition = []
Buydatetime = []
Selldatetime = []
Buyposition = []
Sellposition =[]
Buyprice = []
Sellprice = []

#TimeCandlelist = []
def loadexcel(excelpath,sheetname='Sheet1'):
    df=pd.read_excel(excelpath,sheet_name=sheetname)
    print(df.head(10))
    pass
#encounter problem when deal with Chinese characters
def loadcsv(csvpath):
    df=pd.read_csv(csvpath,)
    print(df.head(10))
    pass

def loadTimetext(textpath):
    Open.clear()
    DateTime.clear()
    Close.clear()
    High.clear()
    Low.clear()
    CandleVolume.clear()
    #CandleOI.clear()
    #pullResult = open(textpath,'r').read()
    pullcsv = open(textpath,'r')
    eline = pullcsv.readline()
    #dataArray = pullResult.split('\n')
    while(eline):
        eline = pullcsv.readline()
        if len(eline)>5:
            line  = eline.split(',')
            t1 = dt.datetime.strptime(line[0]+' '+line[1], '%m/%d/%Y %H:%M:%S.%f')
            DateTime.append(t1)
            Open.append(float(line[2]))
            High.append(float(line[3]))
            Low.append(float(line[4]))
            Close.append(float(line[5]))
            CandleVolume.append(int(line[6]))
            #CandleOI.append(int(line[6]))
    pass

def loadtradetext(textpath):
    tradedatetime.clear()
    tradeprice.clear()
    tradeposition.clear()
    pullcsv = open(textpath,'r')
    eline = pullcsv.readline()
    while(eline):
        eline = pullcsv.readline()
        if len(eline)>5:
            line  = eline.split('\t')
            t1 = dt.datetime.strptime(line[13]+' '+line[14][:-3],'%Y%m%d %H:%M')
            #tradedatetime.append(t1)
            if(line[7]=='买'):
                #tradeposition.append(int(line[11]))
                Buydatetime.append(t1)
                Buyposition.append(int(line[11]))
                Buyprice.append(float(line[10]))
            elif(line[7]=='卖'):
                #tradeposition.append(-int(line[11]))
                Selldatetime.append(t1)
                Sellposition.append(int(line[11]))
                Sellprice.append(float(line[10]))
            else:
                #tradeposition.append(0)
                pass
            #tradeprice.append(float(line[10]))
    pass
#pymssql version. problem for datetime import
def text2db(textpath):
    pullcsv = open(textpath,'r')
    eline = pullcsv.readline()
    with pymssql.connect(host=r'127.0.0.1',user = 'sa', password ='qshmxh',database ='dbcldata',charset='utf8') as conn:
        with conn.cursor() as cursor:
            while(eline):
                eline = pullcsv.readline()
                if len(eline)>5:
                    line  = eline.split(',')
                    t1 = dt.datetime.strptime(line[0]+' '+line[1], '%m/%d/%Y %H:%M:%S.%f')
                    strt1 = t1.strftime('%Y-%m-%d %H:%M:%S')
                    dataopen = float(line[2])
                    datahigh = float(line[3])
                    datalow  = float(line[4])
                    dataclose = float(line[5])
                    datavolume = int(line[6])
                    sql = "insert into CL18021811 (_datetime,_open,_high,_low,_close,_volume) values (%s,%d,%d,%d,%d,%d)"
                    sqltuple = (strt1,dataopen,datahigh,datalow,dataclose,datavolume)
                    cursor.execute(sql,sqltuple)
                    conn.commit()
    pass
#combine with trade record plotting
def plotTimeCandle():
    #fig = plt.figure(figsize =(8,6))
    plt.clf
    fig=plt.figure(figsize=(8,6))
    ax = fig.add_axes([0.1,0.35,0.8,0.5])
    #ax2 = fig.add_axes([0.1,0.15,0.8,0.2])
    ax.yaxis.tick_right()
    #ax2.yaxis.tick_right()

    quotes = mdates.date2num(DateTime), Open, High, Low, Close
    quotes = list(map(list,zip(*quotes)))
    mpf.candlestick_ohlc(ax,quotes,width =0.0001,colorup='green',colordown='red',alpha=1)

    #mpf.candlestick2_ochl(ax,Open,Close,High,Low,width =0.5,colorup='green',colordown='red',alpha=1)
    #ax.set_xticklabels(DateTime,rotation =90)
    #ax.set_xticks(range(0,len(DateTime),1))
    #mpf.volume_overlay(ax2, Open, Close, CandleVolume, colorup='green', colordown='red', width=0.5, alpha=0.8)
    #ax2.set_xticklabels(DateTime,rotation ="vertical")
    #ax2.set_xticks(range(0,len(DateTime),1))
    #ax.scatter(tradedatetime,tradeprice,s=20,c=tradeposition,marker='o')
    ax.scatter(Buydatetime,Buyprice,s=20*Buyposition,c='blue',marker='o')
    ax.scatter(Selldatetime,Sellprice,s=20*Sellposition,c='red',marker='o')
    locator = mdates.MinuteLocator(byminute = [0,30])
    locator.MAXTICKS =40000
    ax.xaxis.set_major_locator(locator)
    majorFmt = mdates.DateFormatter('%m-%d %H:%M:%S')  
    ax.xaxis.set_major_formatter(majorFmt)

    #locator = ticker.MultipleLocator(6)
    #locator.MAXTICKS = 140000
    #ax.xaxis.set_major_locator(locator)
    #ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
    #ax.set_xlim([DateTime[0],DateTime[-1]])
    xlabels = ax.get_xticklabels()
    #plt.subplots_adjust(hspace=0,bottom =0.2)
    plt.setp(xlabels, rotation = 60)
    #ax.scatter(tradedatetime,tradeprice,s=20,c=tradeposition,marker='o')
    #ax.legend(loc='upper left')
    #plt.grid()
    
    plt.show()
    
    pass

def candlefromodbc(startdt,numofcandle):
    with pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=127.0.0.1;DATABASE=dbcldata;UID=sa;PWD=qshmxh') as conn:
        with conn.cursor() as cursor:
            sql = "select top("+str(numofcandle)+") * from CL18021811 where _datetime >= "+ "'" + startdt + "'"
            cursor.execute(sql)
            result = cursor.fetchall()

            conn.commit()
            Open.clear()
            DateTime.clear()
            Close.clear()
            High.clear()
            Low.clear()
            CandleVolume.clear()
            for row in result:
                DateTime.append(row[0])
                Open.append(row[1])
                High.append(row[2])
                Low.append(row[3])
                Close.append(row[4])
                CandleVolume.append(row[5])
                pass
    pass

#def format_date(x,pos=None):
#    if x<0 or x>len(DateTime)-1:
#        return ''
#    return DateTime[int(x)]
#pass

#discard
def plotTradeRecord():
    plt.clf
    fig=plt.figure(figsize=(8,6))
    ax = fig.add_axes([0.1,0.35,0.8,0.5])
    ax.scatter(tradedatetime,tradeprice,s=20,c=tradeposition,marker='o')
    ax.set_xlim([tradedatetime[0],tradedatetime[-1]])
    plt.show()
    pass
#pyodbc version.
def text2odbc(textpath):
    pullcsv = open(textpath,'r')
    eline = pullcsv.readline()
    with pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=127.0.0.1;DATABASE=dbcldata;UID=sa;PWD=qshmxh') as conn:
        with conn.cursor() as cursor:
            while(eline):
                eline = pullcsv.readline()
                if len(eline)>5:
                    line  = eline.split(',')
                    t1 = dt.datetime.strptime(line[0]+' '+line[1], '%m/%d/%Y %H:%M:%S.%f')
                    strt1 = t1.strftime('%Y-%m-%d %H:%M:%S')
                    dataopen = float(line[2])
                    datahigh = float(line[3])
                    datalow  = float(line[4])
                    dataclose = float(line[5])
                    datavolume = int(line[6])
                    sql = "insert into CL18021811 (_datetime,_open,_high,_low,_close,_volume) values (?,?,?,?,?,?)"
                    sqltuple = (strt1,dataopen,datahigh,datalow,dataclose,datavolume)
                    cursor.execute(sql,sqltuple)
                    conn.commit()
    pass
# by minutes
def setinterval(interval):
    tdelta = dt.timedelta(minutes = interval)
    formerDatetime = DateTime
    formerOpen = Open
    formerHigh = High
    formerLow = Low
    formerClose = Close
    formerVolume = CandleVolume
    Open.clear()
    DateTime.clear()
    Close.clear()
    High.clear()
    Low.clear()
    CandleVolume.clear()
    

    pass



#loadexcel(r'D:\Research\9138288(1).xlsx','9138288')
#loadcsv(r'D:\Research\9138288(1).csv')
candlefromodbc("2018-03-02 00:00",20)
#text2odbc(r'D:\Research\CME.CL HOT.csv')

setinterval(5)

#text2db(r'D:\Research\CME.CL HOT.csv')
#loadTimetext(r'D:\Research\test1.txt')
#loadtradetext(r'D:\Research\tradingtest1.txt')
#loadTimetext(r'D:\Research\CME.CL HOT.csv')
#plotTimeCandle()
#plotTradeRecord()


