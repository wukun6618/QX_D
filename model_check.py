#encoding:gbk

import pandas as pd
import numpy as np
import datetime as dt
from datetime import datetime
from iQuant_functools import *
import json
import requests
import time
import configparser
import xml.etree.ElementTree as ET
from xml.dom.minidom import parse
import os
import talib

pd.set_option('expand_frame_repr', False)  #不换行
pd.set_option('display.max_rows', 5000)     #最多显示数据的行数
pd.set_option('display.unicode.ambiguous_as_wide', True) # 中文字段对齐
pd.set_option('display.unicode.east_asian_width', True)
pd.set_option('display.float_format', lambda x: '%.3f' % x) # dataframe格式化输出

list_data_values                    = []#[[0,0, 0, 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
ATR_LEN                             = 5
YKB                                 = 3
DEFAULT_NUMBER_OF_POINTS            = 0.02

class b():
    pass
classlocal = b()

classlocal.printmoney_en            = 1
classlocal.printlocalhold_en        = 1
classlocal.sell_debug_inf_en        = 0
classlocal.checklist_debug_en       = 0 #打印本地自选股行情
classlocal.Index_time_debug_en      = 0
classlocal.Trade_init_debug_en      = 0 #
classlocal.model_df_level2_debug_en = 0 #模型选出列表购买列表
classlocal.JLZY_debug_en            = 0 #棘轮止盈打印
classlocal.huicedebug_en            = 0 #回测的时候打开，运行的时候关闭
classlocal.mp_debug_origin_en       = 0 #模型选出打印
classlocal.ZXCS_debug_en            = 1 #执行周期和次数打印
classlocal.h_data_debug_en          = 0 #打印执行选股前的行情数据

classlocal.RED_TPDYX_debug_en           = 0 #debug信息打印
classlocal.RED_TPDYX_STOP_DEBUG         = 0 #行情止损打印

classlocal.GREEN_TPDYX_debug_en           = 0 #debug信息打印
classlocal.GREEN_TPDYX_STOP_DEBUG         = 0 #行情止损打印
classlocal.check_list               = ['SA00.ZF']
classlocal.check_list_debug_en      = 0 #自定义行情品种

# -------------------------------------------#
# 数据类型
classlocal.p                        = 0                 #绘图点用
classlocal.count                    = 0                 # 01 记录定时函数执行次数
classlocal.Period_Type              = '15m'
classlocal.trade_buy_record_dict    = {}                # 02 买入交易记录
classlocal.buy_code_count           = 0                 # 03 风控函数，防止买入过多。
classlocal.Reflash_buy_list         = 1
# 0：无需刷新stock_level1_lsit 1:需要重新刷新stock_level1_lsit
classlocal.ATR_open_Length          = 4*ATR_LEN         # 图标bar线数量为20

classlocal.ATR_close_Length         = 3*ATR_LEN         # 图标Bar线数量为10
classlocal.M_HL                     = 3*ATR_LEN         # 中轴线参数设置为10

classlocal.MA_middle_length         = 184#99            # 中均线长度
classlocal.MA_long_length           = 215#144           # 长均线长度

classlocal.ATR                      = 0  # ATR平均真实波幅
classlocal.ATR_BuyK                 = 0  # 开多时ATR数值
classlocal.ATR_SellK                = 0  # 开空时ATR数值
classlocal.Price_BuyK               = 0  # 开多时的价格
classlocal.Price_SellK              = 0  # 开空时的价格
classlocal.close                    = 0  #
classlocal.open                     = 0  #
classlocal.low                      = 0  #
classlocal.highmax                  = 0  #
classlocal.lowmin                   = 0  #
classlocal.szxfd                    = 0.018 #
classlocal.modul_length             = 240 #多少日
#雕
classlocal.diao_en                  = 0
classlocal.diao_length              = 34
classlocal.diao                     = 0  #
classlocal.diaosp                   = 8888  #
#七星
classlocal.qxlck_en                 = 1
classlocal.qxlck_length             = 10    #多少日
classlocal.qxlck                    = 0
classlocal.qxlcksp                  = 8888

classlocal.qxdf                     = 0.03   #七星下跌幅度
classlocal.exzf                     = 0.0015 #七星二型最后一根阳线涨幅
#大阳线均线突破
classlocal.RED_TPDYX_en                 = 0
classlocal.RED_TPDYX                    = 0
classlocal.RED_TPDYXsp                  = 8888
classlocal.volume                   = 0
classlocal.selRED_TPDYX_stopcheck       = 0
classlocal.sellRED_TPDYX_time           = 16    #买入后多久执行

#大阳线均线突破
classlocal.GREEN_TPDYX_en                 = 1
classlocal.GREEN_TPDYX                    = 0
classlocal.GREEN_TPDYXsp                  = 8888
classlocal.volume                   = 0
classlocal.selGREEN_TPDYX_stopcheck       = 0
classlocal.sellGREEN_TPDYX_time           = 16    #买入后多久执行

#神零
classlocal.shenling_en              = 0
classlocal.shenling_length          = 10    #多少日
classlocal.shenling                 = 0
classlocal.shenlingsp               = 8888
classlocal.sldf                     = 0.043  #神零下跌幅度
classlocal.slsecondedf              = 0.005  #神零下跌幅度#0.008
################################################################################################
#1.总涨幅止盈
classlocal.Price_SellYA_Ratio       = 2    #涨到个点止盈,手动买入时生效
#2.时间止盈
classlocal.BarSinceEntrySet         = 200  #N天时间止损
#3.盈亏比预设
classlocal.Price_SetSellY_YKB       = YKB    #盈亏比设置为3
classlocal.Price_SetSellS           = DEFAULT_NUMBER_OF_POINTS  #默认止损,无论如何都会在
classlocal.Price_SetSellYratio      = DEFAULT_NUMBER_OF_POINTS*YKB  #
#3.5 盈亏比止盈触发后进行棘轮止盈
classlocal.Price_SellS1_ATRratio    = 15    #ATR棘轮止损默认
classlocal.Price_SellY1_ATRratio    = 0.01   #ATR 止盈 默认比例 越大约灵敏大
classlocal.TC_ATRratio              = 1.0


