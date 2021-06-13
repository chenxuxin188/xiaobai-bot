# 色图功能
import httpx
import re
import time
from PIL import Image
from io import BytesIO
from random import randrange
import base64
import math
import asyncio
import traceback

url = 'https://api.lolicon.app/setu/?apikey={}{}{}'
header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.49"
}

setuReg = r'^ *(?P<keyword>.*?)?[冲衝Gg][冲衝Kk][冲衝Dd][！!]*$'
tripleReg = r'^ *(?P<keyword>.*?)?三[连連][冲衝][！!]*$'

logger = {}
gstat = {}
async def request(url, header):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers = header, timeout=30)
            return response
        except httpx.HTTPError:
            print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[HTTP]' + traceback.format_exc())
            return False
            
async def recall(bot, m, selfid):
    await asyncio.sleep(90)
    try:
        await bot.delete_msg(message_id=m, self_id = selfid)
    except:
        print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]消息撤回失败！消息ID：{}，QQ：{}'.format(m, selfid))

async def G2B(r, anti):
    def process(r, anti):
        try:
            img = Image.open(BytesIO(r.content))
            if(anti == 1):
                img.putpixel((0,0), (randrange(256), randrange(256), randrange(256)))
                img.putpixel((img.size[0] - 1,0), (randrange(256), randrange(256), randrange(256)))
                img.putpixel((0,img.size[1] - 1), (randrange(256), randrange(256), randrange(256)))
                img.putpixel((img.size[0]- 2,img.size[1]- 2), (randrange(256), randrange(256), randrange(256)))

            if(int(r.headers['content-length']) > 12000000):
                p = int(math.sqrt(12000000 / int(r.headers['content-length'])))
                w = int(img.size[0] * p)
                h = int(img.size[1] * p)
                img.thumbnail({w,h})
            buffered = BytesIO()
            img.save(buffered, format='PNG')
            base = base64.b64encode(buffered.getvalue())
            return str(base.decode('utf-8'))
        except Exception:
            print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
            return False

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, process, r, anti)
    return result


