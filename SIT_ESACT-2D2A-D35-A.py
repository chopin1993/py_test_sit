# code utf-8

import datetime
import random
import threading
import time

import paho.mqtt.client as mqtt

from output_log import Log


# -------------------回调函数及操作函数
def on_message_callback(client, userdata, message):
    """
    回调方法
    :param client:
    :param userdata:
    :param message:
    :return:
    """
    # time_callback = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    str_msg = message.topic + " " + ":" + str(message.payload)
    Log().info(str_msg)
    # print(time_callback + '——>>' + message.topic + " " + ":" + str(message.payload))


def on_connect_callback(client, userdata, flags, rc):
    """
    订阅网关日志
    :return:
    """
    Log().info("订阅网关——>>Connected with result code " + str(rc))
    # print("订阅网关——>>Connected with result code " + str(rc))
    if 0 == rc:
        Log().info('连接网关成功')
        # print("连接网关成功")
    elif 1 == rc:
        Log().info('连接失败-不正确的协议版本')
        # print("连接失败-不正确的协议版本")
    elif 2 == rc:
        Log().info('连接失败-无效的客户端标识符')
        print("连接失败-无效的客户端标识符")
    elif 3 == rc:
        Log().info('连接失败-服务器不可用')
        # print("连接失败-服务器不可用")
    elif 4 == rc:
        Log().info('连接失败-错误的用户名或密码')
        # print("连接失败-错误的用户名或密码")
    elif 5 == rc:
        Log().info('连接失败-未授权')
        # print("连接失败-未授权")
    else:
        Log().info('6-255: 未定义.')
        # print("6-255: 未定义.")
    client.subscribe("0JLSPIB9C/0000FFM1/+", qos=0)  # 网关topic
    client.subscribe("0JLSPIB9C/0000FFM1/0000AUNC/command", qos=0)  # 大功率topic
    client.subscribe("0JLSPIB9C/0000FFM1/0000AKMT/command", qos=0)  # 调光控制器opic


def ctrl_power(cmd):  # 大功率控制（订阅和发json）
    """
    大功率控制&读取
    :param cmd: 0-断开；1-闭合；2-读取数据
    :return:
    """
    power_push1 = ['{"cmd":"write","deviceKey":"0000AUNC","function":{"switch_ch1":false}}',
                   '{"cmd":"write","deviceKey":"0000AUNC","function":{"switch_ch1":true}}',
                   '{"cmd":"read","deviceKey":"0000AUNC","function":{"electricity":"","voltage":"","current":"",'
                   '"power":""}']
    if cmd == '0':  # 闭合大功率
        client.publish(topic=power_topic, payload=power_push1[0], qos=1)
    elif cmd == '1':  # 断开大功率
        client.publish(topic=power_topic, payload=power_push1[1], qos=1)
    elif cmd == '1':  # 读取大功率计量参数
        client.publish(topic=power_topic, payload=power_push1[2], qos=1)
    else:
        print('填写的数据标识不存在')


def ctrl_devices():  # 控制设备

    # random_number = random.randint(0, 100)
    devices_push = [
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":false,"diming_target_ch1":0}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":true,"diming_target_ch1":10}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":true,"diming_target_ch1":20}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":true,"diming_target_ch1":30}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":true,"diming_target_ch1":40}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":true,"diming_target_ch1":50}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":true,"diming_target_ch1":60}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":true,"diming_target_ch1":70}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":true,"diming_target_ch1":80}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":true,"diming_target_ch1":90}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":true,"diming_target_ch1":100}}',
        '{"cmd":"write","deviceKey":"0000AKMT","function":{"switch_ch1":false,"diming_target_ch1":0}}']

    while True:
        now = datetime.datetime.now()
        now_h = now.hour
        now_m = now.minute
        Log().info(now_h + now_m)
        # print(now.hour, now.minute)
        if 8 <= now.hour < 21:  # 运行时间：8:00-21:00
            for json_devices in devices_push:
                client.publish(topic=device_topic, payload=json_devices, qos=1)
                time.sleep(300)  # 调光间隔时间5.45min，1个小时完成一个调光循环0—100%    327
        # 每隔60秒检测一次
        time.sleep(60)


# ------------------定义服务器参数-----------------------

HOST = "iot.eastsoft.com.cn"  # 生产服务器地址
PORT = 1883

# 替换为实际的client id，具体要求需要查对应的服务器
client = mqtt.Client('iot.eastsoft.com.cn')
client.username_pw_set('87d01212-b1b8-4f98-8188-76e3d88a13ca', '0YMH6ZCg')  # 连接用户名和密码
client.on_connect = on_connect_callback
client.on_message = on_message_callback
client.connect(HOST, PORT, 60)

gateway_topic = "0JLSPIB9C/0000FFM1/+"
power_topic = "0JLSPIB9C/0000FFM1/0000AUNC/command"  # 大功率订阅主题
power_push = ['{"cmd":"write","deviceKey":"0000AUNC","function":{"switch_ch1":false}}',
              '{"cmd":"write","deviceKey":"0000AUNC","function":{"switch_ch1":true}}',
              '{"cmd":"read","deviceKey":"0000AUNC","function":{"electricity":"","voltage":"","current":"",'
              '"power":""}']
device_topic = '0JLSPIB9C/0000FFM1/0000AKMT/command'

if __name__ == '__main__':
    power = threading.Thread(target=ctrl_power, args=['1'])  # 开启大功率为系统供电
    power.start()
    ctrl_devices_thd = threading.Thread(target=ctrl_devices)
    ctrl_devices_thd.start()
    client.loop_forever()
    log_thd = threading.Thread(target=Log)
    log_thd.start()