classlocal.Price_SellY              = 0     #棘轮止盈利开始价格
classlocal.Price_SellY1             = 0     #棘轮止盈止盈价格,根据ATR值相关

#classlocal.Price_SetSellY1          = 1     #
classlocal.Price_SellY_Flag         = 0     #第一阶段止盈达到
classlocal.TH_low                   = 5.9   #价格筛选下线单位元
classlocal.TH_High                  = 100    #价格筛选上线单位元
################################################################################################

classlocal.Kindex                   = 0     # 当前K线索引
classlocal.Kindex_time              = 0     # 当前K线对应的时间
classlocal.zf_lastK                 = 0     # 当前K线对应的涨幅
classlocal.buy_list                 = []    #买入列表
classlocal.sell_list                = []    #卖出列表
classlocal.LeftMoey                 = 1     #剩余资金
classlocal.LeftMoeyLast             = 0     #上次剩余
classlocal.Total_market_cap         = 0     #持仓次市值
classlocal.Total_market_capLast     = 0     #上次持仓次市值
classlocal.sp_type                  = 'NONE'
classlocal.eastmoney_zx_name        = ''
classlocal.eastmoey_stockPath       = ''
classlocal.eastmoney_user_buy_list  = ''
classlocal.eastmoney_zx_name_list   = ''
classlocal.stockPath_hold           = ''
classlocal.user_buy_list            = ''

classlocal.tradestatus      = ''
classlocal.trade_direction  = 'kong' #duo #kong
classlocal.code             = 'SA00.SF'
classlocal.kindextime       = '20241016093000'
classlocal.timetype         = '15m'
classlocal.tradetype        = 'open'  #open #close
classlocal.tradedata        = ''
classlocal.stop             = 0
classlocal.takprofit        = 0

classlocal.last_price       = 0
classlocal.profit           = 0
classlocal.middleprice      = 0
classlocal.tradestatus      = ''
classlocal.modle            = ''
classlocal.URLopen          = 'https://open.feishu.cn/open-apis/bot/v2/hook/763bec44-0f8e-447b-8341-2e567d7fd6a8'#'https://open.feishu.cn/open-apis/bot/v2/hook/fb5aa4f9-16b9-49f2-8e3b-2583ec3f3e3e'
classlocal.URLclose         = 'https://open.feishu.cn/open-apis/bot/v2/hook/763bec44-0f8e-447b-8341-2e567d7fd6a8'#'https://open.feishu.cn/open-apis/bot/v2/hook/fb5aa4f9-16b9-49f2-8e3b-2583ec3f3e3e'

# -------------------------------------------#
# -------------------------------------------#
# 判断类型
classlocal.BuyPK    = False  # 开多条件
classlocal.SellPK   = False  # 开空条件
classlocal.BuyAK    = False  # 加多条件
classlocal.SellAK   = False  # 加空条件
classlocal.BuyA     = False  # 加仓使能
classlocal.SellA    = False  # 加空使能
classlocal.BuyS     = False  # 多头止损
classlocal.SellS    = False  # 空头止损
classlocal.BuyY     = False  # 空头止盈
classlocal.SellY    = False  # 多头止盈
classlocal.ISfirst  = True   # 多头止盈

###################################start###########################################################################
#
###################################start###########################################################################
def init(ContextInfo):
    #---------------------------------------------------------------------------
    #*为了编译不报错定义了如下变量的初始值，
    #1.如果用实盘需要修改下面参数
    #2.实盘的时候可以将这些参数屏蔽掉从XML导入的控件输入初始值，
    #建议用这种方式设置交易初始值
    global Tradehistory
    global local_hold
    global classlocal

    global deleted_rows

    if classlocal.huicedebug_en != 1:
        if not ContextInfo.is_last_bar():
            return

    #current_hold = local_hold_data_frame_init()
    if classlocal.huicedebug_en :
        account             = 'test'
    else :
        account             = '510000000223'
    accountType             = 'FUTURE'
    eastmoey_stockPath      = 'C:\\eastmoney\\swc8\\config\\User\\9489316496536486\\StockwayStock.ini'
    stockPath_sell          = 'C:\\new_tdx\\T0002\\blocknew\\QX.blk'
    stockholdingpath        = 'C:\\Users\\wukun\\Desktop\\tradehistory\\datclasslocal1.csv'
    user_buy_list_path      = 'C:\\Users\\wukun\\Desktop\\tradehistory\\userbuylist.csv'
    stockrecord             = 'C:\\Users\\wukun\\Desktop\\tradehistory\\tradehistoryrecord.csv'
    Max_buynums             = 8

    M_Start_Time            = "09:25:00"
    M_End_Time              = "02:57:00"
    singel_zf_lastK         = 0.03
    eastmoney_user_buy_list = ['SFT']# ['FUTURE']
    '''
    eastmoney_zx_name_listt =['FT1','FT2','FT3','FT4','FT5','FT6','FT7',\
                              'FT8','FT9','FTA','FTB','FTC']
    '''
    eastmoney_zx_name_listt = ['FT1','FT2','FT3','FT4','FT5','FT6','FT7',\
                              'FT8','FT9']# ['FUTURE']
    #当前K线的对应的下标从0开始
    #---------------------------------------------------------------------------
    # 账号为模型交易界面选择账号
    ContextInfo.accID           = str(account)
    ContextInfo.accountType     = str(accountType).upper()
    ContextInfo.set_account(ContextInfo.accID)
    ContextInfo.val_TrueRange   =[]
    now_time                    = dt.datetime.now().strftime('%Y%m%d')
    #print(type(now_time))
    # 01_采用run_time定时驱动函数
    # ===========周期函数====================
    #print('\n',G_df)
    #print(f'\ninit执行: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
    # 周期函数 (每隔5S，执行MyHandlebar一次)
    current_time = (dt.datetime.now()).strftime('%Y%m%d%H%M') + '00'
    ContextInfo.run_time('MyHandlebar', '5nSecond', current_time, "SH")

    # 02_可调参数,从界面读取
    classlocal.eastmoey_stockPath    = eastmoey_stockPath          #买入股票路径
    classlocal.stockPath_sell        = stockPath_sell             #卖出股票路径
    classlocal.stockPath_hold        = stockholdingpath           #持仓保存路径
    classlocal.user_buy_list_path    = user_buy_list_path              #手动加自选的记录路径
    classlocal.stockPath_recordh     = stockrecord                #本地交易记录保存
    classlocal.max_buy_nums          = Max_buynums                #最大可买入股票数量
    #classlocal.max_singbuy_price     = max_singbuy_price          #单只最高买入最大金额
    #classlocal.buy_avail_rate        = Fundbal_AvailRate          #单只支票买入金额_(可用资金*classlocal.buy_avail_rate(0.10))

    classlocal.monitor_start_time    = M_Start_Time               #监控开始时间
    classlocal.monitor_end_time      = M_End_Time                 #监控开始时间
    classlocal.stockPath_sell        = stockPath_sell             #卖出股票路径
    #classlocal.Total_drawdown_ratio  = drawdown_ratio             #调整持仓交易总金额
    classlocal.zf_lastK              = singel_zf_lastK            #最后一日个股涨幅
    #classlocal.eastmoney_zx_name     = eastmoney_zx_name          #自选分组的名字
    classlocal.eastmoney_zx_name_list = eastmoney_zx_name_listt   #自选分组名字
    classlocal.eastmoney_user_buy_list = eastmoney_user_buy_list   #自选分组名字

    #从本地读取数据
    local_hold      = read_local_hold_data(classlocal.stockPath_hold,False)
    Tradehistory    = read_local_hold_data(classlocal.stockPath_recordh,False)
    if(classlocal.printlocalhold_en and not local_hold.empty):
        print(f'local_hold_INTI:\n{local_hold}')

    #查询当日委托记录
    found_list  = []
    orders      = get_trade_detail_data(ContextInfo.accID, ContextInfo.accountType, 'order')
    for order in orders:
        if  (order.m_strRemark in '读取通达信自选股下单示例') and \
            ('卖出'         not in order.m_strOptName)     and \
            (order.m_nOrderStatus in (48,49,50,51,52,53,55,56)):
            #order.m_strRemark("order.m_strRemark:",order.m_strRemark)
            #m_strInstrumentID 证券代码 m_strExchangeID：交易所
            #m_strOptName 买卖的标记    m_nOrderStatus 委托状态
            #m_nDirection ：EEntrustBS 类型,操作,多空,期货多空 股票买卖永远是48，其他的dir同理
            code = str(order.m_strInstrumentID)+'.'+str(order.m_strExchangeID)
            print(code,order.m_strOptName,order.m_nOrderStatus,order.m_nDirection)
            #code：000001.sz
            if code not in found_list:
                found_list.append(code)
            #委托数据更新到买入字典
            if code not in classlocal.trade_buy_record_dict.keys():
                classlocal.trade_buy_record_dict[code] = ['委托记录', '读取通达信自选股下单示例']
    #print(f'\n当日委托股票数据：{found_list}')
    #print('\nA：',A)
