#coding:utf-8
__author__ = 'xp'

import MySQLdb
from Question import Question

class DataBaseLinker:
    __connect = None
    __dataBaseLinker = None

    def __init__(self):
        """
        @:argument 连接至服务器数据库
        @:param 无
        """
        DataBaseLinker.__connect = MySQLdb.connect( host='localhost', port=3306, user='root', passwd='085850', db='XPOJ', charset="utf8")

    def otherLinker(self, host, port, user, passwd, db):
        """
        @:argument 连接到另外的服务踌躇
        @:param host
            @:type string
            @:argument 目的数据库的ip
        @:param port
            @:type string
            @:argument 目的服务器的端口
        @:param user
            @:type string
            @:argument 连接数据库的用户名
        @:param passwd
            @:type string
            @:argument 连接数据库的密码
        @:param db
            @:type string
            @:argument 连接的数据库名
        """
        DataBaseLinker.__connect = MySQLdb.connect( host=host, port=port, user=user, passwd=passwd, db=db )

    def closeLink(self):
        """
        :return: None
        """
        DataBaseLinker.__connect.close()

    def execute(self, sql):
        """
        :param sql: 要执行的sql语名
        :return: 数据库中提出的结果，查讯失败为None
        """
        result = None
        try:
            cur = DataBaseLinker.__connect.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            cur.execute(sql)
            result = cur.fetchall()
            DataBaseLinker.__connect.commit()
            cur.close()
        except Exception, e:
            print e
        finally:
            return result

    @staticmethod
    def getInstance():
        """
        :return: DataBaseLinker的单例
        """
        if DataBaseLinker.__dataBaseLinker == None:
            DataBaseLinker.__dataBaseLinker = DataBaseLinker()
        return DataBaseLinker.__dataBaseLinker