import pymssql
import mpl_finance

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

