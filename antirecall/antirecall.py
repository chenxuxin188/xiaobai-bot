import time
import asyncio
import traceback



async def recall(bot, m, selfid):
    await asyncio.sleep(90)
    try:
        await bot.delete_msg(message_id=m, self_id = selfid)
    except:
        print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]消息撤回失败！消息ID：{}，QQ：{}'.format(m, selfid))


async def antirecall(event, bot, g):
    print('recall')
    if g[11] == 0:
        return False
    if event.operator_id != event.user_id:
        return False

    if event.operator_id == event.self_id:
        return False
    print('xxx')
    try:
        m = await bot.get_msg(message_id = event.message_id, self_id = event.self_id)
        print(m)
        await bot.send(event, '喵？你撤回了什喵？让咱看看喵……', at_sender = True)
        x = await bot.send(event, time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(m['time'])) + '[CQ:at,qq={}]'.format(event.user_id) + '：\n' + m['message'])
        coro = recall(bot, x['message_id'], event.self_id)
        loop = asyncio.get_event_loop()
        loop.create_task(coro)
        return True
    except:
        print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]消息获取失败！' + traceback.format_exc())
        return False

    