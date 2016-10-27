#!/usr/bin/env python
# -*- coding:utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


def email(email_list, content, subject="奇谈怪论-用户注册"):
    print("我执行了!!!")
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = formataddr(["奇谈怪论", '15711143512@126.com'])
    msg['Subject'] = subject

    server = smtplib.SMTP("smtp.126.com", 25)
    server.login("15711143512@126.com", "tms320c240")
    server.sendmail('15711143512@126.com', email_list, msg.as_string())
    server.quit()

