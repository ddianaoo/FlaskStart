import math, time, sqlite3


class FDataBase:

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Error occurred during receiving mainmenu from db')
        return []

    def addPost(self, title, text):
        sql = '''INSERT INTO posts VALUES(NULL, ?, ?, ?)'''
        try:
            tm = math.floor(time.time())
            self.__cur.execute(sql, (title, text, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error occurred during adding post into db"+str(e))
            return False
        return True

    def getPost(self, id_post):
        sql = f"SELECT title, text FROM posts WHERE id = {id_post} LIMIT 1"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error occurred during receiving single post from db"+str(e))
        return (False, False)

    def getPosts(self):
        sql = '''SELECT id, title, text FROM posts ORDER BY time DESC'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Error occurred during receiving posts from db')
        return []