from PySide2 import QtWidgets
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import *
import sys
import pymysql
import os
import  zmail
import base64
import hashlib
import time
import requests
import tkinter as tk
from tkinter import filedialog
import json

# ---------连接--------------
connect = pymysql.connect(host='localhost',   # 本地数据库
                          user='root',
                          password='1234',
                          db='mydb',
                          charset='utf8') #服务器名,账户,密码，数据库名称
cur = connect.cursor()
#关闭
def closeconn():
    # 关闭游标
    cur.close()
    # 关闭连接
    connect.close()
#查询
def select_all(sel,tab):
    select_sql = 'SELECT {} FROM {};'
    select_sql = select_sql.format(sel,tab)
    cur.execute(select_sql)
    select_datas=cur.fetchall()
    return select_datas
#条件查询
def select_condtion(sel,tab,cond,cont):
    select_sql = 'SELECT {} FROM {} WHERE {}={};'
    select_sql = select_sql.format(sel,tab,cond,cont)
    cur.execute(select_sql)
    select_datas=cur.fetchall()
    return select_datas

#插入数据
def insert(name,pwd):
    sel = select_all('max(user_id)','user_table')
    max_id=sel[0][0]+1
    insert_sql= "insert into user_table values({},'{}',{});"
    ins_sql = insert_sql.format(max_id,name, pwd)
    cur.execute(ins_sql)
    connect.commit()
#条件插入数据
def insert_con(plan_num,brand,model,guarantee,co,tel):
    sel = select_all('max(contract_id)','contract_table')
    max_id=sel[0][0]+1
   # print(max_id)
    insert_sql= "insert into contract_table values({},{},'{}','{}','{}','{}','{}');"
    ins_sql = insert_sql.format(max_id,plan_num,brand,model,guarantee,co,tel)
    cur.execute(ins_sql)
    connect.commit()
#修改数据
def update_condtion(tab,updata_field,updata_value,cond_field,cond_value):
    updata_sql='UPDATE {} SET {}="{}" WHERE {}={}'
    updata_sql = updata_sql.format(tab,updata_field,updata_value,cond_field,cond_value)
    cur.execute(updata_sql)
    connect.commit()
#删除数据
def delete(del_val):
    del_sql = "delete from contract_table where contract_id={};"
    del_sql = del_sql.format(del_val)
    # 执行SQL语句
    cur.execute(del_sql)
     # 执行完要提交
    connect.commit()
##################
"""
  手写文字识别WebAPI接口调用示例接口文档(必看):https://doc.xfyun.cn/rest_api/%E6%89%8B%E5%86%99%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB.html
  图片属性：jpg/png/bmp,最短边至少15px，最长边最大4096px,编码后大小不超过4M,识别文字语种：中英文
  webapi OCR服务参考帖子(必看)：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=39111&highlight=OCR
  (Very Important)创建完webapi应用添加服务之后一定要设置ip白名单，找到控制台--我的应用--设置ip白名单，如何设置参考：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=41891
  错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)
  @author iflytek
"""
def ocr_fuction():
    # OCR手写文字识别接口地址
    URL = "http://webapi.xfyun.cn/v1/service/v1/ocr/handwriting"
    ###需要更改内容
    # 应用APPID(必须为webapi类型应用,并开通手写文字识别服务,参考帖子如何创建一个webapi应用：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=36481)
    APPID = "5f698b5c"
    # 接口密钥(webapi类型应用开通手写文字识别后，控制台--我的应用---手写文字识别---相应服务的apikey)
    API_KEY = "22d07d46937e6e4f474a165729c6c56c"

    def getHeader():
        curTime = str(int(time.time()))
        param = "{\"language\":\""+language+"\",\"location\":\""+location+"\"}"
        paramBase64 = base64.b64encode(param.encode('utf-8'))

        m2 = hashlib.md5()
        str1 = API_KEY + curTime + str(paramBase64, 'utf-8')
        m2.update(str1.encode('utf-8'))
        checkSum = m2.hexdigest()
        # 组装http请求头
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': APPID,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header
    def getBody(filepath):
        with open(filepath, 'rb') as f:
            imgfile = f.read()
        data = {'image': str(base64.b64encode(imgfile), 'utf-8')}
        return data
    # 语种设置
    language = "cn|en"
    # 是否返回文本位置信息
    location = "true"

    window=tk.Tk()
    window.withdraw()
    file_path = filedialog.askopenfilename()
    picFilePath =file_path

    # headers=getHeader(language, location)
    r = requests.post(URL, headers=getHeader(), data=getBody(picFilePath))
    return r
def analysis_json(json_data):
    json1 =json_data.content
    result = json.loads(json1)
    dict1 = result['data']
    dict2 = dict1['block']
    # 保存提取内容
    for d in dict2:
        dict3 = d['line']
        for i in dict3:
            list2 = i['word']
            for words in list2:
                #print(words)
                word = words['content']
                if ':' in word:
                    str_write = word.split(':')
                else:
                    str_write = word.split('：')
                #print(str_write)
                if str_write[0] == "设备品牌":
                    s1 = str_write[1]
                if str_write[0] == "设备型号":
                    s2=str_write[1]
                if str_write[0] == "用期限/频次）":
                    s3 = str_write[1]
                if str_write[0] == "供货公司名称":
                    s4 = str_write[1]
                if str_write[0] == "电话":
                    s5 = str_write[1]
    return [s1,s2,s3,s4,s5]
