from .info import getCards, request, getLive
import asyncio
import json
import time 
from random import randrange

loop = asyncio.new_event_loop()

async def checkUps(bot, db, CQparse, groups, SESSDATA, CSRF):
    l = await db.biliList()
    g = await db.groupList()
    if not l or not g:
        return

    for b in l:
        await asyncio.sleep(randrange(10,60))
        uid = b[0]
        name = b[1]
        did = b[2]
        blive = b[3]
        cards = await getCards(uid, SESSDATA, CSRF)
        live = await getLive(uid, SESSDATA, CSRF)
        if not cards or len(cards) == 0:
            continue
        dl = []
        for c in cards:
            if c.get('id') > did:
                dl.append(c)
        
        lstat = None
        if live:
            if blive == 0:
                lstat = 1
        elif not live:
            if blive == 1:
                lstat = 0
                
        for group in g:
            a = groups.get(group[0])
            if not a:
                continue
            if(group[13]):
                bs = json.loads(group[13])
                for bl in bs:
                    if bl == uid:
                        if lstat == 1:
                            await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】开始直播了喵！直播间地址为：\n{}".format(name, live))
                        elif lstat == 0:
                            await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】下播了喵~".format(name))

                        for u in dl:
                            if u.get('type') == 'update_picture_dynamic':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】发送新动态了喵！".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                                pics = ''
                                for pic in u.get('pic'):
                                    pics += CQparse.img(pic.get('img_src'))
                                await bot.send_msg(self_id=a, group_id=group[0],message=pics)
                            elif u.get('type') == 'update_forward_picture_dynamic':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】转发动态了喵！".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message="原文：\n" + u.get('o_content'))
                                await asyncio.sleep(0.1)
                                pics = ''
                                for pic in u.get('pic'):
                                    pics += CQparse.img(pic.get('img_src'))
                                await bot.send_msg(self_id=a, group_id=group[0],message=pics)
                            elif u.get('type') == 'update_forward_dynamic':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】转发动态了喵！".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message="原文：\n" + u.get('o_content'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_dynamic':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】发送新动态了喵！".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_forward_course':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】转发课程了喵！".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('title') + '\n' + u.get('url'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_video':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】发送新视频了喵！".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('content') + "：\n" + u.get('title') + '\n' + u.get('url'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_forward_video':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】转发视频了喵！".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('content') + "：\n" + u.get('title') + '\n' + u.get('url'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_column':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】发送新专栏了喵！".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('title') + '\n' + u.get('url'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_forward_column':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】发送新专栏了喵！".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('title') + '\n' + u.get('url'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_vest':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】更换新头像框了喵！".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_forward_vest':
                                await bot.send_msg(self_id=a, group_id=group[0],message="关注的UP主【{}】真的好无聊喵，转发换头像框的消息干什喵？".format(name))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                                await bot.send_msg(self_id=a, group_id=group[0],message="原文：\n" + u.get('o_content'))
                                await asyncio.sleep(0.1)
                        break
        if len(dl) != 0:
            await db.biliDynamicUpdated(uid, dl[0].get('id'))
        if lstat == 0 or lstat == 1:
            await db.biliLiveUpdated(uid, lstat)
