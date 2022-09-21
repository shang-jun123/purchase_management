import pymysql
# ---------连接--------------
connect = pymysql.connect(host='localhost',   # 本地数据库
                          user='root',
                          password='1234',
                          db='mydb',
                          charset='utf8') #服务器名,账户,密码，数据库名称
cur = connect.cursor()

print(cur)
try:
    create_sqli = "create table sys (id int, name varchar(30),phone int);"
    cur.execute(create_sqli)
except Exception as e:
    print("创建数据表失败:", e)
else:
    print("创建数据表成功;")

try:
    insert_sqli = "insert into sys values(001, 'xiaoming',123456789);"
    cur.execute(insert_sqli)
except Exception as e:
    print("插入数据失败:", e)
else:
    # 如果是插入数据， 一定要提交数据， 不然数据库中找不到要插入的数据;

    print("插入数据成功;")

print('SELECT * FROM user_table;')
select_sql='SELECT * FROM user_table;'
select=cur.execute(select_sql)
for r in cur:
    print(r)
maxid='SELECT max(id) FROM user_table;'
maxid_select=cur.execute(maxid)