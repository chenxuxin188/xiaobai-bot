import time
import asyncio
import re
from random import randrange

from .like import like
from .normal import normal, nolike

liantongReg = r'([炼煉][銅铜])|([恋戀]童)'
signReg = r'^ *摸+$'
wsignReg = r'[签簽]到'
zaoReg = r'早((上好)|(安))?呀?'
wananReg = r'晚安'
naReg = r'呐+'
kouqiuReg = r'给?我?要?戴?(?P<min>[1-9][0-9]*)(?P<hr>(分钟)|(小时)|(天))的?((禁言)|(口球))(套餐)?'
naImg = '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'

logger = {}

usr = {}

async def interact(event, bot, CQparse, db, g):
    if event.type == 'notice':
        if event.sub_type == 'poke':
            if event.target_id == event.self_id:
                w = g[5]
                ut = logger.get(event.user_id)
                pt = 0
                t = time.time()
                if ut:
                    if t - ut < w:
                        return False
                    else: 
                        pt = ut
                        logger[event.user_id] = t
                else:
                    logger.update({event.user_id: t})
                
                signed = await db.isSigned(event.user_id)
                ulike = await db.getLike(event.user_id)
                mood = await db.getMood(event.user_id)

                if not signed:
                    await bot.send(event, '每天要签到之后才能开始互动喵！', at_sender = True)
                    logger[event.user_id] -= w - 10
                    return True

                clike = like[1]
                mm = 0
                ll = 0
                if mood < 50:
                    mm = 0
                elif mood < 80:
                    mm = 1
                else:
                    mm = 2

                if ulike < clike[1][0]:
                    ll = 0
                elif ulike < clike[1][1]:
                    ll = 1
                else:
                    ll = 2

                r = randrange(120)

                if clike[3][mm][ll] == 1:
                    if(r < mood):
                        await db.changeLike(event.user_id, 1)
                elif clike[3][mm][ll] == -1:
                    if(r > mood):
                        await db.changeLike(event.user_id, -1)
                await db.changeMood(event.user_id, clike[2][mm][ll])
                x = randrange(1,len(clike[4][mm][ll]))
                await bot.send(event, clike[4][mm][ll][x], at_sender = True)
                if  clike[4][mm][ll][0] > 0:
                    await bot.set_group_ban(group_id = event.group_id, user_id = event.user_id, duration = clike[4][mm][ll][0] * 60)
                return True
        elif event.sub_type == 'honor':
            if event.honor_type == 'talkative':
                if event.user_id == event.self_id:
                    await bot.send(event, '龙王再次下发号令，全体群员给咱喷水喵！')
                    return True
                else:
                    await bot.send(event, '龙王喷水喵！', at_sender = True)
                    return True
        else:
            return False

    if event.type == 'message':
        if re.search(liantongReg, event.message):
            await bot.send(event, '五年起步，最高死刑喵！',at_sender = True)
            return True
        elif re.search(naReg, event.message):
            await bot.send(event, CQparse.img64(naImg),at_sender = True)
            return True

        msg = event.message

        xb = re.findall(r'小白', msg)
        t = time.time()
        if xb:
            pass
        elif usr.get(event.group_id):
            us = usr[event.group_id].get(event.user_id)
            if not us:
                return False
            if t - us > 10:
                return False
        else:
            at = False
            codes = CQparse.findCQcodes(event.message)
            for code in codes:
                p = CQparse.CQparse(code)
                if p['CQtype'] == 'at':
                    if p['qq'] != 'all':
                        if int(p['qq']) == event.self_id:
                            at = True
            if at == False:
                return False


        w = g[5]
        ut = logger.get(event.user_id)
        pt = 0
        if ut:
            if t - ut < w:
                return False
            else: 
                pt = ut
                logger[event.user_id] = t
        else:
            logger.update({event.user_id: t})
        
        msg = CQparse.removeCQcodes(msg)
        msg = re.sub(r'小白','', msg)
        msg = re.sub(r' ','', msg)

        lt = time.localtime()


        signed = await db.isSigned(event.user_id)
        ulike = await db.getLike(event.user_id)
        mood = await db.getMood(event.user_id)


        kq = re.search(kouqiuReg,msg)
        if kq:
            await bot.send(event, '真是奇怪的要求喵……')
            dur = 0
            if kq.group('hr') == '分钟':
                dur = 60 * int(kq.group('min'))
            elif kq.group('hr') == '小时':
                dur = 60 * 60 * int(kq.group('min'))
            await bot.set_group_ban(group_id = event.group_id, user_id = event.user_id, duration = dur)

        if re.match(signReg, msg):
            si = await db.sign(event.user_id)
            if si:
                await bot.send(event, '喵喵~~签到成功了喵！\n心情值：{}'.format(si), at_sender = True)
                return True
            else:
                await bot.send(event, '喵？今天你已经签到过了喵！', at_sender = True)
                return True
        elif re.search(wsignReg, msg):
            await bot.send(event, '要好好摸摸咱，咱才让你签到喵！', at_sender = True)
            logger[event.user_id] -= w - 10
            return True

        if not signed:
            await bot.send(event, '每天要签到之后才能开始互动喵！', at_sender = True)
            logger[event.user_id] -= w - 10
            return True

        if msg == '':
            if not usr.get(event.group_id):
                usr.update({event.group_id:{}})
                usr[event.group_id].update({event.user_id:t})
                logger[event.user_id] = pt
                await bot.send(event, '喵？叫咱有什么事喵？', at_sender=True)
                return True
            else:
                us = usr[event.group_id].get(event.user_id)
                if not us:
                    usr[event.group_id].update({event.user_id:t})
                    logger[event.user_id] = pt
                    await bot.send(event, '喵？叫咱有什么事喵？', at_sender=True)
                    return True
                else:
                    if t - us > 10:
                        usr[event.group_id].update({event.user_id:t})
                        logger[event.user_id] = pt
                        await bot.send(event, '喵？叫咱有什么事喵？', at_sender=True)
                    return True
                        

        if re.match(r'好感度', msg):
            await bot.send(event, '咱现在对你的好感度为{}喵~'.format(ulike), at_sender = True)
            return True
        elif re.match(r'心情', msg):
            t = ''
            if mood < 50:
                t = '不怎么样喵……'
            elif mood < 80:
                t = '还行喵~'
            else:
                t = '非常棒喵！'
            await bot.send(event, '心情值：{}\n咱现在的心情{}'.format(mood,t))
            return True
        
        if re.search(zaoReg,msg):
            if lt.tm_hour >= 4 and lt.tm_hour <= 10:
                await bot.send(event, '早上好喵~~', at_sender = True)
                return True
            elif lt.tm_hour >=10 and lt.tm_hour <=18:
                await bot.send(event, '现在已经不早了喵。如果你那是早上的话，那就早上好喵~如果你现在才起床的话，咱希望你今晚早点睡喵！早睡早起，身体棒棒喵！', at_sender=True)
                return True
            else:
                await bot.send(event, '喵？都这个点了，怎么还在跟咱说早上好瞄？唔喵……如果你那边是早上的话，那就早上好喵！', at_sender = True)
                return True
        elif re.match(wananReg,msg):
            ud = await bot.get_group_member_info(group_id = event.group_id, user_id = event.user_id)
            md = await bot.get_group_member_info(group_id = event.group_id, user_id = event.self_id)

            if (md['role'] == 'owner' and ud['role'] == 'admin') or (md['role'] == 'admin' and ud['role'] == 'member'):
                await bot.send(event, '晚安喵~咱口球给你戴好了，一定要睡够八个小时喵！', at_sender = True)
                await bot.set_group_ban(group_id = event.group_id, user_id = event.user_id, duration = 28800)
            else:
                await bot.send(event, '晚安喵~一定要睡够八个小时喵！', at_sender = True)
            return True

        clike = False
        cnolike = False
        cnormal = False

        for l in like:
            if re.match(l[0], msg):
                clike = l
                break

        if not clike:
            for l in normal:
                if re.match(l[0], msg):
                    cnormal = l
                    break

        if (not clike) and (not cnormal):
            for l in nolike:
                if re.match(l[0], msg):
                    cnolike = l
                    break

        if (not clike) and (not cnormal) and (not cnolike): 
            logger[event.user_id] = pt
            return False



        if clike:
            mm = 0
            ll = 0
            if mood < 50:
                mm = 0
            elif mood < 80:
                mm = 1
            else:
                mm = 2

            if ulike < clike[1][0]:
                ll = 0
            elif ulike < clike[1][1]:
                ll = 1
            else:
                ll = 2

            r = randrange(120)

            if clike[3][mm][ll] == 1:
                if(r < mood):
                    await db.changeLike(event.user_id, 1)
            elif clike[3][mm][ll] == -1:
                if(r > mood):
                    await db.changeLike(event.user_id, -1)
            await db.changeMood(event.user_id, clike[2][mm][ll])
            x = randrange(1,len(clike[4][mm][ll]))
            await bot.send(event, clike[4][mm][ll][x], at_sender = True)
            if  clike[4][mm][ll][0] > 0:
                await bot.set_group_ban(group_id = event.group_id, user_id = event.user_id, duration = clike[4][mm][ll][0] * 60)
            return True
        elif cnormal:
            m = mood
            mm = 0
            if m < 50:
                mm = 0
            elif m < 80:
                mm = 1
            else:
                mm = 2

            r = randrange(200)
            if cnormal[3][mm] ==1:
                if(r < m):
                    await db.changeLike(event.user_id, 1)
            elif cnormal[3][mm] == -1:
                if(r > m):
                    await db.changeLike(event.user_id, -1)
            await db.changeMood(event.user_id, cnormal[2][mm])
            x = randrange(1,len(cnormal[1][mm]))
            await bot.send(event, cnormal[1][mm][x], at_sender = True)
            if cnormal[1][mm][0] > 0:
                await bot.set_group_ban(group_id = event.group_id, user_id = event.user_id, duration = cnormal[1][mm][0] * 60)
            return True
        elif cnolike:
            await bot.send(event, cnolike[1][randrange(0,len(cnolike[1]))])
            if cnolike[2] > 0:
                await bot.set_group_ban(group_id = event.group_id, user_id = event.user_id, duration = cnolike[2] * 60)
            return True