import requests
import mysql.connector
from bs4 import BeautifulSoup

db =mysql.connector.connect(user='siavashtajaddini', password='admin123', host='localhost', database='stamfordapps')
url = 'https://stamfordapps.org/restaurantratings/ListRestaurants.aspx?SType=All&slabel=est_id&sdir=Asc/'
result = requests.get(url)
soup = BeautifulSoup(result.text,"html.parser")

datas_table=soup.findAll("table",{"cellspacing":"0","cellpadding":"5","align":"Center","rules":"all","border":"1","id":"grdData"})

for table in datas_table:
    for row in table.findAll("tr")[1: ]:  
        cells = row.findAll("td")[1:9]
        if(len(cells) >0):
            ID=cells[1].text.strip()
            Name = cells[2].text.strip()
            Address = cells[3].text.strip()
            Zip = cells[4].text.strip()
            Contact = cells[5].text.strip()
            Type = cells[6].text.strip()
            Date = cells[7].text.strip()
            Rating = Cells[8].text.strip()
            
db =mysql.connector.connect(user='siavashtajaddini', password='admin123', host='localhost', database='stamfordapps')
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

add_restaurants = "INSERT INTO Restaurants(ID,Name,Address,Zip,Contact,Type,Date,Rating) VALUES (%s,%s,%s,%i,%s,%s,%s,%s)".format(ID,Name,Address,Zip,Contact,Type,Date,Rating)

try:   
    cursor.execute(add_restaurants )
    db.commit()
except:
    db.rollback()
    
try:
    cursor.execute(add_restaurants )
    result = cursor.fetchall()   
except:
    db.rollback()
    db.close()