async def sendSetu(event, bot, CQparse, g):
    if (not gstat.get(event.group_id)):
        gstat.update({event.group_id: 0})
    
    msg = CQparse.removeCQcodes(event.message)
    se = re.match(setuReg, msg)
    t = re.match(tripleReg, msg)

    keyword = ''
    tri = '&num=1'
    if(se):
        if(se.group('keyword') != ''):
            keyword = '&keyword={}'.format(se.group('keyword'))
    elif(t):
        tri = '&num=3'
        if(t.group('keyword') != ''):
            k = t.group('keyword')
            if k == '猫娘' or k == '猫耳' or k == '铂金':
                keyword = '&keyword=猫耳'
    else:
        gstat[event.group_id] = 0
        return False



    if(gstat[event.group_id] == 1):
        await bot.send(event, '咱正在发送色图喵！请等下再冲喵！', at_sender = True)
        return True

    gstat[event.group_id] = 1
    
    if(g):
        if(g[1]):
            if(g[1] != ''):
                apikey = g[1]
        else:
            await bot.send(event, '咱没办法在这个群发色图喵~~')
            gstat[event.group_id] = 0
            return True
    else:
        await bot.send(event, '咱没办法在这个群发色图喵~~')
        gstat[event.group_id] = 0
        return True

    if g[2] == 0:
        await bot.send(event, '咱没办法在这个群发色图喵~~')
        gstat[event.group_id] = 0
        return True

    now = time.time()
    gpt = 0
    upt = 0

    if(not logger.get(event.group_id)):
        logger.update({event.group_id: {'time': now}})
        logger[event.group_id].update({event.user_id: now})
    else:
        if(logger[event.group_id]['time'] + g[7] > now):
            await bot.send(event, '咱刚刚在这里发过色图了喵！', at_sender = True)
            gstat[event.group_id] = 0
            return True
        else:
            if(not logger[event.group_id].get(event.user_id)):
                gpt = logger[event.group_id]['time']
                logger[event.group_id].update({event.user_id: now})
                logger[event.group_id]['time'] = now
            else:
                if(logger[event.group_id][event.user_id] + g[6] > now):
                    await bot.send(event, '你才找咱发过色图喵。不能整天看色图，要休息休息喵！', at_sender = True)
                    gstat[event.group_id] = 0
                    return True
                else:
                    gpt = logger[event.group_id]['time']
                    upt = logger[event.group_id][event.user_id]
                    logger[event.group_id]['time'] = now
                    logger[event.group_id][event.user_id] = now


    
    response = await request(url.format(apikey, keyword, tri), header)
    if(not response):
        logger[event.group_id]['time'] = gpt
        logger[event.group_id][event.user_id] = upt
        await bot.send(event, '色图服务器出错了喵……', at_sender = True)
        gstat[event.group_id] = 0
        return True
    
    data = response.json()
    
    if(data['code'] == -1):
        logger[event.group_id]['time'] = gpt
        logger[event.group_id][event.user_id] = upt
        await bot.send(event, '唔……色图搜索失败了喵，咱也不知道哪里出错了喵……', at_sender = True)
        gstat[event.group_id] = 0
        return True
    elif(data['code'] == 401):
        logger[event.group_id]['time'] = gpt
        logger[event.group_id][event.user_id] = upt
        await bot.send(event, '搜索色图的APIKEY有问题喵，咱建议你找咱的爸爸反馈一下喵！', at_sender = True)
        gstat[event.group_id] = 0
        return True
    elif(data['code'] == 403):
        logger[event.group_id]['time'] = gpt
        logger[event.group_id][event.user_id] = upt
        await bot.send(event, '咱搜索色图的时候好像出了一点点问题喵……建议找爸爸反馈一下喵！', at_sender = True)
        gstat[event.group_id] = 0
        return True
    elif(data['code'] == 404):
        logger[event.group_id]['time'] = gpt
        logger[event.group_id][event.user_id] = upt
        await bot.send(event, '咱找不到相关的色图喵……换一个关键词咱可能就能找到了喵！', at_sender = True)
        gstat[event.group_id] = 0
        return True
    elif(data['code'] == 429):
        logger[event.group_id]['time'] = gpt
        logger[event.group_id][event.user_id] = upt
        await bot.send(event, '色图搜索次数用完了喵。再过{}秒之后，就能再次搜索色图了喵！'.format(data['quota_min_ttl']), at_sender = True)
        gstat[event.group_id] = 0
        return True

    if(t):
        await bot.send(event, '三连冲要开始了喵！请坐好站稳，抓紧扶手喵！', at_sender = True)
        c = 0
        for d in data['data']:
            await bot.send(event, '图{}发射ing喵...\n画师：{} 作品ID：{}'.format(c+1, d['author'], d['pid']), at_sender = True)
            c += 1
            r = None
            s = False
            for i in range(0,3):
                r = await request(d['url'], header)
                if(r):
                    s = True
                    break
            if(not s):
                await bot.send(event, '图{}获取失败了喵QAQ'.format(c), at_sender = True)
                continue
            base = await G2B(r, g[4])
            if (not base):
                await bot.send(event, '图{}发送失败了喵QAQ'.format(c), at_sender = True)
            try:
                xxx = await bot.send(event, CQparse.img64(base))
                if g[3] == 1:
                    coro = recall(bot, xxx['message_id'], event.self_id)
                    loop = asyncio.get_event_loop()
                    loop.create_task(coro)
            except:
                try:
                    xxx = await bot.send(event, CQparse.img64(base))
                    if g[3] == 1:
                        coro = recall(bot, xxx['message_id'], event.self_id)
                        loop = asyncio.get_event_loop()
                        loop.create_task(coro)
                except:
                    try:
                        xxx = await bot.send(event, CQparse.img64(base))
                        if g[3] == 1:
                            coro = recall(bot, xxx['message_id'], event.self_id)
                            loop = asyncio.get_event_loop()
                            loop.create_task(coro)
                    except:
                        await bot.send(event, '图{}发送失败了喵QAQ'.format(c), at_sender = True)
        await bot.send(event, '三连冲结束了喵！', at_sender = True)
        gstat[event.group_id] = 0
        return True
    elif(se):
        d = data['data'][0]
        await bot.send(event, '色图发射ing喵...\n画师：{} 作品ID：{}'.format(d['author'], d['pid']), at_sender = True)
        r = None
        s = False
        for i in range(0,3):
            r = await request(d['url'], header)
            if(r):
                s = True
                break
        if(not s):
            logger[event.group_id]['time'] = gpt
            logger[event.group_id][event.user_id] = upt
            await bot.send(event, '色图获取失败了喵QAQ', at_sender = True)
            return True
        base = await G2B(r, g[4])
        if (not base):
            await bot.send(event, '色图发送失败了喵QAQ', at_sender = True)
            gstat[event.group_id] = 0
            return True
        try:
            xxx = await bot.send(event, CQparse.img64(base))
            if g[3] == 1:
                coro = recall(bot, xxx['message_id'], event.self_id)
                loop = asyncio.get_event_loop()
                loop.create_task(coro)
        except:
            try:
                xxx = await bot.send(event, CQparse.img64(base))
                if g[3] == 1:
                    coro = recall(bot, xxx['message_id'], event.self_id)
                    loop = asyncio.get_event_loop()
                    loop.create_task(coro)
            except:
                try:
                    xxx = await bot.send(event, CQparse.img64(base))
                    if g[3] == 1:
                        coro = recall(bot, xxx['message_id'], event.self_id)
                        loop = asyncio.get_event_loop()
                        loop.create_task(coro)
                except:
                    await bot.send(event, '色图发送失败了喵QAQ', at_sender = True)
        gstat[event.group_id] = 0
        return True
