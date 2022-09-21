# -*- coding: utf-8 -*-
from urllib import parse
import base64
import hashlib
import time
import requests
"""
  手写文字识别WebAPI接口调用示例接口文档(必看):https://doc.xfyun.cn/rest_api/%E6%89%8B%E5%86%99%E6%96%87%E5%AD%97%E8%AF%86%E5%88%AB.html
  图片属性：jpg/png/bmp,最短边至少15px，最长边最大4096px,编码后大小不超过4M,识别文字语种：中英文
  webapi OCR服务参考帖子(必看)：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=39111&highlight=OCR
  (Very Important)创建完webapi应用添加服务之后一定要设置ip白名单，找到控制台--我的应用--设置ip白名单，如何设置参考：http://bbs.xfyun.cn/forum.php?mod=viewthread&tid=41891
  错误码链接：https://www.xfyun.cn/document/error-code (code返回错误码时必看)
  @author iflytek
"""
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

# 图片上传接口地址
import cv2
import tkinter as tk
from tkinter import filedialog
import os
import sys
import numpy as np

window=tk.Tk()
window.withdraw()
file_path = filedialog.askopenfilename()


#file_name = os.path.basename(file_path)
basepath= os.path.dirname(os.path.realpath(sys.argv[0]))
#以上这句获取路径就正确了。
#print(file_path)

#参数传递
file_path1=basepath+"\\picture"
with open(basepath+'\plan.txt') as read_file:
    content=read_file.read()
#sub=input("请输入关键字：") 
sub=content.strip()
x=sub

file_path3=file_path1+'\\'+x
if  os.path.exists(file_path3)==False:
    os.mkdir(file_path3)

picFilePath=file_path
img=cv2.imread(picFilePath)
picFilePath =file_path

# headers=getHeader(language, location)
r = requests.post(URL, headers=getHeader(), data=getBody(picFilePath))
#格式解析
import json
json1=r.content
result=json.loads(json1)
dict1=result['data']
dict2=dict1['block']

#清空上一次的提取内容
result_path=basepath+"\\test.txt"
result_file=open(result_path,'a+')
result_file.truncate(0)

#保存提取内容
for d in dict2:
    dict3=d['line']
    for i in dict3:
        list2=i['word']
        for words in list2:
            #print(words)
            word=words['content']
            if ':'in word:
                str_write = word.split(':')
            else:
                str_write=word.split('：')
            #print(str_write)
            if str_write[0] == "设备型号":
                result_file.write(str_write[1]  + ",")
            if str_write[0] == "设备品牌":
                result_file.write(str_write[1] + ",")
            if str_write[0] == "供货公司名称":
                y=str_write[1]
                result_file.write(str_write[1]  + ",")
            if str_write[0]  == "电话":
                result_file.write(str_write[1] + ",")
            if str_write[0]  == "用期限/频次）":
                result_file.write(str_write[1]  + ",")
result_file.write(x+'\n')
result_file.close()
#保存图片
file_name=y+'.jpg'
file_path2=file_path3+'\\'+file_name
img = cv2.imdecode(np.fromfile(file_path,dtype=np.uint8),-1)
cv2.imencode('.jpg', img)[1].tofile(file_path2)
#print(file_path3)
#清空文本文件
result_path=basepath+"\\plan.txt"
result_file=open(result_path,'a+')
result_file.truncate(0)
result_file.close()

