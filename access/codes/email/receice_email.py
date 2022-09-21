import  zmail
server=zmail.server('ngdstu@126.com','WISPKROFZPNQLNZW')
#server=zmail.server('ngdstu@sina.com','fc59923c657385db')
mail =server.get_latest()
#zmail.show (mail)
#for mail in mails:
x=zmail.show(mail)
#print(x)
for k in ('subject', 'id', 'from', 'to', 'date', 'content_text', 'content_html', 'attachments'):
    if k != 'attachments':
        print(k.capitalize() + ' ', mail.get(k))
    else:
        _ = ''
        for idx, v in enumerate(mail['attachments']):
            _ += str(idx + 1) + '.' + 'Name:' + v[0] + ' ' + 'Size:' + str(len(v[1])) + ' '

        print(k.capitalize() + ' ', _)
print(mail['subject'])
# # print(mail['id'])
# # print(mail['from'])
# # print(mail['to'])
# # print(mail['content_text'])
# print(mail['content_html'])
#print(mail['Attachments'])
# zmail.save_attachment(mail,target_path=None,overwrite=True)
#NUQIYEXROVWPXUAU'''