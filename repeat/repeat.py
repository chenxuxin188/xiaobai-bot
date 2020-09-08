from random import randrange

logger = {}

async def randomRepeat(event, bot, g):
    if g[10] == 0:
        return False
    if randrange(1000) < 2:
        await bot.send(event, event.message)
    return True




async def repeat(event, bot, CQparse,g):
    if g[10] == 0:
        return False
    t = logger.get(event.group_id)
    if not t:
        logger.update({event.group_id: [event.message, event.user_id, 1, False]})
        return False
    elif t[0] != event.message:
        logger[event.group_id] = [event.message, event.user_id, 1, False]
        return False
    elif t[1] != event.user_id:
        logger[event.group_id][1] = event.user_id
        logger[event.group_id][2] += 1
    if (not logger[event.group_id][3]) and (logger[event.group_id][2] > 2):
        logger[event.group_id][3] = True
        x = randrange(100)
        if x < 45:
            await bot.send(event, event.message)
        elif x < 90:
            await bot.send(event, '喵！打断！')
        else:
            await bot.send(event, '不许复读了喵！')
            await bot.set_group_ban(group_id=event.group_id, user_id = event.user_id, duration = 60)
        
        return True
    return False

