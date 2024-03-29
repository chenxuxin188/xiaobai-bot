import httpx
import time
import traceback
import re
import json

durl = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={}&offset_dynamic_id=0&need_top=0'
lurl = 'http://api.live.bilibili.com/bili/living_v2/{}'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41"}

table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
	tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608

def enc(x):
    try:
        x=(x^xor)+add
        r=list('BV1  4 1 7  ')
        for i in range(6):
            r[s[i]]=table[x//58**i%58]
        return ''.join(r)
    except:
        return False

async def request(url, headers, cookies):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers = headers, cookies = cookies, timeout=30)
            return response
        except:
            print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[HTTP]' + traceback.format_exc())
            return False

async def getLive(uid, SESSDATA, CSRF):
    result = False
    count = 0
    while not result and count < 3:
        cookies = httpx.Cookies()
        cookies.set("SESSDATA", SESSDATA, domain=".bilibili.com")
        cookies.set("bili_jct", CSRF, domain=".bilibili.com")
        count += 1
        result = await request(lurl.format(uid), header, cookies)
    if not result:
        return False
    code = json.loads(result.content).get('code')
    msg = json.loads(result.content).get('message')
    if code != 0:
        print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[直播]' + 'Code:{}  Msg:{}'.format(code,msg))
        return False
    
    data = json.loads(result.content).get('data')
    if not data:
        return False
    if data.get('status') != 1:
        return False
    else:
        return data.get('url')


async def getCards(uid, SESSDATA, CSRF):
    avReg = r'^bilibili\:\/\/video\/(?P<av>[0-9]+)\/\?.*?'
    result = False
    count = 0
    while not result and count < 3:
        count += 1
        cookies = httpx.Cookies()
        cookies.set("SESSDATA", SESSDATA, domain=".bilibili.com")
        cookies.set("bili_jct", CSRF, domain=".bilibili.com")
        hh = header
        hh.update({"origin":"https://space.bilibili.com", "referer":"https://space.bilibili.com/"})
        result = await request(durl.format(uid), hh, cookies)
    if not result:
        print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[动态]' + '获取失败')
        return False
    code = json.loads(result.content).get('code')
    msg = json.loads(result.content).get('message')
    if code != 0:
        print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[动态]' + 'Code:{}  Msg:{}'.format(code,msg))
        return False
    data = json.loads(result.content).get('data')
    if not data:
        return False
    cards = data.get('cards')
    if not cards:
        return False
    cc = [] 
    for card in cards:
        did = card['desc'].get('dynamic_id')
        ltime = card['desc'].get('timestamp')
        cd = json.loads(card.get('card'))
        item = cd.get('item') or cd
        description = item.get('description')
        content = item.get('content')
        if cd.get('origin'):
            origin = json.loads(cd.get('origin'))
            oitem = origin.get('item')
            ouser = cd.get('origin_user').get('info').get('uname')
            if oitem:
                odesc = oitem.get('description')
                ocont = oitem.get('content')
                course = origin.get('url')
                id_ = origin.get('id')
                vest = origin.get('vest')
                video = origin.get('jump_url')
                room = origin.get('roomid')
                if odesc:
                    opic = oitem.get('pictures')
                    cc.append({"id": did, "type": "update_forward_picture_dynamic", "content":content,"o_content": odesc, "pic": opic,"time":ltime, "ouser":ouser})
                elif ocont:
                    cc.append({"id": did, "type": "update_forward_dynamic", "content":content,"o_content": ocont, "time":ltime, "ouser":ouser})
                elif course:
                    title = origin.get('title')
                    cc.append({"id": did, "type": "update_forward_course", "title": title, "url": course,"time":ltime, "ouser":ouser})
                elif vest:
                    o_content = vest.get('content')
                    cc.append({"id": did, "type": "update_forward_vest", "content":content, "o_content": o_content,"time":ltime, "ouser":ouser})
                elif id_:
                    title = origin.get('title')
                    cc.append({"id": did, "type": "update_forward_column", "title": title, "url": "https://www.bilibili.com/read/cv{}".format(id_),"time":ltime, "ouser":ouser})
                elif video:
                    ee = enc(int(re.match(avReg, video).group('av')))
                    if not ee:
                        continue
                    video = "https://www.bilibili.com/video/{}".format(ee)
                    title = origin.get('title')
                    cc.append({"id": did, "type": "update_forward_video", "content":content,"title": title, "url": video,"time":ltime, "ouser":ouser})
                elif room:
                    cc.append({"id": did, "type": "update_forward_live", "content":content,"url": 'https://live.bilibili.com/{}'.format(room),"time":ltime, "ouser":ouser})
        else:
            id_ = cd.get('id')
            vest = cd.get('vest')
            video = cd.get('jump_url')
            if vest:
                content = vest.get('content')
                cc.append({"id": did, "type": "update_vest", "content": content,"time":ltime})
            elif id_:
                title = cd.get('title')
                cc.append({"id": did, "type": "update_column", "title": title, "url": "https://www.bilibili.com/read/cv{}".format(id_),"time":ltime})
            elif video:
                content = cd.get('dynamic')
                ee = enc(int(re.match(avReg, video).group('av')))
                if not ee:
                    continue
                video = "https://www.bilibili.com/video/{}".format(ee)
                title = cd.get('title')
                cc.append({"id": did, "type": "update_video", "content":content,"title": title, "url": video,"time":ltime})
            elif content:
                cc.append({"id": did, "type": "update_dynamic", "content": content, "time":ltime})
            elif description:
                pic = item.get('pictures')
                cc.append({"id": did, "type": "update_picture_dynamic", "content": description, "pic": pic, "time":ltime})
    return cc


async def getUp(uid, SESSDATA, CSRF):
    result = False
    count = 0
    while not result and count < 3:
        count += 1
        cookies = httpx.Cookies()
        cookies.set("SESSDATA", SESSDATA, domain=".bilibili.com")
        cookies.set("bili_jct", CSRF, domain=".bilibili.com")
        result = await request(durl.format(uid), header, cookies)
    if not result:
        return({'success': False, 'name': 'name', "did":0})

    code = json.loads(result.content).get('code')
    msg = json.loads(result.content).get('message')
    if code != 0:
        print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[HTTP]' + 'Code:{}  Msg:{}'.format(code,msg))
        return({'success': False, 'name': 'name', "did":0})
    data = json.loads(result.content).get('data')
    cards = data.get('cards')
    if not cards or len(cards) == 0:
        return({'success': False, 'name': 'name', "did":0})

    name = cards[0].get('desc').get('user_profile').get('info').get('uname')
    did = cards[0].get('desc').get('dynamic_id')
    
    return({'success': True, 'name': name, "did":did})
