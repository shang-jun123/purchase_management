from imbox import Imbox
import keyring

password=keyring.get_password('yagmail','ngdstu@sina.com')
print (password)
#8e40d2b3b963b136
with Imbox('pop.sina.com','ngdstu@sina.com','8e40d2b3b963b136',ssl=True) as imbox:
#Imbox(IMAP服务器地址,邮箱地址(用户名),密码,是否开启SSL加密)
    all_inbox_messages=imbox.messages()
    for uid,message in all_inbox_messages:
        print(message.subject)
        print(message.body['plain'])


#NVMOIBBJWSYJXRQZ