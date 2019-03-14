
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import time
import urllib
import urllib2
import json
from flask import Flask
from flask import abort
from flask import redirect

def get_token():
    db = MySQLdb.connect("localhost", "root", "1111", "wx_server", charset='utf8' )
    cursor = db.cursor()
    try:
        cursor.execute("SELECT * FROM wx_token")
        results = cursor.fetchall()
        row0 = results[0]
        tokenid = row0[0]
        token = row0[1]
        tokentime = row0[2]
        now = int(time.time())
        interval = now - tokentime
        if interval > 7150:
            return ''
        else:
            return token
    except:
        print "Error: unable to fecth data"
        return ''
    finally:
        cursor.close()
        db.close()

def get_newToken():
    urlStr = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxe4db97e34725a529&secret=ff13dab2c190bd889f0133aae7b05365'
    resp = urllib.urlopen(urlStr)
    jsonData = json.loads(resp.read())
    return jsonData['access_token']
    # return '19_NE9Xb_1yJpuld7ATNMxgeCTTqNowrkclz4-GH2K931zZOvjpB6CNDb5F40qgqXi-0PoxrUOnGgsvM57u0Lk4eQIk0VBGq8u9eDeOiKiTwuOOucAxl6_LFNRQBkDZ9PbgvvWWmI1AIW-5n0x3WOAgAAASKW'

def save_token(token):
    if len(token) == 0:
        return
    db = MySQLdb.connect("localhost", "root", "1111", "wx_server", charset='utf8' )
    cursor = db.cursor()
    try:
        now = int(time.time())
        sql = "UPDATE wx_token SET token = '%s',time = %d WHERE id = 1" % (token,now)
        cursor.execute(sql)
        db.commit()
        print "save token"
    except:
        print "Error: unable to update token"
    finally:
        cursor.close()
        db.close()

def check_token():
    token = get_token()
    if len(token) == 0:
        print "get_newToken"
        token = get_newToken()
        save_token(token)
    return token

def get_ticket(proInfo):
    token = check_token()
    if len(token) == 0:
        return ''
    urlStr = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % (token) 
    data = '{"expire_seconds": 604800, "action_name": "QR_STR_SCENE", "action_info": {"scene": {"scene_str": "%s"}}}' % (proInfo)
    req = urllib2.Request(urlStr,data)
    resp = urllib2.urlopen(req)
    jsonData = json.loads(resp.read())
    db = MySQLdb.connect("localhost", "root", "1111", "wx_server", charset='utf8' )
    cursor = db.cursor()
    try:
        now = int(time.time())
        sql = "INSERT INTO wx_ticket(ticket) VALUES('%s')" % (jsonData['ticket'])
        cursor.execute(sql)
        db.commit()
        print "save ticket"
    except:
        print "Error: unable to save ticket"
    finally:
        cursor.close()
        db.close()
    return jsonData['ticket']

def post_alarm(alarm):
    token = check_token()
    if len(token) == 0:
        return ''
    urlStr = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % (token)
    first = {"value":alarm['title'],"color":"#173177"}
    keyword1 = {"value":alarm['type'],"color":"#173177"}
    keyword2 = {"value":alarm['time'],"color":"#173177"}
    remark = {"value":alarm['remark'],"color":"#173177"}
    tempdata = {'first':first,'keyword1':keyword1,'keyword2':keyword2,'remark':remark}
    alarmdata = {'touser':'o-2dJ6GvwCkzBeNeuyPInfgoBBGs','template_id':'ecVrsXvge7j51qdCvyr4JD4lZd7u4n9TD5RZbKufElY','url':'http://39.106.178.186/click','data':tempdata}
    # print(alarmdata)
    jsonalarm = json.dumps(alarmdata)
    # print(jsonalarm)
    req = urllib2.Request(urlStr,jsonalarm)
    resp = urllib2.urlopen(req)
    jsonData = json.loads(resp.read())
    print(jsonData)
