import requests
class c():
    pass
classlocal = c()
classlocal.messagetype      = 'KONG'
classlocal.code             = 'SA00.SF'
classlocal.kindextime       = '20241014135000'
classlocal.timetype         = '15m'
classlocal.type             = 'Buy_open'
classlocal.stop             = 123
classlocal.takprofit        = 565656
classlocal.URL1             = 'https://open.feishu.cn/open-apis/bot/v2/hook/fb5aa4f9-16b9-49f2-8e3b-2583ec3f3e3e'

def payload_set(code,kindextime,type,stop,takprofit):
    payload1 = {
        "msg_type": "interactive",
        "card": {
            "config": {"wide_screen_mode": True},
            "header": {"template": "red", "title": {"tag": "plain_text", "content": "{}".format(type),}},
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
                                                    "content": "Code:\n{}".format(code),
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
                                                    "content": "Kindextime：\n{}".format(kindextime),
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
                                                    "content": "Takprofit：\n{}".format(takprofit),
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
    return payload1
# 向飞书机器人发送卡片消息和天气
def send_message_to_feishu(classlocal):
    # 设置请求头,指定消息格式为JSON
    # 飞书自定义机器人
    type                    = classlocal.type +' '+ classlocal.timetype +' '+ classlocal.code 
    messagetype             = classlocal.messagetype 
    url_open                = classlocal.URL1
    code                    = classlocal.code 
    kindextime              = classlocal.kindextime
    stop                    = classlocal.stop 
    takprofit               = classlocal.takprofit
    headers1                = {'Content-Type': 'application/json'}
    payload1                = payload_set(code,kindextime,type,stop,takprofit)
    response                = requests.post(url=url_open, json=payload1, headers=headers1)  # 发送POST请求
    if response.status_code == 200:  # 判断返回状态码是否为200(请求成功)
        print('发送成功')
    else:
        print('发送失败')

send_message_to_feishu(classlocal)