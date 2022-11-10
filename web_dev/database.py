import sqlite3 as sql

con = sql.connect('maindatabase.db')
c = con.cursor()
# c.execute('create table logindb(username text unique not null,password text not null)')
# c.execute('create table product_details(id text primary key , title text not null , desc text , category text not null, mrp float not null, prev_price float,photo blob not null)')
# c.execute('drop table logindb')
# c.execute('drop table product_details')
con.commit()
con.close()