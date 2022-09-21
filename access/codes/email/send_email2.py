import yagmail
yag=yagmail.SMTP(user='ngdstu@126.com',host='smtp.126.com')
contents=["测试",
          "邮件"
          '<a href="https://makerbean.com">每颗豆网站</a>',
          yagmail.inline('课表.png'),
          '课表.png']

yag.send('ngdstu@126.com','我的邮件',contents)