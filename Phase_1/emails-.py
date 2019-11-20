
from xml.dom.minidom import parse
import xml.dom.minidom


def add(s, lst, row, tag):
    for x in s.split(','):
        lst.append('%s-%s:%s' % (tag, x.lower(), row))

# 使用minidom解析器打开 XML 文档
DOMTree = xml.dom.minidom.parse("1k.xml")
collection = DOMTree.documentElement

movies = collection.getElementsByTagName("mail")

lst = []

for movie in movies:
    row = movie.getElementsByTagName('row')[0].firstChild.data
    try:
        from_str = movie.getElementsByTagName('from')[0].firstChild.data
        add(from_str, lst, row, 'from')
    except:
        from_str = ''
    try:
        to_str = movie.getElementsByTagName('to')[0].firstChild.data
        add(to_str, lst, row, 'to')
    except:
        to_str = ''
    try:
        cc_str = movie.getElementsByTagName('cc')[0].firstChild.data
        add(cc_str, lst, row, 'cc')
    except:
        cc_str = ''
    try:
        bcc_str = movie.getElementsByTagName('bcc')[0].firstChild.data
        add(bcc_str, lst, row, 'bcc')
    except:
        bcc_str = ''


fp = open('out.txt', 'w')
for item in lst:
    fp.write(item + '\n')
fp.close()



