from flask import Flask
from flask import abort
from flask import redirect
from flask import request
import wx_server
import wx_postreceive

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

@app.route('/ticket',methods=['GET'])
def ticket():
    info = request.args.get('productinfo')
    urlStr = "https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s" % (wx_server.get_ticket(info))
    return urlStr
    #return wx_server.get_ticket(info)

@app.route('/wxreceiver',methods=['GET','POST'])
def receive():
    if request.method == 'POST':
        return wx_postreceive.check_data(request.data)
    else:
        echoStr = request.args.get('echostr')
        print "GET %s" % (request.data)
        return echoStr

@app.route('/testAlarm',methods=['GET'])
def testAlarm():
    title = request.args.get('title')
    atype = request.args.get('type')
    atime = request.args.get('time')
    remark = request.args.get('remark')
    alarm = {'title':title,'type':atype,'time':atime,'remark':remark}
    wx_server.post_alarm(alarm)
    return 'success'

@app.route('/click')
def click():
    return '<h1>Hello World!</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
