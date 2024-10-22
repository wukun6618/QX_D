import requests
from datetime import datetime

class c():
    pass
classlocal = c()

classlocal.trade_direction  = 'kong' #duo #kong
classlocal.code             = 'SA00.SF'
classlocal.kindextime       = '20241014135000'
classlocal.timetype         = '15m'
classlocal.tradetype        = 'open'  #open #close
classlocal.tradedata        = ''
classlocal.stop             = 123
classlocal.takeprofit        = 565656

classlocal.last_price       = 555
classlocal.profit           = -99
classlocal.mediumprice      = 555
classlocal.tradestatus      = ''
classlocal.modle            = 'TPDYX'
classlocal.URLopen          = 'https://open.feishu.cn/open-apis/bot/v2/hook/fb5aa4f9-16b9-49f2-8e3b-2583ec3f3e3e'
classlocal.URLclose         = 'https://open.feishu.cn/open-apis/bot/v2/hook/fb5aa4f9-16b9-49f2-8e3b-2583ec3f3e3e'
def open_payload_set(modle,trade_direction,tradedata,lastprice,stop,takeprofit,mediumprice):
    if trade_direction == 'duo':
        Head_color = 'Purple'
    else:
        Head_color = 'Orange'
    # 构建卡片消息
    card_message = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": False },
                "header": {"template":     "{}".format(Head_color), "title": {"tag": "plain_text", "content": "{}".format(tradedata),}},

            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content":"modle         :{}".format(modle),
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content":"lastprice      :{}".format(lastprice),
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content":"mediumprice :{}".format(mediumprice),
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content":"stop            :{}".format(stop),
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content":"takeprofit       :{}".format(takeprofit),
                    }
                }

            ]
        }
    }
    return card_message


def close_payload_set(modle,tradedata,lastprice,stop,takeprofit,profit):
    if profit >= 0 :
        Head_color = 'red'
    else :
        Head_color = 'green'
    # 构建卡片消息
    card_message = {
        "msg_type": "interactive",
        "card": {
            "config": {
                "wide_screen_mode": False },
                "header": {"template":     "{}".format(Head_color), "title": {"tag": "plain_text", "content": "{}".format(tradedata),}},
            "elements": [
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content":"modle      :{}".format(modle),
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content":"lastprice   :{}".format(lastprice),
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content":"Stop        :{}".format(stop),
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content":"takeprofit   :{}".format(takeprofit),
                    }
                },
                {
                    "tag": "div",
                    "text": {
                        "tag": "lark_md",
                        "content":"profit       :{}".format(profit),
                    }
                }

            ]
        }
    }
    return card_message

# 向飞书机器人发送卡片消息和天气
def send_message_to_feishu(classlocal):
    # 设置请求头,指定消息格式为JSON
    # 飞书自定义机器人
    '''
    classlocal.trade_direction  = 'close' #duo #kong
    classlocal.code             = 'SA00.SF'
    classlocal.kindextime       = '20241014135000'
    classlocal.timetype         = '15m'
    classlocal.tradetype        = 'open'  #open #close
    '''
    tradestatus             = classlocal.tradestatus 
    code                    = classlocal.code 
    date_string             = classlocal.kindextime
    date_object             = datetime.strptime(date_string, "%Y%m%d%H%M%S")
    # 转换回字符串
    new_date_string         = date_object.strftime("%Y-%m-%d %H:%M")
    kindextime              = new_date_string
    timetype                = classlocal.timetype
    trade_direction         = classlocal.trade_direction # 
    tradetype               = classlocal.tradetype       # 

    stop                    = classlocal.stop
    takeprofit               = classlocal.takeprofit
    lastprice               = classlocal.last_price
    profit                  = classlocal.profit
    modle                   = classlocal.modle
    #duo
    if trade_direction == 'duo':
        #open
        if tradetype == 'open':
            mediumprice  = (lastprice - stop)/2 + stop
            opentype     = 'open'
            tradedata    = opentype +' '+ trade_direction +' '+ code + ' '+ timetype + ' ' + kindextime + ' ' + tradestatus
            payload      = open_payload_set(modle,trade_direction,tradedata,lastprice,stop,takeprofit,mediumprice)
            url1             = classlocal.URLopen
        #close
        else:
            opentype     = 'close'
            tradedata    = opentype +' '+ trade_direction +' '+ code + ' '+ timetype + ' ' + kindextime + ' ' + tradestatus
            payload      = close_payload_set(modle,tradedata,lastprice,stop,takeprofit,profit)
            url1             = classlocal.URLclose
    #kong
    else :
                #open
        if tradetype == 'open':
            mediumprice  = (stop - lastprice)/2 + lastprice
            opentype     = 'open'
            tradedata    = opentype +' '+ trade_direction +' '+ code + ' '+ timetype + ' ' + kindextime + ' ' + tradestatus
            payload      = open_payload_set(modle,trade_direction,tradedata,lastprice,stop,takeprofit,mediumprice)
            url1             = classlocal.URLopen
        #close
        else:
            opentype     = 'close'
            tradedata    = opentype +' '+ trade_direction +' '+ code + ' '+ timetype + ' ' + kindextime + ' ' + tradestatus
            payload      = close_payload_set(modle,tradedata,lastprice,stop,takeprofit,profit)
            url1             = classlocal.URLclose

    headers1                = {'Content-Type': 'application/json'}
    try:
        response                = requests.post( url = url1, json = payload, headers = headers1)  # 发送POST请求
    
        if response.status_code == 200:  # 判断返回状态码是否为200(请求成功)
            response.raise_for_status()  # 如果响应状态码不是200，主动抛出异常
            #print("消息发送成功：", response.text)
        else:
            print('发送失败')
    except requests.exceptions.RequestException as e:
        print("发送失败：", e)
        
send_message_to_feishu(classlocal)