##############################
main_win = None
register_win=None

class LoginWin:

    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/login.ui')
        self.ui.btn_login.clicked.connect(self.onLogin)
        self.ui.Button_register.clicked.connect(self.register)

    def onLogin(self):
        global main_win
        flag = 0
        # 实例化另外一个窗口
        main_win = Window_Main()
        text_une =self.ui.edt_username.text()
        text_pwd= self.ui.edt_password.text()
        sel_datas=select_all('*','user_table')
        for s in sel_datas:
            if text_une==s[1]and text_pwd==s[2]:
                flag=1
        if flag==1:
            # 显示新窗口
            main_win.ui.show()
            # 关闭自己
            self.ui.close()
            QMessageBox.information(self.ui,'成功','登录成功！')
        else:
            QMessageBox.critical(self.ui,'错误','用户名或密码错误！')
        self.ui.edt_username.clear()
        self.ui.edt_password.clear()

    def register(self):
        global register_win
        register_win = Register_Main()
        # 显示新窗口
        register_win.ui.show()
        # 关闭自己
        self.ui.close()

class Register_Main:
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/register.ui')
        self.ui.Button_user_register.clicked.connect(self.user_register)
        self.ui.pushButton_exit.clicked.connect(self.exit_pbutton)

    def user_register(self):
        text_user_name =self.ui.Edit_user_name.text()
        text_user_pw= self.ui.Edit_user_pw.text()
        text_pwdcon = self.ui.Edit_user_pwcon.text()
        if text_user_name=='' or text_user_pw=='' or text_pwdcon=='':
            print(QMessageBox.warning(self.ui,'警告','信息未填写完整！'))
        else:
            user_name = select_all('user_name','user_table')
            flag = 0
            for u in user_name:
                if u[0] == text_user_name:
                    flag = 1
            if flag == 1:
                print(QMessageBox.warning(self.ui,'警告','用户名已存在！'))
            else:
                if text_user_pw==text_pwdcon:
                    insert(text_user_name,text_user_pw)
                    print(QMessageBox.information(self.ui,'信息','注册成功！'))
                else:
                    print(QMessageBox.warning(self.ui,'警告','密码不一致！'))

    def exit_pbutton(self):
        # 显示新窗口
        wm.ui.show()
        # 关闭自己
        self.ui.close()
class Newpurchase_Main:
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/new_purchase.ui')
        self.ui.Button_extract.clicked.connect(self.extract_information)
        self.ui.Button_exit.clicked.connect(self.exit_button)
        self.ui.Button_save.clicked.connect(self.save_data)

    def extract_information(self):
        json_data = ocr_fuction()
        estr = analysis_json(json_data)
        self.ui.lineEdit_brand.setText(estr[0])
        self.ui.lineEdit_model.setText(estr[1])
        self.ui.lineEdit_guarantee.setText(estr[2])
        self.ui.lineEdit_co.setText(estr[3])
        self.ui.lineEdit_tel.setText(estr[4])
        QMessageBox.information(self.ui, '信息', '谈判信息提取成功！')
    def save_data(self):
        text_plannum= self.ui.lineEdit_plannum.text()
        text_brand = self.ui.lineEdit_brand.text()
        text_model = self.ui.lineEdit_model.text()
        text_guarantee = self.ui.lineEdit_guarantee.text()
        text_co = self.ui.lineEdit_co.text()
        text_tel = self.ui.lineEdit_tel.text()
        if text_plannum=='':
            QMessageBox.warning(self.ui, '警告', '计划号未填写！')
        else:
            insert_con(text_plannum,text_brand,text_model,text_guarantee,text_co,text_tel)
            QMessageBox.information(self.ui, '信息', '保存成功！')

    def exit_button(self):
        #global  sys_win
        #sys_win=Window_Main()
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()

class Contract_Main:
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/contract.ui')
        self.ui.Button_return.clicked.connect(self.button_return)
        self.ui.Button_manager.clicked.connect(self.button_manager)

        for i in range(len(sel_cond)):
            for j in range(len(sel_cond[i])):
                #print(sel_cond[i][j])
                s=sel_cond[i][j]
                self.ui.table_contract.setItem(i, j, QTableWidgetItem(str(s)))
    def button_return(self):
        # 显示新窗口
        main_win.ui.show()
        # 关闭自己
        self.ui.close()
    def button_manager(self):
        global  cm_win
        cm_win = Contract_Manangerment()
        # 显示新窗口
        cm_win.ui.show()
        # 关闭自己
        self.ui.close()

        pass
