import math
import time
import sqlite3
from flask import url_for
import re


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

    def addPost(self, title, text, url):
        sql = '''INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)'''
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM posts WHERE url LIKE '{url}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Url already in use")
                return False
            base = url_for('static', filename='img')
            text = re.sub(r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
                          "\\g<tag>" + base + "/\\g<url>>",
                          text)
            tm = math.floor(time.time())
            self.__cur.execute(sql, (title, text, url, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error occurred during adding post into db"+str(e))
            return False
        return True

    def getPost(self, url):
        sql = f"SELECT title, text FROM posts WHERE url LIKE '{url}' LIMIT 1"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error occurred during receiving single post from db"+str(e))
        return (False, False)

    def getPosts(self):
        sql = '''SELECT id, title, text, url FROM posts ORDER BY time DESC'''
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except:
            print('Error occurred during receiving posts from db')
        return []

    def addUser(self, username, email, password):
        sql = '''INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)'''

        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'")
            res = self.__cur.fetchone()
            if res['count'] > 0:
                print("Email already in use")
                return False

            tm = math.floor(time.time())
            self.__cur.execute(sql, (username, email, password, tm))
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error occurred during adding user into db"+str(e))
            return False
        return True


    def getUser(self, user_id=None, email=None):
        if email is not None:
            sql = f"SELECT * FROM users WHERE email LIKE '{email}' LIMIT 1"
        elif user_id is not None:
            sql = f"SELECT * FROM users WHERE id LIKE '{user_id}' LIMIT 1"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print("Error occurred during receiving user from db"+str(e))
        return False

    def updateUserPhoto(self, img, user_id):
        if not img:
            return False

        sql = "UPDATE users SET photo = ? WHERE id = ?"
        try:
            binary = sqlite3.Binary(img)
            self.__cur.execute(sql, (binary, user_id))
            self.__db.commit()
        except sqlite3.Error as e:
            print('Error'+str(e))
            return False
        return True
