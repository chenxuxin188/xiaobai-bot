import httpx
import time
import traceback
import re
import asyncio
from bs4 import BeautifulSoup

url = 'http://book.sfacg.com/Novel/{}/MainIndex/'
freeReg = r'\/Novel\/(?P<book>[0-9]*)\/(?P<volume>[0-9]*)\/(?P<chapter>[0-9]*)\/'
vipReg = r'\/vip\/c\/(?P<chapter>[0-9]*)\/'

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36 Edg/86.0.622.38","Host": "book.sfacg.com"}

async def request(url, header):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers = header, timeout=30)
            return response
        except:
            print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[HTTP]' + url + '\n' + traceback.format_exc())
            return False

async def checkNovel(book):
    r = False
    t = 0
    while t < 3 and not r:
        t += 1
        h = header
        h.update({"Referer":'http://book.sfacg.com/Novel/{}/'.format(book)})
        r = await request(url.format(book), h)
        await asyncio.sleep(1)
    if r:
        m = 0
        result = {'success': True}
        p = BeautifulSoup(r.text, 'html.parser')

        title = p.find_all('title')
        if title[0].text == "出错了":
            result.update({'success': False})
            return result
        free = p.find_all('a', href=re.compile(freeReg))
        vip = p.find_all('a', href=re.compile(vipReg))
        freeList = []
        for f in free:
            ff = re.match(freeReg, f['href'])
            chapter = int(ff.group('chapter'))
            if chapter > m:
                m = chapter
            freeList.append([chapter,int(ff.group('volume'))])
        result.update({'free':freeList})
        vipList = []
        for f in vip:
            ff = re.match(vipReg, f['href'])
            chapter = int(ff.group('chapter'))
            if chapter > m:
                m = chapter
            vipList.append(chapter)
        result.update({'vip':vipList})
        result.update({'max':m})
        return result
    else:
        return {'success': False}

async def getChapters(free, vip, book, name):
    freeurl = 'http://book.sfacg.com/Novel/{}/{}/{}/'
    vipurl = 'https://book.sfacg.com/vip/c/{}/'

    countReg = r'字数：(?P<count>[0-9]+)'

    updates = []

    for f in free:
        await asyncio.sleep(1)
        r = False
        c = 0
        while not r and c < 3:
            c += 1
            h = header
            h.update({"Referer":'http://book.sfacg.com/Novel/{}/MainIndex/'.format(book)})
            r = await request(freeurl.format(book,f[1],f[0]), header)
        if not r:
            continue
        p = BeautifulSoup(r.text, 'html.parser')
        title = p.find('h1', class_='article-title').text
        count = int(re.match(countReg, p.find(text=re.compile(countReg))).group('count'))
        preview = p.find(id='ChapterBody').text[:90] + '...'
        text= freeurl.format(book,f[1],f[0]) + '\n更新了喵更新了喵~~！！\n书名：'+ name + '\n' + title + '\n'+ preview + '\n字数：' + str(count) + "\n" + "评价："
        s = ''
        if count >= 4000:
            s = '哇！更新了好多喵！太好了喵！'
        elif count >= 3000:
            s = '哇！要是每天都更新这么多就好了喵！'
        elif count >= 2000:
            s = '不错喵！继续努力喵！'
        else:
            s = '你更新了个锤子喵？？？'

        text += s

        updates.append(text)

    for v in vip:
        await asyncio.sleep(1)
        r = False
        c = 0
        while not r and c < 3:
            c += 1
            r = await request(vipurl.format(v), header)
        if not r:
            continue
        p = BeautifulSoup(r.text, 'html.parser')
        title = p.find('h1', class_='article-title').text
        count = int(re.match(countReg, p.find(text=re.compile(countReg))).group('count'))
        preview = p.find(id='ChapterBody').text

        text = vipurl.format(v) + '\n更新了喵更新了喵~~！！\n书名：'+ name + '\n' + title + '\n'+ preview + '\n字数：' + str(count) + "\n" + "评价："
        
        s = ''
        if count >= 4000:
            s = '哇！更新了好多喵！太好了喵！'
        elif count >= 3000:
            s = '哇！要是每天都更新这么多就好了喵！'
        elif count >= 2000:
            s = '不错喵！继续努力喵！'
        else:
            s = '你更新了个锤子喵？？？'

        text += s

        updates.append(text)

    return updates



async def getNovel(book):
    r = None
    t = 0
    while t < 3 and not r:
        t += 1
        h = header
        h.update({"Referer":'http://book.sfacg.com/Novel/{}/'.format(book)})
        r = await request(url.format(book), header)
    if r:
        m = 0
        result = {}
        p = BeautifulSoup(r.text, 'html.parser')
        title = p.find_all('title')
        if title[0].text == "出错了":
            result.update({'success': False, 'title': "出错了", "chapter":99999999})
            return result
        titleReg = r'^(?P<name>.*)章节列表\|.*\|.*\|.*网站$'
        n=re.match(titleReg,title[0].text).group('name')
        result.update({'title':n})
        free = p.find_all('a', href=re.compile(freeReg))
        vip = p.find_all('a', href=re.compile(vipReg))
        for f in free:
            ff = re.match(freeReg, f['href'])
            chapter = int(ff.group('chapter'))
            if chapter > m:
                m = chapter
        for f in vip:
            ff = re.match(vipReg, f['href'])
            chapter = int(ff.group('chapter'))
            if chapter > m:
                m = chapter
        result.update({'success': True, 'chapter':m})
        return result
    else:
        return {'success': False, 'title': "失败", "chapter":99999999}