###################################start###########################################################################
#周期函数 (每隔5S，执行MyHandlebar一次)，'5nSecond'
###################################start###########################################################################
def MyHandlebar(ContextInfo):
    #print(f'\n周期函数执行handlebar:  第{classlocal.count}次')
    pass
###################################start###########################################################################
#主图Tick 触发
###################################start###########################################################################
def handlebar(ContextInfo):
    global Sell_list
    global account_df
    global handlebarcnt
    global Buy_df
    global model_df_level2

    if classlocal.huicedebug_en != 1:
        if not ContextInfo.is_last_bar():
            return
    if classlocal.ISfirst :
        classlocal.ISfirst      = False
        Sell_list               = []
        handlebarcnt            = 0
        # 获取当前账户的资金信息
        #测试的时候暂时放这里
        Buy_df                  = pd.DataFrame()
        model_df_level2         = pd.DataFrame()

    Kindex                      = ContextInfo.barpos
    classlocal.p                 = ContextInfo.get_net_value(Kindex)                         #该索引策略回测的净值，后面绘图使用
    index_time                  = timetag_to_datetime(ContextInfo.get_bar_timetag(Kindex),'%Y%m%d')

    if (classlocal.Period_Type[-1] == 'd'):
        index_time              = timetag_to_datetime(ContextInfo.get_bar_timetag(Kindex),'%Y%m%d')
    elif (classlocal.Period_Type[-1] == 'm'):
        index_time              = timetag_to_datetime(ContextInfo.get_bar_timetag(Kindex),'%Y%m%d%H%M%S')
    now_time                    = dt.datetime.now().strftime('%H:%M:%S')
    classlocal.Kindex           = Kindex
    classlocal.Kindex_time      = index_time
    if classlocal.Index_time_debug_en :
        print('\nKindex:',Kindex)
        print('index_time:',index_time)
        print('now_time:',now_time)
        print('classlocal.Period_Type:',classlocal.Period_Type)
    if Kindex > 1:
        #----------------------------------------------------------------------------------------------------------
        stockpath = classlocal.eastmoey_stockPath
        eastmoney_zx_name_list = classlocal.eastmoney_zx_name_list
        model_df_level2.drop(model_df_level2.index, inplace=True)

        for eastmoney_zx_name in eastmoney_zx_name_list:
            mdfl2 = Perform_stock_picks(ContextInfo,stockpath,eastmoney_zx_name,model_df_level2)
            if not mdfl2.empty:
                model_df_level2 = model_df_level2.append(mdfl2)
            else :
                model_df_level2 = model_df_level2
        if classlocal.ZXCS_debug_en:
            print(f'\n周期函数执行:  第{classlocal.count}次')
            print('K线时间:',index_time)
            print(f'\n当前时间: {dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        #------------------------------------------------------------------------------
        # 
        if classlocal.model_df_level2_debug_en and not model_df_level2.empty:
            print(f'model_df_level2—start:\n{model_df_level2}')
        if not model_df_level2.empty:
            for code in model_df_level2.index:
                if ContextInfo.is_suspended_stock(code):
                    model_df_level2.drop(code,inplace=True)
        if classlocal.model_df_level2_debug_en and not model_df_level2.empty:
            print(f'模型最终选出列表:\n{model_df_level2}')
        #--------------------------------------------------------------------------
    handlebarcnt +=1
###################################start###########################################################################
# 获取资金账号信息#
# 从服务器获取持仓信息
###################################start###########################################################################
def account_info(ContextInfo):
    account_df                                = pd.DataFrame()
    account_list                              = get_trade_detail_data(ContextInfo.accID, 'FUTURE', 'account')
    #列出数据和数据下标，一般用在 for 循环当中
    for index, obj in enumerate(account_list):
        account_df.loc[index, '总资产']        = obj.m_dBalance
        account_df.loc[index, '总市值']        = obj.m_dStockValue
        account_df.loc[index, '可用余额']      = obj.m_dAvailable
        account_df.loc[index, '当前交易日']    = obj.m_strTradingDate
        account_df.loc[index, '持仓盈亏']      = obj.m_dPositionProfit
    if classlocal.printmoney_en :
        print(f'资金账号信息:\n{account_df}')
    #syl = (obj.m_dBalance - 200000000)/200000000
    #print('收益率:',syl)
    return account_df
###################################start###########################################################################
#
###################################start###########################################################################
def QXLCK_checkout(MA1_short,MA1_short7,MA2_long,MA2_long7):
    close           = classlocal.close
    open            = classlocal.open
    low             = classlocal.low[-8:]
    high            = classlocal.high[-8:]
    length          = len(classlocal.high)
    highmax         = max(high)
    lowmin          = min(low)
    closes_opens    = close - open
    #均线朝上在回调位置在回调位置
    stop            = 0
    righthand       = 0
    righthand       =  (MA1_short > MA2_long) and (MA2_long > MA2_long7) and \
                       (lowmin   < MA1_short) and (highmax > MA1_short)
    righthand       = 1
    if righthand:
        yixing = (closes_opens[-1]>0) and (closes_opens[-2]<0) and (closes_opens[-3]>0) and \
                 (closes_opens[-4]>0) and (closes_opens[-5]<0) and (closes_opens[-6]<0) and (closes_opens[-7])<0

        erxing = (closes_opens[-1]>0) and (closes_opens[-2]<0) and (closes_opens[-3]<0) and (closes_opens[-4]>0) and \
                 (closes_opens[-5]<0) and (closes_opens[-6]<0) and (closes_opens[-7]<0)
        #意味着倒数两根线已经涨起来了
        #把止损推到最近两根线的最低点
        #erxing = 0
        if yixing:
            classlocal.qxlck    =  1
            #print('classlocal_1.Kindex ',classlocal.Kindex)
        elif erxing:
            classlocal.qxlck    =  0
            if (close[-1] - close[-2]) / close[-2] > classlocal.exzf:
                classlocal.qxlck    =  2
            #print('classlocal_2.Kindex ',classlocal.Kindex)
        else :
            classlocal.qxlck    =  0
            classlocal.qxlcksp  = 888
    else:
        classlocal.qxlck    = 0
        classlocal.qxlcksp  = 8888

    high_12 = max(high[-1],high[-2],high[-3],high[-4])
    low_12  = min(low[-1],low[-2],low[-3],low[-4])

    #上涨式的七星不做
    if(highmax <= high_12):
       # classlocal.qxlck    =  0
        stop = low_12
    else :
        stop = lowmin
    classlocal.qxlcksp  = stop
###################################start###########################################################################
#
###################################start###########################################################################
def RED_TPDYX_checkout(MA1_short,MA1_short7,MA2_long,MA2_long7):
    close           = classlocal.close
    open            = classlocal.open
    low             = classlocal.low[-20:]
    high            = classlocal.high[-10:]

    highmax         = max(high)    #classlocal.highmax                                           #6日最高点
    lowmin          = classlocal.lowmin                                                          #20日最低点

    DTCS            = (MA1_short > MA2_long) and (MA2_long > MA2_long7)                          #均线多头朝上
    YXSC            = (close[-2] > MA2_long) and (open[-2] < MA2_long) and (close[-2]>open[-2])  #阳线上穿
    JRZGD           = high[-2] >= highmax  #突破这天就是近日最高点
    low_12          = min(low[-2],low[-3],low[-4])


    righthand       = DTCS and YXSC and JRZGD
    if classlocal.RED_TPDYX_debug_en:
        if righthand:
            print("\nDTCS:",DTCS)
            print("\nYXSC:",YXSC)
            print("\nRZGD:",JRZGD)
            print("\nhigh[-2]:",high[-2])
            print("\nhigh:",high)
            print("\nhighmax:",highmax)
            print("\nlowmin:",lowmin)
        #print("\nselRED_TPDYX_stopcheck:",classlocal.selRED_TPDYX_stopcheck)

    classlocal.RED_TPDYX    =  0
    if (righthand):
        classlocal.RED_TPDYX    = 1
        classlocal.RED_TPDYXsp  = low_12
    else:
        classlocal.RED_TPDYX    = 0
        classlocal.RED_TPDYXsp  = 8888

###################################start###########################################################################
#回调低突破大阴线
###################################start###########################################################################
def GREEN_TPDYX_checkout(MA1_short,MA1_short7,MA2_long,MA2_long7):
    close           = classlocal.close
    open            = classlocal.open
    low             = classlocal.low[-10:]
    high            = classlocal.high[-20:]

    lowmin          = min(low)                                                  #10最低点
    highmax         = classlocal.high                                           #20日最高点

    DTCS            = (MA1_short < MA2_long) and (MA2_long < MA2_long7)         #均线多头朝下
    YXSC            = (close[-2] < MA2_long) and (open[-2] > MA2_long ) and \
                      (close[-2] < open[-2])                                    #阴线下穿破位

    JRZGD           = low[-2] <= lowmin                 #近日最低点
    high_12         = max(high[-2],high[-3],high[-4])

    righthand       = DTCS and YXSC and JRZGD
    if classlocal.GREEN_TPDYX_debug_en:
        if righthand:
            print("\nDTCS:",DTCS)
            print("\nYXSC:",YXSC)
            print("\nRZGD:",JRZGD)
            print("\nhigh[-2]:",high[-2])
            print("\nhigh:",high)
            print("\nhighmax:",highmax)
            print("\nlowmin:",lowmin)

    classlocal.GREEN_TPDYX    =  0
    if (righthand):
        classlocal.GREEN_TPDYX    = 1
        classlocal.GREEN_TPDYXsp  = high_12
    else:
        classlocal.GREEN_TPDYX    = 0
        classlocal.GREEN_TPDYXsp  = 8888
###################################start###########################################################################
#classlocal.shenling    = 0
#classlocal.shenlingsp  = 8888
###################################start###########################################################################
def YJSD_checkout():

    close   = classlocal.close
    open    = classlocal.open
    low     = classlocal.low
    highmax = classlocal.highmax
    lowmin  = classlocal.lowmin
    #获取个股昨日收盘价
    lastprice = close[-1]
    #昨日13日收盘价均值
    ma13      = np.mean(close[-classlocal.MAength1-1:-1])
    #昨日34日收盘价均值
    ma34      = np.mean(close[-classlocal.MAength2-1:-1])
    #如果13日均线上穿34日均线，且昨日收盘价位于13日均线之上
    righthand =  (lastprice > ma13) and (ma13 > ma34) and (close[-1] > open[-1])

    if (righthand):

        #最高到最低的跌幅
        FIRST_YANG    =   (close[-1] > open[-1])
        SENCOD_YIN    =   (close[-2] <= open[-2])
        THIRD_YIN     =   (close[-3] <= open[-3])
        FOURTH_YANG   =  (close[-4] > open[-4])

        FIRST_ZEHNFU  =  (open[-2] - close[-2]) / close[-2] <= 0.02
        SECOND_ZEHNFU =  (open[-3] - close[-3]) / close[-3] <= 0.02

        tiaojian1     = (close[-1] > open[-2]) and (close[-1] > open[-3]) and (close[-1] > close[-4])
        tiaojian2     = (close[-1] > open[-1]) and (close[-2] < open[-2]) and (close[-3] < open[-3]) and (close[-4] > open[-4])
        #print(tiaojian1,tiaojian2)
        #tiaojian3 = (open[-2] > close[-4]) and (open[-3] > close[-4])
        tiaojian3       = 1
        tiaojian4       = (low[-1] > open[-4] ) and (low[-2] > open[-4]) and (low[-3] > open[-4])

        diao            = FIRST_ZEHNFU and SECOND_ZEHNFU and tiaojian1 and \
                    tiaojian2    and tiaojian3     and tiaojian4 and \
                    FIRST_YANG   and SENCOD_YIN    and THIRD_YIN and FOURTH_YANG
        stop                = low[-4]
        classlocal.diao     = diao
        classlocal.diaosp   = stop
    else:
        classlocal.diao     = 0
        classlocal.diaosp   = 8888
###################################start###########################################################################
#
###################################start###########################################################################
def compare_values_min(value1, value2):
    if value1 < value2:
        return value1
    else:
        return value2
###################################start###########################################################################
#
###################################start###########################################################################
def compare_values_max(value1, value2):
    if value1 > value2:
        return value1
    else:
        return value2
###################################start###########################################################################
#
###################################start###########################################################################
def Calculate_SellY_According_to_SP(last_price,sp_price,Profit_loss_ratio):
    Price_SellY     = 0
    Price_SellY_t   = last_price+(last_price - sp_price)*Profit_loss_ratio
    Price_SellY     = decimal_places_are_rounded(Price_SellY_t,4)
    if (classlocal.Trade_init_debug_en):
        print(f'last_price\n,{last_price}')
        print(f'sp_price\n,{sp_price}')
        print(f'Price_SellY\n,{Price_SellY}')
    return Price_SellY

###################################start###########################################################################
#
###################################start###########################################################################
def Calculate_SellY_According_to_SP_Kong(last_price,sp_price,Profit_loss_ratio):
    Price_SellY     = 0
    Price_SellY_t   = last_price - (sp_price - last_price)*Profit_loss_ratio
    Price_SellY     = decimal_places_are_rounded(Price_SellY_t,4)
    if (classlocal.Trade_init_debug_en):
        print(f'last_price\n,{last_price}')
        print(f'sp_price\n,{sp_price}')
        print(f'Price_SellY\n,{Price_SellY}')

    return Price_SellY
###################################start###########################################################################
#执行选股
###################################start###########################################################################
def Perform_stock_picks(ContextInfo,stockpath,eastmoney_zx_name,compare_df):
    m_df_lv2 = pd.DataFrame()
    #index_time = classlocal.Kindex_time
    # 01_读取待买入股票数据
    check_list= parse_ini_file(stockpath,eastmoney_zx_name)
    if classlocal.check_list_debug_en:
        check_list = classlocal.check_list
    model_record_df     = pd.DataFrame()
    # ============ 执行时间 ======================
    if check_list:
        if check_list:
            model_record_dftt = model_process(ContextInfo,check_list)
            if classlocal.mp_debug_origin_en and not model_record_dftt.empty:
                print('\本地列表\n:',check_list)
                print('\n模型选出进入\n:',model_record_dftt)
                print('compare_df\n:',compare_df)
            if not model_record_dftt.empty:
                try:
                    if classlocal.Reflash_buy_list :
                        for code in model_record_dftt.index:
                            if code not in compare_df.index:
                                if m_df_lv2.empty:
                                   m_df_lv2 = model_record_dftt
                            else :
                                if code not in compare_df.index:
                                    if code not in m_df_lv2.index:
                                        m_df_lv2 = m_df_lv2+model_record_dftt
                except AttributeError:
                    print("索引不能转换为列表")
        else :
            m_df_lv2    = model_record_df
    if classlocal.mp_debug_origin_en and not model_record_dftt.empty:
        print('模型选出退出\n:',m_df_lv2)
    return m_df_lv2

###################################start###########################################################################
#Convert_the_market_data_type
#输入tradedatas得到一个arry,可以用来计算ATR和均线,当最小最有效时才计算
###################################start###########################################################################
def Convert_the_market_data_type(tradedatas,tradedata_lows,length):
    tradedata_nparry                = []
    tradedatas                      = tradedatas[-length:]
    lows                            = tradedata_lows[-length:]
    lowmin                          = lows.min()
    if lowmin > 0 :
        tradedata_nparry            = np.array(tradedatas)

    return tradedata_nparry
###################################start###########################################################################
#
###################################start###########################################################################
def model_process(ContextInfo,check_list):
    endtime_t = '000000'
    list_data_values    = [0,0,0,0]
    list_clolums        = ['Kindex','Tradingday','Price_SellS','Price_SellY','ATR_BuyK']
    dit1                = dict(zip(range(0,0), list_data_values))
    #转置矩阵
    G_df                = pd.DataFrame(dit1,list_clolums).T
    index               = classlocal.Kindex
    endtime             = classlocal.Kindex_time
    td                  = classlocal.Kindex_time
    #获取数据           #
    length1             = classlocal.modul_length+5
    period_t            = classlocal.Period_Type
   # h_data              = get_market_data_ex_modify(ContextInfo,check_list,period_t,endtime,length1)
    #
    h_data_init         = ContextInfo.get_market_data_ex(['close','high','open','low','volume'],\
                        check_list,period = period_t,end_time=endtime,count=length1,\
                        dividend_type='front', fill_data=True, subscribe = True)
    #h_data_t              = get_market_data_ex_modify(ContextInfo,code,period_t,endtime,length1)

    if classlocal.h_data_debug_en:
        print('check_list:\n',check_list)
        print('period_t:\n',period_t)
        print('endtime:\n',endtime)
        print('length1:\n',length1)
        print('h_data:\n',h_data_init)
    h_data = h_data_init
    #处理数据
    #输出列表:买入列别:止损:七根线最低值
    lowmin              = 0

    for code in check_list:
        if (period_t[-1] == 'm'):
            #endtime_t = endtime[-6:-2]
            #print('endtime_t:\n',endtime_t)
            if 1:#( "0900" < endtime_t < "1500"):
                h_data_code         = h_data_init[code]
                h_data              = h_data_code.loc[h_data_code['volume'] != 0]
                if classlocal.h_data_debug_en:
                    print('h_data_t:\n',h_data)
                closes              = h_data['close']
                lows                = h_data['low']
                highs               = h_data['high']
                opens               = h_data['open']
                volumes             = h_data['volume']
            else:
                closes              = h_data[code]['close']
                lows                = h_data[code]['low']
                highs               = h_data[code]['high']
                opens               = h_data[code]['open']
                volumes             = h_data[code]['volume']
        elif period_t[-1] =="d":
            closes              = h_data[code]['close']
            lows                = h_data[code]['low']
            highs               = h_data[code]['high']
            opens               = h_data[code]['open']
            volumes             = h_data[code]['volume']
        else :
            closes              = h_data[code]['close']
            lows                = h_data[code]['low']
            highs               = h_data[code]['high']
            opens               = h_data[code]['open']
            volumes             = h_data[code]['volume']


        closes_opens_dict   = closes - opens
        closemin            = closes.min()
        openmin             = opens.min()
        #34日
        len                 = 20#classlocal.modul_length
        lowmin              = lows[-len:].min()
        #暂时改为6日的最高点
        highmax             = highs[-8:].max()

        highmax             = decimal_places_are_rounded(highmax,3)
        lowmin              = decimal_places_are_rounded(lowmin,3)
        #print(code,closes)
        if(classlocal.checklist_debug_en):
            print(f'period_t[-1]\n{period_t[-1]}')
            #print(f'endtime_t\n{endtime_t}')
            print(f'h_data\n{h_data}')
            print(f'h_data\n{type(h_data)}')
            print(f'closemin\n{closemin}')
            print(f'openmin\n{openmin}')
            print(f'lowmin\n{lowmin}')
            print(f'highmax\n{highmax}')

        rows        = h_data.shape[0] 
        if  rows< classlocal.MA_long_length + 9:
            print(f'code:{code},行数:{rows}')
            print(f'计算均线数据长度不够结束本次筛选\n')
            break

        if((closemin > 0) and (openmin > 0) and (lowmin > 0) and highmax):
            #print('G_df.loc[code,'Price_SellS']:',G_df.loc[code,'Price_SellS'])
            #转成数组可以按照index取值
            close   = np.array(closes)
            low     = np.array(lows)
            high    = np.array(highs)
            open    = np.array(opens)
            volume  = np.array(volumes)
            #print(code,close)
            #opens_serious        = np.array(opens)
            closes_opens_serious = np.array(closes_opens_dict)
            #closes_opens         = closes_opens_serious
            classlocal.close     = close
            classlocal.open      = open
            classlocal.low       = low
            classlocal.high      = high
            classlocal.highmax   = highmax
            classlocal.lowmin    = lowmin
            classlocal.volume    = volume

            #昨日13日收盘价均值
            MA_middle                = np.mean(close[-classlocal.MA_middle_length-1:-1])
            MA_middle_7              = np.mean(close[-(classlocal.MA_middle_length+7):-7])
            #昨日34日收盘价均值
            MA_long                = np.mean(close[-classlocal.MA_long_length-1:-1])
            MA_long_7              = np.mean(close[-(classlocal.MA_long_length+7):-7])

            
            qxlck                = 0
            diao                 = 0
            RED_TPDYX            = 0
            GREEN_TPDYXsp        = 0
            GREEN_TPDYX          = 0
            if classlocal.GREEN_TPDYX_en:
                GREEN_TPDYX_checkout(MA_middle,MA_middle_7,MA_long,MA_long_7)
                GREEN_TPDYX                        = classlocal.GREEN_TPDYX
                GREEN_TPDYXsp                      = classlocal.GREEN_TPDYXsp

            if classlocal.qxlck_en :
                QXLCK_checkout(MA_middle,MA_middle_7,MA_long,MA_long_7)
                qxlck                    = classlocal.qxlck
                qxlcksp                  = classlocal.qxlcksp
            if classlocal.diao_en :
                YJSD_checkout()
                diao                         = classlocal.diao
                diaosp                       = classlocal.diaosp

            if classlocal.RED_TPDYX_en:
                MA1_short                    = MA_middle
                MA1_short7                   = MA_middle_7
                MA2_long                     = MA_long
                MA2_long7                    = MA_long_7
                RED_TPDYX_checkout(MA1_short,MA1_short7,MA2_long,MA2_long7)
                RED_TPDYX                    = classlocal.RED_TPDYX
                RED_TPDYXsp                  = classlocal.RED_TPDYXsp
            #---------------------------------------------------------------------------------------
            last_price                       = close[-1]
            #---------------------------------------------------------------------------------------
            if GREEN_TPDYX:
                str_modelname                = "大阴线突破"
                G_df.loc[code,'Price_SellS'] = decimal_places_are_rounded(GREEN_TPDYXsp,2)

                G_df.loc[code,'Tradingday']  = td
                sp_price                     = G_df.loc[code,'Price_SellS']
                Profit_loss_ratio            = classlocal.Price_SetSellY_YKB
                zf_zy                        = Calculate_SellY_According_to_SP_Kong(last_price,sp_price,Profit_loss_ratio)
                takprofit                    = decimal_places_are_rounded(zf_zy,2)
                G_df.loc[code,'Price_SellY'] = takprofit
                G_df.loc[code,'Kindex']      = int(index)

                classlocal.trade_direction  = 'kong' #duo #kong
                classlocal.code             = code
                classlocal.kindextime       = endtime
                classlocal.timetype         = '15m'
                classlocal.tradetype        = 'open'  #open #close
                classlocal.tradedata        = ''
                classlocal.stop             = sp_price
                classlocal.takprofit        = takprofit

                classlocal.last_price       = last_price
                classlocal.profit           = 0
                middlepricet                = (high[-1] - low[-1])/2 + low[-1]
                middleprice                 = decimal_places_are_rounded(middlepricet,3)
                classlocal.middleprice      = middleprice
                classlocal.tradestatus      = ''
                classlocal.modle            = str_modelname
                send_message_to_feishu(classlocal)

            if qxlck == 1:
                str_modelname                      = '七星一型'
                G_df.loc[code,'Price_SellS'] = decimal_places_are_rounded(qxlcksp,2)

                G_df.loc[code,'Tradingday']  = td
                sp_price                     = G_df.loc[code,'Price_SellS']
                Profit_loss_ratio            = classlocal.Price_SetSellY_YKB
                zf_zy                        = Calculate_SellY_According_to_SP(last_price,sp_price,Profit_loss_ratio)
                takprofit                    = decimal_places_are_rounded(zf_zy,3)
                G_df.loc[code,'Price_SellY'] = takprofit
                G_df.loc[code,'Kindex']      = int(index)
                #主图档当前K线索引

                classlocal.trade_direction  = 'duo' #duo #kong
                classlocal.code             = code
                classlocal.kindextime       = endtime
                classlocal.timetype         = '15m'
                classlocal.tradetype        = 'open'  #open #close
                classlocal.tradedata        = ''
                classlocal.stop             = sp_price
                classlocal.takprofit        = takprofit

                classlocal.last_price       = last_price
                classlocal.profit           = 0
                middlepricet                = (high[-1] - low[-1])/2 + low[-1]
                middleprice                 = decimal_places_are_rounded(middlepricet,3)
                classlocal.middleprice      = middleprice
                classlocal.tradestatus      = ''
                classlocal.modle            = str_modelname
                send_message_to_feishu(classlocal)

            if qxlck == 2:
                str_modelname                = "七星二型"
                G_df.loc[code,'Price_SellS'] = decimal_places_are_rounded(qxlcksp,2)


                G_df.loc[code,'Tradingday']  = td
                sp_price                     = G_df.loc[code,'Price_SellS']
                Profit_loss_ratio            =  classlocal.Price_SetSellY_YKB
                zf_zy                        = Calculate_SellY_According_to_SP(last_price,sp_price,Profit_loss_ratio)
                takprofit                    = decimal_places_are_rounded(zf_zy,2)
                G_df.loc[code,'Price_SellY'] = takprofit
                G_df.loc[code,'Kindex']      = int(index)

                classlocal.trade_direction  = 'duo' #duo #kong
                classlocal.code             = code
                classlocal.kindextime       = endtime
                classlocal.timetype         = '15m'
                classlocal.tradetype        = 'open'  #open #close
                classlocal.tradedata        = ''
                classlocal.stop             = sp_price
                classlocal.takprofit        = takprofit

                classlocal.last_price       = last_price
                classlocal.profit           = 0
                middlepricet                = (high[-1] - low[-1])/2 + low[-1]
                middleprice                 = decimal_places_are_rounded(middlepricet,3)
                classlocal.middleprice      = middleprice
                classlocal.tradestatus      = ''
                classlocal.modle            = str_modelname
                send_message_to_feishu(classlocal)

            if diao:
                str_modelname                = "一箭双雕"
                G_df.loc[code,'Price_SellS'] = decimal_places_are_rounded(diaosp,2)


                G_df.loc[code,'Tradingday']  = td
                sp_price                     = G_df.loc[code,'Price_SellS']
                Profit_loss_ratio            =  classlocal.Price_SetSellY_YKB
                zf_zy                        = Calculate_SellY_According_to_SP(last_price,sp_price,Profit_loss_ratio)
                takprofit                    = decimal_places_are_rounded(zf_zy,2)
                G_df.loc[code,'Price_SellY'] = takprofit
                G_df.loc[code,'Kindex']      = int(index)
                #print(f'G_df\n,{G_df}')
                #print('一箭双雕',code)
                classlocal.trade_direction  = 'duo' #duo #kong
                classlocal.code             = code
                classlocal.kindextime       = endtime
                classlocal.timetype         = '15m'
                classlocal.tradetype        = 'open'  #open #close
                classlocal.tradedata        = ''
                classlocal.stop             = sp_price
                classlocal.takprofit        = takprofit

                classlocal.last_price       = last_price
                classlocal.profit           = 0
                middlepricet                = (high[-1] - low[-1])/2 + low[-1]
                middleprice                 = decimal_places_are_rounded(middlepricet,3)
                classlocal.middleprice      = middleprice
                classlocal.tradestatus      = ''
                classlocal.modle            = str_modelname
                send_message_to_feishu(classlocal)
                
            if RED_TPDYX:
                str_modelname                 = "大阳线突破"
                G_df.loc[code,'Price_SellS'] = decimal_places_are_rounded(RED_TPDYXsp,2)

                G_df.loc[code,'ATR_BuyK']    = buy_atr
                G_df.loc[code,'Tradingday']  = td
                sp_price                     = G_df.loc[code,'Price_SellS']
                Profit_loss_ratio            =  classlocal.Price_SetSellY_YKB
                zf_zy                        = Calculate_SellY_According_to_SP(last_price,sp_price,Profit_loss_ratio)
                takprofit                    = decimal_places_are_rounded(zf_zy,2)
                G_df.loc[code,'Price_SellY'] = takprofit
                G_df.loc[code,'Kindex']      = int(index)

                classlocal.trade_direction  = 'duo' #duo #kong
                classlocal.code             = code
                classlocal.kindextime       = endtime
                classlocal.timetype         = '15m'
                classlocal.tradetype        = 'open'  #open #close
                classlocal.tradedata        = ''
                classlocal.stop             = sp_price
                classlocal.takprofit        = takprofit

                classlocal.last_price       = last_price
                classlocal.profit           = 0
                middlepricet                = (high[-1] - low[-1])/2 + low[-1]
                middleprice                 = decimal_places_are_rounded(middlepricet,3)
                classlocal.middleprice      = middleprice
                classlocal.tradestatus      = ''
                classlocal.modle            = str_modelname
                send_message_to_feishu(classlocal)
    return G_df
###################################start###########################################################################
#上证所 SH
#深交所 SZ
#大商所 DF 114.
#郑商所 ZF 115.
#上期所 SF 113.
#中金所 IF 220.
#外部自定义市场 ED
###################################start###########################################################################
def modify_elements(elements):
    modified_elements = []
    for elem in elements:
        if elem.startswith('1.'):
            modified_elements.append(elem[2:] + '.SH')
        elif elem.startswith('0.'):
            modified_elements.append(elem[2:] + '.SZ')
        elif elem.startswith('114.'):
            modified_elements.append(elem[2:] + '.DF')
        elif elem.startswith('115.'):
            modified_elements.append(elem[2:] + '.ZF')
        elif elem.startswith('113.'):
            modified_elements.append(elem[2:] + '.SF')
        elif elem.startswith('220.'):
            modified_elements.append(elem[2:] + '.IF')
        else:
            modified_elements.append(elem[2:] + '.ED')
    return modified_elements

def parse_ini_file(file_path,ZX):
    config      = configparser.ConfigParser()
    v           = config.read(file_path,encoding='utf-16')
    v           = config.sections()
    # 读取INI文件中的值
    #print('v',v)

    value       = config.get('\\SelfSelect', ZX)
    output_list = value.split(',')
    #print(output_list)
    modified_elements = modify_elements(output_list)
    #print(modified_elements)
    stockcode   = list(filter(None, modified_elements))
    lst         = stockcode
    stockcode   = list(map(lambda s: s[2:], lst))
    lst         = stockcode.pop()
    #print(stockcode)
    return stockcode

###################################start###########################################################################
#
###################################start###########################################################################
# 写入CSV文件
def write_to_csv(data,file_path,index1):
    data.to_csv(file_path, index = index1)

# 读取CSV文件
def read_from_csv(file_path,index1):
    df = pd.read_csv(file_path)
    #将Code列设置为索引,前提是本地列一定要有"Code"
    local_hold = df.set_index(keys='Code', drop=True)
    return local_hold

def local_hold_data_frame_init():
    global locallist_clolums
    list_data_values  = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,]
    locallist_clolums = ['Code','Price_SellY_Flag','BarSinceEntry','Price_SellY','Price_SellY1','Price_SellS',\
                        'Price_SellS1','dLastPrice','dProfitRate','Buy_time','nVolume','nCanUseVolume',\
                        'PositionProfit','ATR_Start_time','dMarketValue','Tradingday','Price_BuyK','mBuy_KIndex','mLast_KIndex','strInstrumentID','ATR_BuyK']
    dit1 = dict(zip(range(0,0), list_data_values))
    #转置矩阵
    G_df = pd.DataFrame(dit1,locallist_clolums).T
    return G_df