class Contract_Manangerment:
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/contract_mangerment.ui')
        self.ui.Button_return.clicked.connect(self.button_return)
        self.ui.Button_select.clicked.connect(self.button_select)
        self.ui.Button_delete.clicked.connect(self.button_delete)
        self.ui.Button_set.clicked.connect(self.button_set)
    def button_select(self):
        cont=self.ui.Edit_contractid.text()
        sel=select_condtion('*','contract_table','contract_id',cont)
        self.ui.Edit_plannum.setText(str(sel[0][1]))
        self.ui.Edit_brand.setText(str(sel[0][2]))
        self.ui.Edit_model.setText(sel[0][3])
        self.ui.Edit_guarantee.setText(sel[0][4])
        self.ui.Edit_co.setText(sel[0][5])
        self.ui.Edit_tel.setText(sel[0][6])
    def button_delete(self):
        cont = self.ui.Edit_contractid.text()
        delete(cont)
        QMessageBox.information(self.ui, '信息', '删除成功！')
    def button_set(self):
        cont = self.ui.Edit_contractid.text()
        text_plannum= self.ui.Edit_plannum.text()
        text_brand = self.ui.Edit_brand.text()
        text_model = self.ui.Edit_model.text()
        text_guarantee = self.ui.Edit_guarantee.text()
        text_co = self.ui.Edit_co.text()
        text_tel = self.ui.Edit_tel.text()

        update_condtion('contract_table','plan_num',text_plannum,'contract_id',cont)
        update_condtion('contract_table','brand',text_brand, 'contract_id', cont)
        update_condtion('contract_table', 'model',text_model, 'contract_id', cont)
        update_condtion('contract_table', 'guarantee',text_guarantee, 'contract_id', cont)
        update_condtion('contract_table', 'co',text_co, 'contract_id', cont)
        update_condtion('contract_table', 'tel', text_tel, 'contract_id', cont)
        QMessageBox.information(self.ui, '信息', '修改成功！')

    def button_return(self):
        global  c_win
        c_win=Contract_Main()
        # 显示新窗口
        c_win.ui.show()
        # 关闭自己
        self.ui.close()

class Window_Main:
    def __init__(self):
        super().__init__()
        self.ui = QUiLoader().load('ui/system.ui')
        self.ui.exit_Button.clicked.connect(self.exit_button)
        self.ui.Button_extract_att.clicked.connect(self.extract_attcahment)
        self.ui.Button_open_file.clicked.connect(self.open_file)
        self.ui.Button_newpurchase.clicked.connect(self.new_purchase)
        self.ui.Button_select.clicked.connect(self.select_conditon)

    def select_conditon(self):
        global sel_cond ,contract_win
        text_option = self.ui.Edit_option.text()
        text_option='plan_num'
        text_content = self.ui.Edit_content.text()
        sel_cond = select_condtion('*', 'contract_table', text_option,text_content)
        contract_win=Contract_Main()
        # 显示新窗口
        contract_win.ui.show()
        # 关闭自己
        self.ui.close()
    def exit_button(self):
        # 显示新窗口
        wm.ui.show()
        # 关闭自己
        self.ui.close()
    def extract_attcahment(self):
        email = 'ngdstu@126.com'
        pwd = 'AIYBLCJXVGHCSBHQ'
        # sub='邮箱'
        # email=input("请输入你的邮箱账户：")
        # pwd=input("请输入你的授权密码：")
        # sub = input("请输入关键字：")
        # email= self.ui.lineEdit.text()
        # pwd = self.ui.lineEdit_2.text()
        #邮箱主题
        plan_num = self.ui.Edit_plan_num.text()
        if plan_num=='':
            QMessageBox.warning(self.ui, '错误', '未填写计划号')
        else:
            server = zmail.server(email, pwd)
            mails = server.get_mails(subject=plan_num)
            # file = "D:\\供货商资料"
            file = os.path.dirname(os.path.realpath(sys.argv[0]))
            file = file + "\\供货商资料"
            files = file + '\\' + plan_num
            # print(files)
            isexists=os.path.exists(files)
            if not isexists:
                os.makedirs(files)
            for mail in mails:
                # zmail.show(mail)
                zmail.save_attachment(mail, target_path=files, overwrite=True)
            # print("附件已提取完毕")
            QMessageBox.information(self.ui, '提取结果', '附件已提取完毕')
    def open_file(self):
        plan_num = self.ui.Edit_plan_num.text()
        if plan_num=='':
            QMessageBox.warning(self.ui, '错误', '未填写计划号')
        else:
            file = os.path.dirname(os.path.realpath(sys.argv[0]))
            file = file + "\\供货商资料"
            files = file + '\\' + plan_num
            isexists = os.path.exists(files)
            if isexists:
                os.startfile(files)
                QMessageBox.information(self.ui, '成功', '文件打开成功')
            else:
                QMessageBox.information(self.ui, '失败', '未找到文件')
    def new_purchase(self):
        global newpurchase_win
        newpurchase_win = Newpurchase_Main()
        #print('打开界面')
        # 显示新窗口
        newpurchase_win.ui.show()
        # 关闭自己
        self.ui.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    wm = LoginWin()
    wm.ui.show()
    sys.exit(app.exec_())
    closeconn()