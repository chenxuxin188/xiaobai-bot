from .info import getCards, request, getLive
import asyncio
import json
import time
import traceback

bili = {}

async def checkUps(bot, db, CQparse, groups, SESSDATA, CSRF):
    async def sendmsg(self_id,group_id,message):
        c = 0
        while c < 3:
            c += 1
            try:
                await bot.send_msg(self_id=self_id, group_id=group_id, message = message)
                return True
            except:
                print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[BILI]' + traceback.format_exc())
        return False

    l = await db.biliList()
    g = await db.groupList()
    if not l or not g:
        return

    for b in l:
        await asyncio.sleep(10)
        uid = b[0]
        name = b[1]

        cards = await getCards(uid, SESSDATA, CSRF)
        live = await getLive(uid, SESSDATA, CSRF)

        if not bili[uid]:
            bili.update({uid: [cards[0].get('id'), live]})
            continue

        if not cards or len(cards) == 0:
            continue
        dl = []
        for c in cards:
            if c.get('id') > bili[uid][0]:
                dl.append(c)
        
        lstat = None
        if live:
            if bili[uid][1] == 0:
                lstat = 1
        elif not live:
            if bili[uid][1] == 1:
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
                            await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】开始直播了喵！直播间地址为：\n{}".format(name, live))
                        elif lstat == 0:
                            await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】下播了喵~".format(name))

                        for u in reversed(dl):

                            if u.get('type') == 'update_picture_dynamic':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】发送新动态了喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                                pics = ''
                                for pic in u.get('pic'):
                                    pics += CQparse.img(pic.get('img_src'))
                                await sendmsg(self_id=a, group_id=group[0],message=pics)
                            elif u.get('type') == 'update_forward_picture_dynamic':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】转发动态了喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message="原文：\n" + u.get('ouser') + "：\n" + u.get('o_content'))
                                await asyncio.sleep(0.1)
                                pics = ''
                                for pic in u.get('pic'):
                                    pics += CQparse.img(pic.get('img_src'))
                                await sendmsg(self_id=a, group_id=group[0],message=pics)
                            elif u.get('type') == 'update_forward_dynamic':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】转发动态了喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message="原文：\n" + u.get('ouser') + "：\n" + u.get('o_content'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_dynamic':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】发送新动态了喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_forward_course':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】转发课程了喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "\n" + "课程发布者：" + u.get('ouser') + "：\n" + u.get('title'))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message='课程链接：' + u.get('url'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_video':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】发送新视频了喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "：\n" + u.get('content') + "\n" + u.get('title'))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message='视频链接：' + u.get('url'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_forward_video':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】转发视频了喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "：\n" + u.get('content') + "\n" + u.get('ouser') + "：\n" + u.get('title'))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message='视频链接：' + u.get('url'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_column':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】发送新专栏了喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "：\n" + u.get('title'))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message='专栏链接：' + u.get('url'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_forward_column':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】转发专栏了喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "\n" + u.get('ouser') + "：\n" + u.get('title'))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message='专栏链接：' + u.get('url'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_vest':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】更换新装饰了喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_forward_vest':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】真的好无聊喵，转发换装饰的消息干什喵？".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message="原文：\n" + u.get('o_content'))
                                await asyncio.sleep(0.1)
                            elif u.get('type') == 'update_forward_live':
                                await sendmsg(self_id=a, group_id=group[0],message="关注的UP主【{}】转发了直播间喵！".format(name))
                                await sendmsg(self_id=a, group_id=group[0],message='动态链接：https://t.bilibili.com/{}'.format(u.get('id')))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message=time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(u.get('time'))) + "\n" + name + "：\n" + u.get('content'))
                                await asyncio.sleep(0.1)
                                await sendmsg(self_id=a, group_id=group[0],message="直播间地址：\n" + u.get('url'))
                                await asyncio.sleep(0.1)
                        break
        if len(dl) != 0:
            bili[uid][0] = dl[0].get('id')
        if lstat == 0 or lstat == 1:
            bili[uid][1] = lstat
