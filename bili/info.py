import httpx
import time
import traceback
import re
import asyncio
import json

durl = 'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid={}&offset_dynamic_id=0&need_top=0'
lurl = 'http://api.live.bilibili.com/bili/living_v2/{}'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.49"}

table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
	tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608

def enc(x):
	x=(x^xor)+add
	r=list('BV1  4 1 7  ')
	for i in range(6):
		r[s[i]]=table[x//58**i%58]
	return ''.join(r)

async def request(url, header):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers = header, timeout=30)
            return response
        except httpx.HTTPError:
            print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[HTTP]' + traceback.format_exc())
            return False

async def getLive(uid):
    result = False
    count = 0
    while not result and count < 3:
        count += 1
        result = await request(lurl.format(uid), header)
    if not result:
        return False
    data = json.loads(result.text).get('data')
    if not data:
        return False
    if data.get('status') != 1:
        return False
    else:
        return data.get('url')


async def getCards(uid):
    avReg = r'^bilibili\:\/\/video\/(?P<av>[0-9]+)\/\?.*?'
    result = False
    count = 0
    while not result and count < 3:
        count += 1
        result = await request(durl.format(uid), header)
    if not result:
        return False
    data = json.loads(result.text).get('data')
    if not data:
        return False
    cards = data.get('cards')
    if not cards:
        return False
    cc = [] 
    for card in cards:
        did = card['desc'].get('dynamic_id')
        time = card['desc'].get('timestamp')
        cd = json.loads(card.get('card'))
        item = cd.get('item')
        if item:
            description = item.get('description')
            content = item.get('content')
            if description:
                pic = item.get('pictures')
                cc.append({"id": did, "type": "update_picture_dynamic", "content": description, "pic": pic, "time":time})
            else:
                if cd.get('origin'):
                    origin = json.loads(cd.get('origin'))
                    oitem = origin.get('item')
                    if oitem:
                        odesc = oitem.get('description')
                        ocont = oitem.get('content')
                        if odesc:
                            opic = oitem.get('pictures')
                            cc.append({"id": did, "type": "update_forward_picture_dynamic", "content":content,"o_content": odesc, "pic": opic,"time":time})
                        else:
                            cc.append({"id": did, "type": "update_forward_dynamic", "content":content,"o_content": ocont, "time":time})
                    else :
                        course = origin.get('url')
                        id_ = origin.get('id')
                        vest = origin.get('vest')
                        if course:
                            title = origin.get('title')
                            cc.append({"id": did, "type": "update_forward_course", "title": title, "url": course,"time":time})
                        elif vest:
                            o_content = vest.get('content')
                            cc.append({"id": did, "type": "update_forward_vest", "content":content, "o_content": o_content,"time":time})
                        elif id_:
                            title = origin.get('title')
                            cc.append({"id": did, "type": "update_forward_column", "title": title, "url": "https://www.bilibili.com/read/cv{}".format(id_),"time":time})
                        else:
                            video = origin.get('jump_url')
                            video = "https://www.bilibili.com/video/{}".format(enc(int(re.match(avReg, video).group('av'))))
                            title = origin.get('title')
                            cc.append({"id": did, "type": "update_forward_video", "content":content,"title": title, "url": video,"time":time})
                else:
                    cc.append({"id": did, "type": "update_dynamic", "content": content, "time":time})

        else :
            id_ = cd.get('id')
            vest = cd.get('vest')
            if vest:
                content = vest.get('content')
                cc.append({"id": did, "type": "update_vest", "content": content,"time":time})
            elif id_:
                title = cd.get('title')
                cc.append({"id": did, "type": "update_column", "title": title, "url": "https://www.bilibili.com/read/cv{}".format(id_),"time":time})
            else:
                content = cd.get('dynamic')
                video = cd.get('jump_url')
                video = "https://www.bilibili.com/video/{}".format(enc(int(re.match(avReg, video).group('av'))))
                title = cd.get('title')
                cc.append({"id": did, "type": "update_video", "content":content,"title": title, "url": video,"time":time})
    return cc


async def getUp(uid):
    result = False
    count = 0
    while not result and count < 3:
        count += 1
        result = await request(durl.format(uid), header)
    if not result:
        return({'success': False, 'name': 'name', "did":0})
    data = json.loads(result.text).get('data')
    cards = data.get('cards')
    if not cards or len(cards) == 0:
        return({'success': False, 'name': 'name', "did":0})

    name = cards[0].get('desc').get('user_profile').get('info').get('uname')
    did = cards[0].get('desc').get('dynamic_id')
    
    return({'success': True, 'name': name, "did":did})
    