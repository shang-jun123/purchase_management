import pymysql
# ---------连接--------------
connect = pymysql.connect(host='localhost',   # 本地数据库
                          user='root',
                          password='1234',
                          db='mydb',
                          charset='utf8') #服务器名,账户,密码，数据库名称
cur = connect.cursor()

def insert(name,pwd):
    #print(name,pwd)
    sel = select_all('max(user_id)','user_table')
    max_id=sel[0][0]+1
    insert_sql= "insert into user_table values({},'{}',{});"
    ins_sql = insert_sql.format(max_id,name, pwd)
    cur.execute(ins_sql)
    connect.commit()
def select_all(sel,tab):
    select_sql = 'SELECT {} FROM {};'
    select_sql = select_sql.format(sel,tab)
    cur.execute(select_sql)
    select_datas=cur.fetchall()
    return select_datas
def closeconn():
    # 关闭游标
    cur.close()
    # 关闭连接
    connect.close()
def insert_con(plan_num,brand,model,guarantee,co,tel):
    sel = select_all('max(user_id)','user_table')
    max_id=sel[0][0]+1
    insert_sql= "insert into contract_table values({},{},'{}','{}','{}','{}','{}');"
    ins_sql = insert_sql.format(max_id,plan_num,brand,model,guarantee,co,tel)
    cur.execute(ins_sql)
    connect.commit()
def select_condtion(sel,tab,cond,cont):
    select_sql = 'SELECT {} FROM {} WHERE {}={};'
    select_sql = select_sql.format(sel,tab,cond,cont)
    cur.execute(select_sql)
    select_datas=cur.fetchall()
    return select_datas
def update_condtion(tab,updata_field,updata_value,cond_field,cond_value):
    updata_sql='UPDATE {} SET {}="{}" WHERE {}={}'
    updata_sql = updata_sql.format(tab,updata_field,updata_value,cond_field,cond_value)
    cur.execute(updata_sql)
    connect.commit()
def delete(del_val):
    del_sql = "delete from contract_table where contract_id={};"
    del_sql = del_sql.format(del_val)
    # 执行SQL语句
    cur.execute(del_sql)
     # 执行完要提交
    connect.commit()
#insert_con(1,'Dell','TS-300','十年','南工大','13814121588')
#insert('root2',123)
#sel=select_condtion('*','contract_table','plan_num','1')
#update_condtion('contract_table','plan_num',1,'contract_id','4')
delete(6)
closeconn()