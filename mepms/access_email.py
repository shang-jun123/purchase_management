import  zmail
import  os
import sys

basepath= os.path.dirname(os.path.realpath(sys.argv[0]))
#邮箱账户与授权码
###需要更改
email='glyywcy@163.com'
pwd='JNYPOOTGXOUKWCEN'
# email='ngdstu@126.com'
# pwd='WISPKROFZPNQLNZW'

#参数传递vba-python
with open(basepath+'\plan.txt',encoding="utf-8") as read_file:
    content=read_file.read()

sub=content.strip()
#sub="007"
server=zmail.server(email,pwd)
mails = server.get_mails(subject=sub)
#file_plan=basepath+"\\"+"供货商资料"+"\\"+sub
file_plan = os.path.join(basepath,"供货商资料",sub)
if not os.path.exists(file_plan):
    os.makedirs(file_plan)
file_co=""
if len(mails)==0:
    print("不存在附件")

for mail in mails:
    for k in ('subject',  'attachments'):
        if k != 'attachments':
            #print(k.capitalize() + ' ', mail.get(k))
            #mail.get(k)为邮箱主题
            #print(mail.get(k))
            file_co = os.path.join(file_plan, str.strip(mail.get(k)))
            if mail.get('attachments'):
                if not os.path.exists(file_co):
                    os.makedirs(file_co)
            else:
                print("\n主题为“"+mail.get(k)+"”的附件未提取成功")
        else:
            for name, raw in mail['attachments']:
                size = 0
                file_path = os.path.join(file_co, name)
                #print(file_path)
                overwrite = True
                if not  os.path.exists(file_path):
                    total = len(raw)
                    print('\n' + name + '\n' + str(round(total / 1024 / 1024, 2)) + "MB")
                    #raise FileExistsError("{} already exists, set overwrite to True to avoid this error.")
                    with open(file_path, 'wb') as f:
                        f.write(raw)
                        size+=len(raw)
                        print('\r'+'[下载进度]：%s%.2f%%' % ('>'*int(size*50/total),float(size/total*100)),end='\n')
    #zmail.save_attachment(mail,target_path=file_co,overwrite=True)
result_path=basepath+"\\plan.txt"
result_file=open(result_path,'a+')
result_file.truncate(0)



