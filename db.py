import aiomysql
import traceback
import config
import time
import math
from random import randrange

class DB:
  def __init__(self):
    pass

  async def createPool(self, loop):
    try:
      self.pool = await aiomysql.create_pool(
        host=config.mysql_host,
        port=config.mysql_port,
        user=config.mysql_user,
        password=config.mysql_pswd,
        db=config.mysql_db,
        loop=loop,
        minsize=5,
        maxsize=50,
        autocommit=True
      )

      if config.first:
        print('开始初始化数据库')
        group = """CREATE TABLE IF NOT EXISTS `group`  (
                    `group` bigint(0) NOT NULL,
                    `setuKey` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NULL DEFAULT NULL,
                    `setu` tinyint(0) NOT NULL DEFAULT 0,
                    `seturecall` tinyint(0) NOT NULL DEFAULT 1,
                    `anti` tinyint(0) NOT NULL DEFAULT 0,
                    `iactCD` int(0) NOT NULL DEFAULT 10,
                    `individualCD` int(0) NOT NULL DEFAULT 600,
                    `groupCD` int(0) NOT NULL DEFAULT 300,
                    `kouqiu` tinyint(0) NOT NULL DEFAULT 0,
                    `ban` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NULL DEFAULT NULL,
                    `repeat` tinyint(0) NOT NULL DEFAULT 1,
                    `antirecall` tinyint(0) NOT NULL DEFAULT 1,
                    `blb` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NULL DEFAULT NULL,
                    `bili` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NULL DEFAULT NULL,
                    PRIMARY KEY (`group`) USING BTREE
                  ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_520_ci ROW_FORMAT = Dynamic;"""

        sign = """CREATE TABLE IF NOT EXISTS `sign`  (
                    `num` bigint(0) NOT NULL,
                    `like` double NOT NULL DEFAULT 0,
                    `count` int(0) NOT NULL DEFAULT 0,
                    `date` double NOT NULL DEFAULT 0,
                    `mood` int(0) NOT NULL DEFAULT 0,
                    PRIMARY KEY (`num`) USING BTREE
                  ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_520_ci ROW_FORMAT = Dynamic;"""
        
        blb = """CREATE TABLE IF NOT EXISTS `blb`  (
                    `id` bigint(0) NOT NULL,
                    `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL,
                    `chapter` bigint(0) NOT NULL,
                    PRIMARY KEY (`id`) USING BTREE
                  ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_520_ci ROW_FORMAT = Dynamic;"""

        bili = """CREATE TABLE IF NOT EXISTS `bili`  (
                    `id` bigint(0) NOT NULL,
                    `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL,
                    `did` bigint(0) NOT NULL,
                    `live` tinyint(0) NOT NULL,
                    PRIMARY KEY (`id`) USING BTREE
                  ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_520_ci ROW_FORMAT = Dynamic;"""

        user = """CREATE TABLE IF NOT EXISTS `user`  (
                    `id` int(0) NOT NULL AUTO_INCREMENT,
                    `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL,
                    `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL,
                    `superadmin` tinyint(0) NOT NULL DEFAULT 0,
                    `groups` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
                    `qq` bigint(0) NULL DEFAULT NULL,
                    PRIMARY KEY (`id`, `username`) USING BTREE
                  ) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_520_ci ROW_FORMAT = Dynamic;"""

        cgroup = [
          "ALTER TABLE `group` ADD COLUMN `group` bigint(0) NOT NULL",
          "ALTER TABLE `group` ADD COLUMN `setuKey` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NULL DEFAULT NULL",
          "ALTER TABLE `group` ADD COLUMN `setu` tinyint(0) NOT NULL DEFAULT 0",
          "ALTER TABLE `group` ADD COLUMN `seturecall` tinyint(0) NOT NULL DEFAULT 1",
          "ALTER TABLE `group` ADD COLUMN `anti` tinyint(0) NOT NULL DEFAULT 0",
          "ALTER TABLE `group` ADD COLUMN `iactCD` int(0) NOT NULL DEFAULT 10",
          "ALTER TABLE `group` ADD COLUMN `individualCD` int(0) NOT NULL DEFAULT 600",
          "ALTER TABLE `group` ADD COLUMN `groupCD` int(0) NOT NULL DEFAULT 300",
          "ALTER TABLE `group` ADD COLUMN `kouqiu` tinyint(0) NOT NULL DEFAULT 0",
          "ALTER TABLE `group` ADD COLUMN `ban` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NULL DEFAULT NULL",
          "ALTER TABLE `group` ADD COLUMN `repeat` tinyint(0) NOT NULL DEFAULT 1",
          "ALTER TABLE `group` ADD COLUMN `antirecall` tinyint(0) NOT NULL DEFAULT 1",
          "ALTER TABLE `group` ADD COLUMN `blb` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NULL DEFAULT NULL",
          "ALTER TABLE `group` ADD COLUMN `bili` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NULL DEFAULT NULL"
        ]

        csign = [
          "ALTER TABLE `csign` ADD COLUMN `num` bigint(0) NOT NULL",
          "ALTER TABLE `csign` ADD COLUMN `like` double NOT NULL DEFAULT 0",
          "ALTER TABLE `csign` ADD COLUMN `count` int(0) NOT NULL DEFAULT 0",
          "ALTER TABLE `csign` ADD COLUMN `date` double NOT NULL DEFAULT 0",
          "ALTER TABLE `csign` ADD COLUMN `mood` int(0) NOT NULL DEFAULT 0"
        ]

        cblb = [
          "ALTER TABLE `cblb` ADD COLUMN `id` bigint(0) NOT NULL",
          "ALTER TABLE `cblb` ADD COLUMN `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL",
          "ALTER TABLE `cblb` ADD COLUMN `chapter` bigint(0) NOT NULL"
        ]

        cbili = [
          "ALTER TABLE `cbili` ADD COLUMN `id` bigint(0) NOT NULL",
          "ALTER TABLE `cbili` ADD COLUMN `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL",
          "ALTER TABLE `cbili` ADD COLUMN `did` bigint(0) NOT NULL",
          "ALTER TABLE `cbili` ADD COLUMN `live` tinyint(0) NOT NULL"
        ]

        cuser = [
          "ALTER TABLE `cuser` ADD COLUMN `id` int(0) NOT NULL AUTO_INCREMENT",
          "ALTER TABLE `cuser` ADD COLUMN `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL",
          "ALTER TABLE `cuser` ADD COLUMN `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci NOT NULL",
          "ALTER TABLE `cuser` ADD COLUMN `superadmin` tinyint(0) NOT NULL DEFAULT 0",
          "ALTER TABLE `cuser` ADD COLUMN `groups` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL",
          "ALTER TABLE `cuser` ADD COLUMN `qq` bigint(0) NULL DEFAULT NULL"
        ]


        async with self.pool.acquire() as mydb:
          async with mydb.cursor() as db:
            await db.execute(group)
            await db.execute(sign)
            await db.execute(blb)
            await db.execute(bili)
            await db.execute(user)
            for cmd in cgroup:
              try:
                await db.execute(cmd)
              except Exception:
                pass
            for cmd in csign:
              try:
                await db.execute(cmd)
              except Exception:
                pass
            for cmd in cblb:
              try:
                await db.execute(cmd)
              except Exception:
                pass
            for cmd in cbili:
              try:
                await db.execute(cmd)
              except Exception:
                pass
            for cmd in cuser:
              try:
                await db.execute(cmd)
              except Exception:
                pass
            await db.close()
        print('数据库初始化完成')
      return True
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False
      
  
  async def groupList(self):
    try:
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
          await db.execute('SELECT * from `group`')
          l = await db.fetchall()
          await db.close()
          
          return l
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False

  async def getGroup(self, group):
    try:
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
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
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
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
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
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
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
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
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
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
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
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
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
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
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
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
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
          await db.execute('SELECT mood from `sign` WHERE `sign`.num=%s', (user,))
          res = await db.fetchall()
          if change != 0:
            await db.execute('UPDATE `sign` SET `sign`.mood=%s WHERE `sign`.num = %s', (min(res[0][0] + change*randrange(1,4), 100), user))
          await db.close()
          
          return True
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False

  async def blbBookList(self):
    try:
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
          await db.execute('SELECT * from `blb`')
          l = await db.fetchall()
          await db.close()
          
          return l
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False

  async def blbUpdated(self, book, chapter):
    try:
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
          await db.execute('UPDATE `blb` SET `blb`.chapter=%s WHERE `blb`.id=%s', (chapter,book))
          await db.close()
          
          return True
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False


  async def biliList(self):
    try:
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
          await db.execute('SELECT * from `bili`')
          l = await db.fetchall()
          await db.close()
          
          return l
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False

  async def biliDynamicUpdated(self, user, did):
    try:
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
          await db.execute('UPDATE `bili` SET `bili`.did=%s WHERE `bili`.id=%s', (did,user))
          await db.close()
          
          return True
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False

  async def biliLiveUpdated(self, user, stat):
    try:
      async with self.pool.acquire() as mydb:
        async with mydb.cursor() as db:
          await db.execute('UPDATE `bili` SET `bili`.live=%s WHERE `bili`.id=%s', (stat,user))
          await db.close()
          
          return True
    except Exception:
      print(time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime()) + '[ERROR]' + traceback.format_exc())
      return False