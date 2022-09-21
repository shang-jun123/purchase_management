import os
basepath = os.path.dirname(__file__)  # 当前文件所在路径
print(basepath)

file_path1=basepath+"\\医疗设备采购"
with open(r'D:\git\access\医疗设备采购\test.txt') as read_file:
    content=read_file.read()
sub="008"
file_plan=basepath+"\\"+"供货商资料"+"\\"+sub

#sub=input("请输入关键字：")
print(content)
sub=content.strip()
print(sub)
print(len(content))
if len(content)>0:
    print('提取完毕D:\git\access\codes\email\open_file.py')