# code utf-8
import json
import random
import time
from output_log import Log


# 设备通道列表
channel_list = ["channel1", "channel2", "channel3", "channel4", "channel5",
                "channel6",
                "channel7", "channel8", "channel9", "channel10", "channel11",
                "channel12", "channel13", "channel14", "channel15"]


def judge_channel(channel_num):
    """
    判断通道，返回通道相关属性
    :param channel_num:通道号
    :return:
    """
    str(channel_num)
    if channel_num == "channel1":  # 第一通道
        print('当前是第1通道')
    elif channel_num == "channel2":
        print('当前是第2通道')
    elif channel_num == "channel3":
        print('当前是第3通道')
    elif channel_num == "channel4":
        print('当前是第4通道')
    elif channel_num == "channel5":
        print('当前是第5通道')
    elif channel_num == "channel6":
        print('当前是第6通道')
    elif channel_num == "channel7":
        print('当前是第7通道')
    elif channel_num == "channel8":
        print('当前是第8通道')
        channel8_mode(channel_num)
    elif channel_num == "channel9":
        print('当前是第9通道')
    elif channel_num == "channel10":
        print('当前是第10通道')
    elif channel_num == "channel11":
        print('当前是第11通道')
    elif channel_num == "channel12":
        print('当前是第12通道')
    elif channel_num == "channel13":
        print('当前是第13通道')
    elif channel_num == "channel14":
        print('当前是第14通道')
    else:
        print('当前是第15通道')
    return  # 返回通道具有的模式


def channel8_mode(channel_num):
    """
    channel8的模式判断，并发送模式配置和随机值
    :param channel_num:
    :return:
    """
    mode_list = ['value', 'resistance', 'current']
    for mode in mode_list:
        if mode == 'value':
            print('配置{0}模式'.format(mode))  # 实际应用中调用模式配置函数
            time.sleep(0.5)  # 延时，等待配置生效
            print('发送配置的{0}'.format(mode))
            mode_Voltage_value(channel_num)
        elif mode == 'resistance':
            print('配置{0}模式'.format(mode))  # 实际应用中调用模式配置函数
            time.sleep(0.5)  # 延时，等待配置生效
            print('发送配置的{0}'.format(mode))
        else:  # current模式
            print('配置{0}模式'.format(mode))  # 实际应用中调用模式配置函数
            time.sleep(0.5)  # 延时，等待配置生效
            print('发送配置的{0}'.format(mode))


def mode_Voltage_value(channel_num):
    """"""
    random_value = random.randint(0, 10000)  # 生成电压随机数
    value_channel = {
        "cmd": "write",
        "deviceKey": "biou0000",
        "function": {channel_num: random_value},
    }
    data = json.dumps(value_channel)
    # client.publish(topic=device_cmd_topic, payload=data, qos=1)
    print(data)  # 通过client.publish输出到设备


def mode_current():
    """"""
    pass


def mode_resistance():
    """"""
    pass


print(judge_channel("channel8"))
