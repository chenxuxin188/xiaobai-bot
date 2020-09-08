import aiomysql
import traceback
import config
import time
import math
from random import randrange

class DB:
  def __init__(self):
    pass

  async def connect(self):
    try:
      self.mydb = await aiomysql.connect(
        host=config.mysql_host,
        port=config.mysql_port,
        user=config.mysql_user,
        password=config.mysql_pswd,
        db=config.mysql_db,
        autocommit=True
      )
      return True
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False

  def close(self):
    try:
      self.mydb.close()
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False

  async def groupList(self):
    try:
      async with self.mydb.cursor() as db:
        await db.execute('SELECT * from `group`')
        l = await db.fetchall()
        await db.close()
        return l
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False

  async def getGroup(self, group):
    try:
      async with self.mydb.cursor() as db:
        await db.execute('SELECT * from `group` WHERE `group`.group=%s', (group,))
        d = await db.fetchall()
        await db.close()
        if(len(d) == 0):
          return False
        else:
          return d[0]
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False



  async def addGroup(self, group):
    try:
      async with self.mydb.cursor() as db:
        await db.execute('SELECT * from `group` WHERE `group`.group=%s', (group,))
        res = await db.fetchall()
        if len(res) == 0:
          await db.execute('INSERT INTO `group` (`group`, `setu`, `seturecall`, `anti`, `iactCD`, `individualCD`, `groupCD`, kouqiu) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', [group, 0, 1, 0, 10, 600, 300, 0])
        await db.close()
        return True
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False


  async def kouqiu(self, group, stat):
    try:
      async with self.mydb.cursor() as db:
        await db.execute('UPDATE `group` SET `group`.kouqiu=%s WHERE `group`.group=%s', (stat ,group))
        await db.close()
        return True
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False



  async def isSigned(self, user):
    t = time.time()
    t += 28800
    try:
      async with self.mydb.cursor() as db:
        await db.execute('SELECT date from `sign` WHERE `sign`.num=%s', (user,))
        res = await db.fetchall()
        await db.close()
        if len(res) == 0:
          return False
        else:
          r = res[0][0]
          if int(r/86400) == int(t/86400):
            return True
          return False
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False



  async def sign(self, user):
    t = time.time()
    t += 28800
    try:
      async with self.mydb.cursor() as db:
        await db.execute('SELECT * from `sign` WHERE `sign`.num=%s', (user,))
        res = await db.fetchall()
        rand = randrange(0,101)
        rlike = randrange(1,6)
        if len(res) == 0:
          await db.execute('INSERT INTO `sign` (`num`, `like`, `date`, `mood`) VALUES (%s, %s, %s, %s)', (user, rlike, t, rand))
          await db.close()
          return rand
        else:
          r = res[0]
          if int(r[3]/86400) == int(t/86400):
            await db.close()
            return False
          like = r[1] + rlike
          await db.execute('UPDATE `sign` SET `sign`.like=%s WHERE `sign`.num=%s', (like, user))
          await db.execute('UPDATE `sign` SET `sign`.count=%s WHERE `sign`.num=%s', (0, user))
          await db.execute('UPDATE `sign` SET `sign`.date=%s WHERE `sign`.num=%s', (t, user))
          await db.execute('UPDATE `sign` SET `sign`.mood=%s WHERE `sign`.num=%s', (rand, user))
          await db.close()
          return rand
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False


  async def changeLike(self, user, change):
    try:
      c = change
      async with self.mydb.cursor() as db:
        await db.execute('SELECT * from `sign` WHERE `sign`.num=%s', (user,))
        res = await db.fetchall()
        x = res[0][2]
        if c == 1:
          await db.execute('UPDATE `sign` SET `sign`.count=%s WHERE `sign`.num=%s', (x + 1, user))
          c = randrange(1,4) * 4 / (3 + math.pow(2, 0.2 * x))
        await db.execute('UPDATE `sign` SET `sign`.like=%s WHERE `sign`.num=%s', (res[0][1] + c, user))
        await db.close()
        return True
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False

  async def getLike(self, user):
    try:
      async with self.mydb.cursor() as db:
        await db.execute('SELECT * from `sign` WHERE `sign`.num=%s', (user,))
        res = await db.fetchall()
        await db.close()
        if len(res) == 0:
          return False
        return res[0][1]
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False


  async def getMood(self, user):
    try:
      async with self.mydb.cursor() as db:
        await db.execute('SELECT mood from `sign` WHERE `sign`.num=%s', (user,))
        res = await db.fetchall()
        await db.close()
        if len(res) == 0:
          return False
        return res[0][0]
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False


  async def changeMood(self, user, change):
    try:
      async with self.mydb.cursor() as db:
        await db.execute('SELECT mood from `sign` WHERE `sign`.num=%s', (user,))
        res = await db.fetchall()
        if change != 0:
          await db.execute('UPDATE `sign` SET `sign`.mood=%s WHERE `sign`.num = %s', (min(res[0][0] + change*randrange(1,4), 100), user))
        await db.close()
        return True
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False
  def __del__(self):
    try:
      del self.mydb
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())