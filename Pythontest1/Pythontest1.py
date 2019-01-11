import pymssql
import mpl_finance
import pyodbc
class Candle1():
    def __init__(self, open1, high1, low1, close1):
        self.open = open1
        self.high = high1
        self.low = low1
        self.close = close1

    def printopen(self):
        return self.open


my_candle1 = Candle1(10,20,30,40)
my_candle2 = Candle1(100,200,300,400)
candlelist=[]
candlelist.append(my_candle1)
candlelist.append(my_candle2)
candlelist[1].printopen()

conn = pymssql.connect(host=r'DESKTOP-8OMB7OV\SQLEXPRESS',user = 'sa', password ='qshmxh',database ='dbcontact',charset='utf8')
print(conn)
cursor = conn.cursor()
#sql = 'select * from Contacts'
sql = "insert into Contacts () values()"
cursor.execute(sql)
#rs = cursor.fetchall()
rs = cursor.fetchone()
cursor.close()
conn.close()
print(rs)

with pymssql.connect(host=r'DESKTOP-8OMB7OV\SQLEXPRESS',user = 'sa', password ='qshmxh',database ='dbcontact',charset='utf8') as conn:
    with conn.cursor() as cursor:
        sql = 'select * from Contacts'
        cursor.execute(sql)
        rs = cursor.fetchall()
        for row in rs:
            print(row)
        pass
    pass




with pymssql.connect(host=r'DESKTOP-8OMB7OV\SQLEXPRESS',user = 'sa', password ='qshmxh',database ='dbcontact',charset='utf8') as conn:
    with conn.cursor() as cursor:
        test1 = '5266252'
        sql = "insert into Contacts (ContactName,Email,PhoneNumber,Address) values(%s,%s,%s,%s)"
        sqllist = ('Johnson','johnson@gmail.com',test1,'dac 14')
        cursor.execute(sql,sqllist)

        #sql = "insert into Contacts(ContactName,Email,PhoneNumber,Address) values(%d,%s,%s,%s)"
        #sqllist =[('Johnson','johnson@gmail.com','5266252','dac14'),('kitty','kitty@gmail.com','5152','ddw14')]
        #cursor.executemany(sql,sqllist)

        #sql = "Update Contacts set PhoneNumber = %s where Id = %d"
        #cursor.execute(sql,('256125',7))
        conn.commit()

pass



def candlefromodbc(startdt,numofcandle):
    with pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};SERVER=127.0.0.1;DATABASE=dbcldata;UID=sa;PWD=qshmxh') as conn:
        with conn.cursor() as cursor:
            #sql = "select top("+str(numofcandle)+") * from CL18021811 where _datetime >= "+ startdt
            sql = "select top("+str(numofcandle)+") * from CL18021811 where _datetime >= "+'\'2018-03-02T02:01\''
            cursor.execute(sql)
            result = cursor.fetchall()
            sqlresult.append(result)
            conn.commit()
    pass

candlefromodbc('2018-03-02 00:00',10)

str1 ="_datetime >= "
str2 ="'2018-03-02T02:01'"
teststr = str1+str2