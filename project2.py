import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='project2',
                                         user='root',
                                         password='Partida@124426')
    if connection.is_connected():
        #1:Printing titles.
        query = "select * from titles"
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute(query)
        print('1.)Printing titles.')
        for row in cursor.fetchall():
            print(row)
        print(' ') 
        
        #2:Create a table customer.
        mySql_Create_Table_Query = """CREATE TABLE IF NOT EXISTS customer ( 
                             custID Int(6) NOT NULL,
                             custName varchar(30) NULL,
                             zip INT(5) NULL,
                             city VARCHAR(15) NULL,
                             state VARCHAR(15) NULL,
                             PRIMARY KEY (custID)) """
        cursor = connection.cursor()
        result = cursor.execute(mySql_Create_Table_Query)
        print('2.)Create a table customer.')
        print("Customer Table created successfully ")
        print(' ') 
        
        
        #3:Insert 5 customers.
        mySql_insert_query = """INSERT IGNORE INTO customer (custID, custName, zip, city, state) 
                           VALUES (%s, %s, %s, %s, %s) """
                           
        records_to_insert = [(102287, "ABRAHAM SILBERSCHATZ", 92316, "Bloomington", "California"),
                             (292364, "HENRY KORTH", 90011, "Los Angeles", "California"),
                             (154732, "CALVIN HARRIS", 11368, "New York", "New York"),
                             (128635, "MARTIN GARRIX", 75217, "Dallas", "Texas"),
                             (114427, "JAMES GOODWILL", 33125, "Miami", "Florida")]
        
        cursor = connection.cursor()
        cursor.executemany(mySql_insert_query, records_to_insert)
        connection.commit()
        print('3.)Insert 5 customers.')
        print("Customers inserted successfully into customer table")
        print(' ') 
        
        #4:Find the publisher who has published the most titles.
        query = "with count_num as(select pname, count(titles.pubID) as num_titles from publishers join titles on publishers.pubID = titles.pubID group by pname), max_num as(select max(num_titles) as max_count from count_num) select pname from count_num join max_num on num_titles = max_num.max_count"
        cursor = connection.cursor()
        cursor.execute(query)
        print('4.)Find the publisher who has published the most titles.')
        for row in cursor.fetchall():
            print(row)
        print(' ')
        
        #5:List all the authors and the total price of their published titles, in order of greatest to least total price. If an author has no published titles, they do not need to be listed.
        query = "select aName, sum(price) as total_price from authors join titleauthors on authors.auID = titleauthors.auID join titles on titleauthors.titleID = titles.titleID group by aName order by total_price desc"
        cursor = connection.cursor()
        cursor.execute(query)
        print('5:List all the authors and the total price of their published titles, in order of greatest to least total price. If an author has no published titles, they do not need to be listed.')
        for row in cursor.fetchall():
            print(row)
        print(' ')
            
        #6:Find the names of all titles which have more than 1 author who wrote it.
        query = "select title from titles join titleauthors on titles.titleID = titleauthors.titleID join authors on titleauthors.auID = authors.auID group by title having count(titleauthors.auID) > 1"
        cursor = connection.cursor()
        cursor.execute(query)
        print('6.)Find the names of all titles which have more than 1 author who wrote it.')
        for row in cursor.fetchall():
            print(row)
        print(' ')
        
        #7:Find the names of all publishers who have published a book with a price below $500, with a cover type of “Paper Back”.
        query = "select DISTINCT pname from publishers join titles on publishers.pubID = titles.pubID where cover = 'PAPER\nBACK' or cover = 'PAPER BACK' and price < 500"
        cursor = connection.cursor()
        cursor.execute(query)
        print('7.)Find the names of all publishers who have published a book with a price below $500, with a cover type of “Paper Back”.')
        for row in cursor.fetchall():
            print(row)
        print(' ')
         
        #8:Write a query to retrieve the names of all authors who have written books whose subjects contain the word “JAVA”, but have not written any books on the subject “VISUAL BASIC.NET”.
        query = "select Distinct aName from authors join titleauthors on authors.auID = titleauthors.auID join titles on titleauthors.titleID = titles.titleID join subjects on titles.subID = subjects.subID where sName like '%JAVA%' and authors.auID not in (select titleauthors.auID from titleauthors join titles on titleauthors.titleID = titles.titleID join subjects on titles.subID = subjects.subID where sName like '%VISUAL BASIC.NET%')"
        cursor = connection.cursor()
        cursor.execute(query)
        print('8.)Write a query to retrieve the names of all authors who have written books whose subjects contain the word “JAVA”, but have not written any books on the subject “VISUAL BASIC.NET”.')
        for row in cursor.fetchall():
            print(row)
        print(' ')
        
        #9:Write a query to retrieve the names of all publishers whose email addresses contains the domain “.com”.
        query = "select pname from publishers where email like '%.com%'"
        cursor = connection.cursor()
        cursor.execute(query)
        print('9.)Write a query to retrieve the names of all publishers whose email addresses contains the domain “.com”.')
        for row in cursor.fetchall():
            print(row)
        print(' ')
        
        #10:Form a query to decrease the price of all books published before 2003 by 5% and increase the price of all books published after 2004 by 15%.
        cursor = connection.cursor()
        sql_update_query = """update titles set price = price * 0.95 where pubDate < '2003-01-01'"""
        cursor.execute(sql_update_query)
        cursor = connection.cursor()
        sql_update_query2 = """update titles set price = price * 1.15 where pubDate > '2004-12-31'"""
        cursor.execute(sql_update_query2)
        connection.commit()
        query = "select * from titles"
        print('10.)Form a query to decrease the price of all books published before 2003 by 5% and increase the price of all books published after 2004 by 15%.')
        print("Prices have successfully been updated")
        cursor = connection.cursor()
        cursor.execute(query)
        for row in cursor.fetchall():
            print(row)
        print(' ')
        
except Error as e:
    print("Error while connecting to MySQL", e)
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")