###################################start###########################################################################
#
###################################start###########################################################################
def write_local_hold_data(data,file_path,index1):
    # 检查文件是否存在
    try:
        with open(file_path, 'r'):
            pass
    except FileNotFoundError:
        # 文件不存在，创建新文件,没有数据空文件
        df_empty = pd.DataFrame()
        df_empty.to_csv(file_path, index=index1)

    # 写入数据到CSV文件
    write_to_csv(data,file_path,index1)
    return data

###################################start###########################################################################
#
###################################start###########################################################################
def read_local_hold_data(file_path,index1):
    # 检查文件是否存在
    try:
        with open(file_path, 'r'):
            pass
    except FileNotFoundError:
        # 文件不存在，创建新文件,没有数据空文件
        #df_empty = pd.DataFrame()
        df_empty = local_hold_data_frame_init()
        df_empty.to_csv(file_path, index=index1)

    data         = read_from_csv(file_path,index1)
    return data

###################################start###########################################################################
#
###################################start###########################################################################
def decimal_places_are_rounded(floatdata,div):
    floatdata   = round(floatdata, div)
    floatdata   = '{:.2f}'.format(floatdata)
    floatdata   = float(floatdata)
    return floatdata
###################################start###########################################################################
#
###################################start###########################################################################
def dict_into_dataframe(data_dict,cloums):
    """
        字典转换成Dataframe或Series
    """
    if len(data_dict) == 0:
        return {}
    if len(data_dict) >= 1:
        data_df = pd.DataFrame(data_dict)
        data_df = data_df.T[cloums]
        #data_df.rename(columns ={'lastPrice':'最新价', 'lastClose': '昨收价'}, inplace = True)
    return data_df



###################################start###########################################################################
#飞书发送函数
#开仓和平仓输入参数不同
###################################start###########################################################################
from datetime import datetime

def open_payload_set(modle,trade_direction,tradedata,lastprice,stop,takprofit,middleprice):
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
                        "content":"middleprice :{}".format(middleprice),
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
                        "content":"takprofit       :{}".format(takprofit),
                    }
                }

            ]
        }
    }
    return card_message


def close_payload_set(modle,tradedata,lastprice,stop,takprofit,profit):
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
                        "content":"takprofit   :{}".format(takprofit),
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
    try:
        response                = requests.post( url = url1, json = payload, headers = headers1)  # 发送POST请求
    
        if response.status_code == 200:  # 判断返回状态码是否为200(请求成功)
            response.raise_for_status()  # 如果响应状态码不是200，主动抛出异常
            #print("消息发送成功：", response.text)
        else:
            print('发送失败')
    except requests.exceptions.RequestException as e:
        print("发送失败：", e)


