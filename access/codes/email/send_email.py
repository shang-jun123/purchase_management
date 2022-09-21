import smtplib
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header



host_server = "smtp.126.com"
sender = "ngdstu@126.com"
pwd = "NVMOIBBJWSYJXRQZ"
receiver = "ngdstu@sina.com"

mail_title = "python办公自动化测试"
mail_content = "你好,<p>这是使用Pyhon登录sina邮箱发送HTML的邮件:</p><p><a \
href='https://www.python.org'>Python</a></p>"

msg = MIMEMultipart()
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender
msg["To"] = Header("测试邮箱", 'utf-8')
#msg["To"] =receiver
msg.attach(MIMEText(mail_content, 'html', 'utf-8'))

attachment=MIMEApplication(open(r'C:\Users\Admin\Desktop\课表.png','rb').read())
attachment.add_header('Content-Disposition','attachement',filename='课表.png')
msg.attach(attachment)

try:
    smtp = SMTP_SSL(host_server)
    smtp.set_debuglevel(0)
    smtp.ehlo(host_server)

    smtp.login(sender, pwd)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
    print("邮件发送成功")
except smtplib.SMTPException:
    print("无法发送邮件")









