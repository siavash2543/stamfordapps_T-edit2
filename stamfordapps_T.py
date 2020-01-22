import requests
from bs4 import BeautifulSoup
import mysql.connector
import dateparser
 
db =mysql.connector.connect(user='siavashtajaddini', password='admin123', host='localhost', database='stamfordapps')

url ='https://stamfordapps.org/restaurantratings/ListRestaurants.aspx?SType=All&slabel=est_id&sdir=Asc'
r= requests.get(url)
contents = BeautifulSoup(r.text,"html.parser")

tables=[]
datas_table=contents.findAll("table",{"cellspacing":"0","cellpadding":"5","align":"Center","rules":"all","border":"1","id":"grdData"})
for table in datas_table:
    headers=[]
    rows=table.findAll('tr')
   
    
    for header in table.find('tr').findAll('th')[1:9]:
        headers.append(header.text)
    
    for row in table.findAll('tr')[1: ]:
        values=[]
        for col in row.findAll('td')[1:9]:
            values.append(col.text)
        if values:
            tablesDict={headers[i]:values[i] for i in range(len(values))}           
            tables.append(tablesDict)
            

for data in tables:
    print(data)
            
db=mysql.connector.connect(user='siavashtajaddini', password='admin123', host='localhost', database='stamfordapps')
cursor=db.cursor()
cursor.execute("DROP TABLE IF EXISTS restaurants")

restaurants=(""" CREATE TABLE restaurants (
ID int(10) PRIMARY KEY,
Name varchar(30) NOT NULL,
Address varchar(50) NOT NULL,
Zip int(10) NOT NULL,
Contact varchar(20) NOT NULL,
Type varchar(20) NOT NULL,
Date varchar(20) NOT NULL,
Rating varchar(20) NOT NULL);""")

cursor.execute(restaurants)

add_restaurants = "INSERT INTO restaurants(ID,Name,Address,Zip,Contact,Type,Date,Rating) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)".format(ID,Name,Address,Zip,Contact,Type,Date,Rating)

try:    
    cursor.execute(add_restaurants)
    db.commit()

except:   
    db.rollback()
    db.close()
    



