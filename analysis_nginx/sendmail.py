#!/usr/bin/python
#coding=utf-8
#author=little boss

import time
import pandas as pd
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

print (time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
data_log = pd.read_table(r'/data/auto_log/total_utl.txt',sep='\t',names=['response_time','url'])

nginx_url = data_log[data_log.isnull()!= 'True']
nginx_url_reduce = nginx_url[nginx_url['response_time'] != '-']
nginx_url_reduce['url'] = nginx_url_reduce['url'].apply(lambda x:x.split('?')[0])
total = pd.DataFrame(nginx_url_reduce['url'].value_counts())


nginx_url_reduce['response_time'] = nginx_url_reduce['response_time'].apply(lambda x:x.strip(','))
nginx_url_reduce['response_time'] = nginx_url_reduce['response_time'].apply(lambda x:float(x))

great = pd.DataFrame(nginx_url_reduce[nginx_url_reduce['response_time'] > 1.0]['url'].value_counts())


end_url1 = total.merge(great,left_index=True,right_index=True)
end_url1['ratio'] = end_url1['url_y'] / end_url1['url_x']
end_url1 = end_url1.sort_values('ratio',ascending=False)
#end_url2 = end_url1.round(2)
end_url1['ratio'] = end_url1['ratio'].map(lambda x:format(x,'.2%'))
end_url = end_url1.rename(columns={'url_x':'总数','url_y':'大于1s数量','ratio':'占比%'})
end_url.index.name = '接口'
end_url.to_html("url.html")
print("dataframe exec complete,result is ok")


with open('/data/auto_log/url.html','r') as f:
    file = f.read()
    f.close()
    print("write html file complete,result is fine")

mail_info = {
 "from": "xxx@xxx.com",
 "to": "xxx@xxx.com",
 "hostname": "smtp.xxx.xx.com",
 "username": "xxx@xxx.com",
 "password": "xxxx",
 "mail_subject": "接口响应时间大于1s详情",
 "mail_text": file,
 "mail_encoding": "gb2312"
}

if __name__ == '__main__':
#这里使用SMTP_SSL就是默认使用465端口
    smtp = SMTP_SSL(mail_info["hostname"])
    smtp.set_debuglevel(0)
                    
    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])

    msg = MIMEText(mail_info["mail_text"], "html", mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["from"] = mail_info["from"]
    msg["to"] = mail_info["to"]
                                                
    smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())

    smtp.quit()
    print("send mail complete ,result is nice")
