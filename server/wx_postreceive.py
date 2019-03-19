#!/usr/bin/python
# -*- coding: UTF-8 -*-

import xml.sax  
import xml.sax.handler  
  
class XMLHandler(xml.sax.handler.ContentHandler):  
    def __init__(self):  
        self.buffer = ""                    
        self.mapping = {}                  
  
    def startElement(self, name, attributes):  
        self.buffer = ""                    
  
    def characters(self, data):  
        self.buffer += data                      
  
    def endElement(self, name):  
        self.mapping[name] = self.buffer           
  
    def getDict(self):  
        return self.mapping 

def check_data(xml_data):
    print(xml_data)
    xh = XMLHandler()  
    xml.sax.parseString(xml_data, xh)  
    ret = xh.getDict()
    openid = ret['FromUserName']
    print "openid:%s" % (openid)
    ticket = ret['Ticket']
    print "ticket :%s" % (ticket)
    EventKey = ret['EventKey']
    print "eventkey:%s" % (EventKey)
    return "success"


# <xml><ToUserName><![CDATA[gh_db41c35f6bd7]]></ToUserName>
# <FromUserName><![CDATA[o-2dJ6GvwCkzBeNeuyPInfgoBBGs]]></FromUserName>
# <CreateTime>1552211256</CreateTime>
# <MsgType><![CDATA[event]]></MsgType>
# <Event><![CDATA[SCAN]]></Event>
# <EventKey><![CDATA[testst12342]]></EventKey>
# <Ticket><![CDATA[gQGf8DwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyWWlIUnNJWERkOUUxeTluZXhzY2cAAgQJ3YRcAwSAOgkA]]></Ticket>
# </xml>

