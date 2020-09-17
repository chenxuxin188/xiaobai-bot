import time

owner = {}

async def atownerban(event, bot, CQparse, g):
    ban = None
    if g[14] > 0:
        ban = g[14]
    else:
        return False

    codes = CQparse.findCQcodes(event.message)
    for code in codes:
        p = CQparse.CQparse(code)
        if p['CQtype'] == 'at':
            if p['qq'] != 'all':
                if not owner.get(event.group_id) or time.time() - owner.get(event.group_id)[1] > 86400:
                    usr = await bot.get_group_member_info(user_id = int(p['qq']), self_id = event.self_id, group_id = event.group_id)
                    if usr['role'] == 'owner':
                        owner.update({event.group_id: [int(p['qq']), time.time()]})
                        await bot.set_group_ban(self_id = event.self_id, group_id = event.group_id, user_id = event.user_id, duration = ban * 60)
                        return True
                else:
                    if int(p['qq']) == owner.get(event.group_id)[0]:
                        await bot.set_group_ban(self_id = event.self_id, group_id = event.group_id, user_id = event.user_id, duration = ban * 60)
                        return True
