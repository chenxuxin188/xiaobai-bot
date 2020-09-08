import re
import os

def escape(ss, insideCQ = False):
    s = re.sub(r'\&', '&amp;', ss)
    s = re.sub(r'\[', '&#91;', s)
    s = re.sub(r'\]', '&#93;', s)
    if(insideCQ):
        s = re.sub(r'\,', '&#44;', s)
        s = re.sub(r'(\ud83c[\udf00-\udfff])|(\ud83d[\udc00-\ude4f\ude80-\udeff])|[\u2600-\u2B55]', ' ', s)
    return s


def CQparse(code):
    CQg = re.search(r'\[CQ:([a-z]+?)((,([a-z]+)=([^,[\]]*))+)\]', code)
    p = { 'CQtype': CQg.group(1) }
    subs = re.findall(r',([a-z]+?)=([^,[\]]*)', CQg.group(2))
    for x in subs:
        p.update({x[0]: x[1]})
    return p

def findCQcodes(message):
    codes = re.findall(r'\[CQ[^\]]*\]', message)
    return codes
    
def removeCQcodes(message):
    return re.sub(r'\[CQ[^\]]*\]', '', message)

def img(file):
    return '[CQ:image,file={}]'.format(escape(file, True))

def img64(base64):
    return '[CQ:image,file=base64://{}]'.format(base64)

def record64(base64):
    return '[CQ:record,file=base64://{}]'.format(base64)