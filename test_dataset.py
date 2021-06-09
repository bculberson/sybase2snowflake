import pyodbc
import string
import random
from random import randint

conn = pyodbc.connect("DSN=DEVART_ASE", timeout=2)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute("disk init name='t1', physname='/opt/sybase/external_data/Test.dat', skip_alloc='true', size='25G'")
cursor.execute("disk init name='t2', physname='/opt/sybase/external_data/TestLog.dat', skip_alloc='true', size='10G'")
cursor.execute("create database testdb on t1='25g' log on t2='10g'")
cursor.execute("sp_dboption testdb, 'ddl in tran', 'true'")
cursor.execute("CREATE TABLE testdb.dbo.TEST (id INT IDENTITY UNIQUE, data VARCHAR(255))")
cursor.close()

records = 0
sql = "INSERT into testdb.dbo.TEST (data) values (?)"
print("Inserting test data")
while True:
    data = ''.join(random.choice(string.printable) for x in range(randint(0, 254)))
    cursor = conn.cursor()
    cursor.execute(sql, data)
    cursor.close()
    records = records + 1
    if records % 1000 == 0:
      print(f"{records} test records created.")
