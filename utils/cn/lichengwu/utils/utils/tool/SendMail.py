__author__ = 'zuojing'

import smtplib
from email.mime.multipart import MIMEMultipart
import sys

if __name__ == '__main__':

    user = sys.argv[0]
    context = sys.argv[1]
    attach_file = sys.argv[2]

    smtp = smtplib.SMTP_SSL("smtp.alibaba-inc.com", "465")
    smtp.ehlo()
    smtp.login('chengwu.lcw@alibaba-inc.com', 'xxxxx')
    msg = MIMEMultipart()
    msg['Subject'] = 'tisd1111as'
    msg['From'] = 'chengwu.lcw@taobao.com'
    msg['To'] = 'chengwu.lcw@taobao.com'
    smtp.sendmail('chengwu.lcw@taobao.com', 'chengwu.lcw@taobao.com',
                  msg.as_string())
    smtp.quit()


