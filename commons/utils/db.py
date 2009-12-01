# vim:fileencoding=utf8
from datetime import date,datetime,timedelta
import MySQLdb
from MySQLdb.cursors import *
from django.conf import settings

import MySQLdb.connections

def _get_connection(con):
    """
    Connectionオブジェクトを取り出す
    Djangoはラップしているため
    """
    from mysql_replicated2.base import DatabaseWrapper

    connection = None
    if isinstance(con, MySQLdb.connections.Connection):
        connection = con
    elif isinstance(con, DatabaseWrapper):
        #con._cursor(settings) # コネクションを取得
        con._cursor()
        connection = con.connection
    else : # for django connection object
        connection = con.connection
    return connection

def select(con, sql, params=None, instance=None):
    connection = _get_connection(con)

    default_cur = connection.cursorclass
    connection.cursorclass=DictCursor
    rows = None
    try:
        cur = connection.cursor()

        cur.execute(sql,params)
        rows = cur.fetchall()
        cur.close()
    finally:
        connection.cursorclass=default_cur

    if not rows or not instance:
        return rows and rows or ()

    l = []
    for row in rows:
        obj = instance()
        for key,val in row.iteritems():
            setattr(obj,key,val)
        l.append(obj)
    return l

def update(con, sql, params=None):
    """ for (update|insert|delete) statement """
    cur = con.cursor()
    cur.execute(sql,params)
    return cur.rowcount

def strftime_for_db(dateobj):
    """
    """
    if not isinstance(dateobj,date):
        raise TypeError('%s is not datetime.date type.' % (type(dateobj)) )

    if isinstance(dateobj, datetime):
        return dateobj.strftime('%Y-%m-%d %H:%M:%S')
    else :
        return dateobj.strftime('%Y-%m-%d')


    
    

#con = MySQLdb.connect(db="test01", host="localhost", port=3306, user="root", passwd="")
#a = select(con, "select * from test where id=%s" ,["101"])
#print a
