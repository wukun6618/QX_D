import requests
from datetime import datetime

class c():
    pass
classlocal = c()

classlocal.trade_direction  = 'duo' #duo #kong
classlocal.code             = 'SA00.SF'
classlocal.kindextime       = '20241014135000'
classlocal.timetype         = '15m'
classlocal.tradetype        = 'open'  #open #close
classlocal.tradedata        = ''
classlocal.stop             = 123
classlocal.takprofit        = 565656

classlocal.last_price       = 555
classlocal.profit           = -99
classlocal.middleprice      = 555
classlocal.tradestatus      = 'success'
classlocal.modle            = 'TPDYX'
classlocal.URLopen          = 'https://open.feishu.cn/open-apis/bot/v2/hook/fb5aa4f9-16b9-49f2-8e3b-2583ec3f3e3e'
classlocal.URLclose         = 'https://open.feishu.cn/open-apis/bot/v2/hook/fb5aa4f9-16b9-49f2-8e3b-2583ec3f3e3e'

def open_payload_set(modle,trade_direction,tradedata,lastprice,stop,takprofit,middleprice):

    if trade_direction == 'duo':
        Head_color = 'Purple'
    else:
        Head_color = 'Orange'
    print(f'Head_color:{Head_color}')
    print(f'tradetype:{trade_direction}')
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {"template":  "{}".format(Head_color), "title": {"tag": "plain_text", "content": "{}".format(tradedata),}},
            "elements": [
                {
                    "tag": "column_set",
                    "flex_mode": "none",
                    "background_style": "default",
                    "columns": [
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "modle:\n{}".format(modle),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "lastprice\n{}".format(lastprice),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "middleprice\n{}".format(middleprice),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "stop：\n{}".format(stop),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "takprofit：\n{}".format(takprofit),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                    ]
                }
            ]
        }
    }  # 替换为实际的JSON消息
    return payload

def close_payload_set(modle,tradedata,lastprice,stop,takprofit,profit):
    if profit >= 0 :
        Head_color = 'red'
    else :
        Head_color = 'green'
    payload = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {"template":  "{}".format(Head_color), "title": {"tag": "plain_text", "content": "{}".format(tradedata),}},
            "elements": [
                {
                    "tag": "column_set",
                    "flex_mode": "none",
                    "background_style": "default",
                    "columns": [
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "modle:\n{}".format(modle),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "type\n{}".format(type),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "Stop：\n{}".format(stop),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "takprofit：\n{}".format(takprofit),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "lastprice\n{}".format(lastprice),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "tag": "column",
                            "width": "weighted",
                            "weight": 1,
                            "vertical_align": "top",
                            "elements": [
                                {
                                    "tag": "column_set",
                                    "flex_mode": "none",
                                    "background_style": "grey",
                                    "columns": [
                                        {
                                            "tag": "column",
                                            "width": "weighted",
                                            "weight": 1,
                                            "vertical_align": "top",
                                            "elements": [
                                                {
                                                    "tag": "markdown",
                                                    "content": "profit\n{}".format(profit),
                                                    "text_align": "center"
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        },
                    ]
                }
            ]
        }
    }  # 替换为实际的JSON消息
    return payload
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
    takprofit               = classlocal.takprofit
    lastprice               = classlocal.last_price
    profit                  = classlocal.profit
    modle                   = classlocal.modle
    #duo
    if trade_direction == 'duo':
        #open
        if tradetype == 'open':
            middleprice  = (lastprice - stop)/2 + stop
            opentype     = 'open'
            tradedata    = opentype +' '+ trade_direction +' '+ code + ' '+ timetype + ' ' + kindextime + ' ' + tradestatus
            payload      = open_payload_set(modle,trade_direction,tradedata,lastprice,stop,takprofit,middleprice)
            url1             = classlocal.URLopen
        #close
        else:
            opentype     = 'close'
            tradedata    = opentype +' '+ trade_direction +' '+ code + ' '+ timetype + ' ' + kindextime + ' ' + tradestatus
            payload      = close_payload_set(modle,tradedata,lastprice,stop,takprofit,profit)
            url1             = classlocal.URLclose
    #kong
    else :
                #open
        if tradetype == 'open':
            middleprice  = (stop - lastprice)/2 + lastprice
            opentype     = 'open'
            tradedata    = opentype +' '+ trade_direction +' '+ code + ' '+ timetype + ' ' + kindextime + ' ' + tradestatus
            payload      = open_payload_set(modle,trade_direction,tradedata,lastprice,stop,takprofit,middleprice)
            url1             = classlocal.URLopen
        #close
        else:
            opentype     = 'close'
            tradedata    = opentype +' '+ trade_direction +' '+ code + ' '+ timetype + ' ' + kindextime + ' ' + tradestatus
            payload      = close_payload_set(modle,tradedata,lastprice,stop,takprofit,profit)
            url1             = classlocal.URLclose

    headers1                = {'Content-Type': 'application/json'}
    response                = requests.post( url = url1, json = payload, headers = headers1)  # 发送POST请求
    if response.status_code == 200:  # 判断返回状态码是否为200(请求成功)
        print('发送成功')
    else:
        print('发送失败')

send_message_to_feishu(classlocal)