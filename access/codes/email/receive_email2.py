import  zmail
import  os
import sys
from tqdm import tqdm

basepath= os.path.dirname(os.path.realpath(sys.argv[0]))
#邮箱账户与授权码
###需要更改
# email='ngdstu@126.com'
# pwd='WISPKROFZPNQLNZW'
email='glyywcy@163.com'
pwd='JNYPOOTGXOUKWCEN'
#
# email='ngdstu@126.com'
# pwd='WISPKROFZPNQLNZW'

#参数传递vba-python
# with open(basepath+'\plan.txt',encoding="utf-8") as read_file:
#     content=read_file.read()

# sub=content.strip()
sub="008"
server=zmail.server(email,pwd)
mails = server.get_mails(subject=sub)
file=basepath+"\\"+"供货商资料"
file1=file+"\\"+sub
if not  os.path.exists(file1):
    os.makedirs(file1)
for mail in mails:
    for k in ('subject',  'attachments'): 
        if k != 'attachments':
            #print(k.capitalize() + ' ', mail.get(k))
            #mail.get(k)为邮箱主题
            #print(mail.get(k))
            file2 = file1 + "\\" + mail.get(k)
            if mail.get('attachments'):
                if not os.path.exists(file2):
                    os.makedirs(file2)
            else:
                print("主题为“"+mail.get(k)+"”的附件未提取成功\n")

        else:
            _ = ''
            # for idx, v in enumerate(mail['attachments']):
            #     _ += str(idx + 1) + '.' + 'Name:' + v[0] + ' ' + 'Size:' + str(len(v[1])) + ' '
            #     print(v[0])
            #
            #     #print(str(round(len(v[1])/1024/1024,2))+"MB")
            # #print(k.capitalize() + ' ', _)
            #     if  os.path.exists(file2):
            #         raise FileExistsError("{} already exists, set overwrite to True to avoid this error.")
            #     with open(file2, 'wb') as f:
            #         f.write(v)
            for name, raw in mail['attachments']:
                file_path = os.path.join(file2, name)
                print(file_path)
                total=len(raw)

                # if os.path.exists(file_path):
                #     print("已经存在文件")
                #     #raise FileExistsError("{} already exists, set overwrite to True to avoid this error.")
                # else:
                #     #os.makedirs(file2)
                #     # with open(file_path, 'wb') as file, tqdm(
                #     #         desc=file_path,
                #     #         total=total,
                #     #         unit='iB',
                #     #         unit_scale=True,
                #     #         unit_divisor=1024,
                #     # ) as bar:
                #     #     #for data in resp.iter_content(chunk_size=1024):
                #     #         size = file.write(raw)
                #     #         bar.update(size)
                #     with open(file_path, 'wb') as f:
                #         f.write(raw)
    zmail.save_attachment(mail,target_path=file_path,overwrite=True)

result_path=basepath+"\\plan.txt"
result_file=open(result_path,'a+')
result_file.truncate(0)



