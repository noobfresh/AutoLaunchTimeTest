#!/usr/bin/python
# coding=utf-8
import sqlite3

con = ''
cur = ''


def connect(host):
    global con
    global cur
    try:
        con = sqlite3.connect(host)
        cur = con.cursor()
        return True
    except Exception, e:
        print(u'数据库连接失败! e = ' + repr(e))
        return False


def update(table, cname, cvalue, name, value, commit=True):
    global con
    sql = 'update ' + table + ' set ' + name + "='" + value + "' where " + cname + "='" + cvalue + "'"
    try:
        query(sql)
        if commit:
            con.commit()
        return True
    except Exception, e:
        print ('e = ' + repr(e))
        return False


def create(table, value, main=False, commit=True):
    global con
    global cur
    sql = 'create table ' + table + '('
    if main:
        sql += main + ' INTEGER PRIMARY KEY AUTOINCREMENT,'
    name = []
    type = []
    for n in value.keys():
        name.append(n)
    for n in value.values():
        type.append(n)
    i = 0
    while i < len(value):
        if i == len(value) - 1:
            sql += name[i] + ' ' + type[i].upper() + ')'
        else:
            sql += name[i] + ' ' + type[i].upper() + ','
        i += 1
    try:
        query(sql)
        if commit:
            con.commit()
        return True
    except Exception, e:
        print ('e = ' + repr(e))
        return False


def insert(table, value, commit=True):
    global con
    sql = 'insert into ' + table + '('
    i = 0
    for n in value.keys():
        i = i + 1
        if i != len(value):
            sql = sql + n + ','
        else:
            sql = sql + n + ')values('
    i = 0
    for n in value.values():
        i = i + 1
        if i != len(value):
            sql = sql + "'" + n + "'" + ','
        else:
            sql = sql + "'" + n + "'" + ')'
    try:
        query(sql)
        if commit:
            con.commit()
        return True
    except Exception, e:
        print ('e = ' + repr(e))
        return False


def select(table, name, vname, vvalue):
    global cur
    sql = 'select ' + name + ' from ' + table + ' where ' + vname + "='" + vvalue + "'"
    try:
        query(sql)
    except Exception, e:
        print ('e = ' + repr(e))
        return None
    try:
        re = cur.fetchall()
        return str(re[0][0])
    except Exception, e:
        print ('e = ' + repr(e))
        return None


def query(sql):
    global cur
    return cur.execute(sql)


def delete(table, vname, vvalue, commit=True):
    global con
    sql = 'DELETE  FROM  ' + table + ' WHERE  ' + vname + "='" + vvalue + "'"
    try:
        query(sql)
        if commit:
            con.commit()
        return True
    except Exception, e:
        print ('e = ' + repr(e))
        return False


def drop(table):
    sql = 'DROP TABLE  ' + table
    try:
        query(sql)
        return True
    except Exception, e:
        print ('e = ' + repr(e))
        return False


def close():
    global con
    global cur
    cur.close()
    con.commit()
    con.close()
