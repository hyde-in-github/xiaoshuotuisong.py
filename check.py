# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import urllib2
from BeautifulSoup import BeautifulSoup
from cn2dig import cn2dig
import re

# <codecell>

html = urllib2.urlopen('http://tieba.baidu.com/f?kw=%CD%EA%C3%C0%CA%C0%BD%E7%D0%A1%CB%B5&fr=ala0')
soup = BeautifulSoup(html)

def send(content):
    import smtplib
    from email.Message import Message
    from time import sleep

    smtpserver='smtp.126.com'
    username='xiaoshuotuisong@126.com'
    password='xiaoshuo'
    from_addr='xiaoshuotuisong@126.com'
    to_addr='451588059@qq.com'
    #cc_addr='1241224798@qq.com'

    sm=smtplib.SMTP(smtpserver,port=25,timeout=20)
    sm.set_debuglevel(1)
    sm.ehlo()
    sm.starttls()
    sm.ehlo()
    sm.login(username,password)
    for i in sorted(content.viewkeys()):
        message=Message()
        message['Subject']= content[i]['title']
        message['From']=from_addr
        message['To']=to_addr
        #message['Cc']=cc_addr
        message.set_payload(content[i]['text'])
        msg=message.as_string()
        sm.sendmail(from_addr,to_addr,msg)
        sleep(5)
    sm.quit()

# <codecell>

pattern1 = re.compile('href=".*?"')
pattern2 = re.compile('title=".*?"')
pattern3 = re.compile('".*?"')
pattern4 = re.compile(u'第.*?章')
pattern5 = re.compile('>\D+?\S+?\D+?<')
pattern6 = re.compile('>\S+?<')

# <codecell>

content = {}
for i in range(3):
    href = pattern1.findall(str(soup.findAll('ul')[3].findAll('li')[i].findAll('a')[0]))[0].split('href=')[1].split('"')[1]
    title = pattern2.findall(str(soup.findAll('ul')[3].findAll('li')[i].findAll('a')[0]))[0].split('title=')[1].split('"')[1]
    try:
        No = cn2dig(pattern4.findall(unicode(title,'utf-8'))[0].split(u'第')[1].split(u'章')[0])
        content[No] = {}
        content[No]['title'] = title
        content[No]['href'] = href
    except:
        None

# <codecell>

fp = open('/home/hyde/xiaoshuo/last.txt','r')
last = int(fp.read())
fp.close()

# <codecell>

if max(content) > last:
    fp = open('/home/hyde/xiaoshuo/last.txt','w')
    fp.write(str(max(content)))
    fp.close()

    for i in content:
        href = content[i]['href']
        string = ''
        html = urllib2.urlopen('http://tieba.baidu.com' + href)
        soup1 = BeautifulSoup(html)
        string += '\xe3\x80\x80\xe3\x80\x80' + pattern5.findall(str(soup1.findAll('cc')[0].findAll('div')[0]))[0].replace(' ', '').replace('\xe3\x80\x80', '').replace('>', '').replace('<', '') + '\n'
        for j in pattern6.findall(str(soup1.findAll('cc')[0].findAll('div')[0])):
            string += '\xe3\x80\x80\xe3\x80\x80' + j.replace('\xe3\x80\x80', '').replace('>', '').replace('<', '') + '\n'
            content[No]['text'] = string
    send(content)xiO

# <codecell>

