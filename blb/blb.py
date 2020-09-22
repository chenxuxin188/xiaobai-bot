from .chapter import checkNovel, request, getChapters
import asyncio
import json

loop = asyncio.new_event_loop()

async def checkBooks(bot, db, groups):
    l = await db.blbBookList()
    g = await db.groupList()
    if not l or not g:
        return

    for b in l:
        await asyncio.sleep(10)
        book = b[0]
        name = b[1]
        chapter = b[2]
        dic = await checkNovel(book)
        if not dic['success']:
            continue
        free = dic['free']
        vip = dic['vip']
        fl = []
        vl = []
        for f in free:
            if f[0] > chapter:
                fl.append(f)
        for v in vip:
            if v > chapter:
                vl.append(v)
        updates = await getChapters(fl, vl, book, name)

        for group in g:
            if(group[12]):
                bs = json.loads(group[12])
                for bl in bs:
                    if bl == book:
                        for u in updates:
                            a = groups.get(group[0])
                            if not a:
                                break
                            suc = False
                            ttt = 0
                            while not suc and ttt < 3:
                                try:
                                    ttt += 1
                                    atall = ''
                                    if group[15] == 1:
                                        atall = '[CQ:at,qq=all]'
                                    await bot.send_msg(self_id=a, group_id=group[0],message=atall + u)
                                    await asyncio.sleep(0.2)
                                    suc = True
                                except:
                                    suc = False
                        break
        await db.blbUpdated(book, dic['max'])
