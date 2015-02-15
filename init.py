# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>
import urllib2
from cn2dig import cn2dig
from BeautifulSoup import BeautifulSoup
import re
path = '/home/hyde/xiaoshuo/last.txt'

html = urllib2.urlopen('http://tieba.baidu.com/f?kw=%CD%EA%C3%C0%CA%C0%BD%E7%D0%A1%CB%B5&fr=ala0')
soup = BeautifulSoup(html)
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
        
fp = open(path,'w')
fp.write(str(max(content)))
fp.close()
