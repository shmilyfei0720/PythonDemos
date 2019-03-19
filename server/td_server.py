#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json

def td_userlogin(name,pwd):
    ret = ''
    if name == 'chen' and pwd == 'test1234':
        ret = {"ret":0,"content":"success"}
    else:
        ret = {"ret":-1,"content":"failed"}
    jsonData = json.dumps(ret)
    return jsonData