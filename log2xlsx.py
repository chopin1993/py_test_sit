# coding:utf-8

import re

import xlsxwriter


def log2xls(name):
    """
    文本文件筛选后生成表格，v1.1版本，筛选单个参数，多个参数（枚举）
                    ,v1.2版本，筛选参数在不同帧中，温度、湿度、NTC温度在不同的帧里面

    1.打开文件
    2.匹配文本
    3.建立工作簿、工作表
    4.设置字体格式（表头、内容）
    5.循环写入
    :param name:
    :return:
    """

    with open(name, mode="r", encoding="utf-8") as handle:
        "打开文件"
        log = handle.read()

        "匹配文本"
        # find = r".*?通道号:(\d*).*?大量程照度[(]窗磁状态[)]:(\d*).*?自然光照度:(\d*).*?温度:([\d.]*).*?湿度:([\d.]*)"  # 多个参数
        # find = r"湿度:([\d.]*)" # 单个参数

        """查找-电流-数据"""
        # find_temp = r"CD 78 05 00.*?[(]查询[)]传感器数据：.*?1:.*?类型:温度  数据:([\d.]*)"
        find_current = r"current\":(.+?),\"electricity"
        back_current = re.findall(find_current, log)
        print(back_current)
        print('查找到 {0} 个数据：'.format(len(back_current)))

        """查找-电能-数据"""
        find_electricity = r"\"electricity\":(.+?),\"power"
        back_electricity = re.findall(find_electricity, log)
        print(back_electricity)
        print('查找到 {0} 个数据：'.format(len(back_electricity)))

        """查找-功率-数据"""
        find_power = r"\"power\":(.+?),\"voltage"
        back_power = re.findall(find_power, log)
        print(back_power)
        print('查找到 {0} 个数据：'.format(len(back_power)))

        """查找-时间戳-数据"""
        find_time = r"(.+?) -\| 调光控制器SitTest -\| INFO -\| 0JLSPIB9C/0000FFM1/0000AUNC :b'{\"deviceKey\":\"0000AUNC\",\"function\":{\"current\":"
        back_time = re.findall(find_time, log)
        print(back_time)
        print('查找到 {0} 个数据：'.format(len(back_time)))

        """创建工作表、工作簿"""
        wb = xlsxwriter.Workbook("原始数据.xlsx")
        wb_data = wb.add_worksheet("大功率数据统计")

        """设置字段格式"""
        header = {
            'bold': False,  # 粗体
            'font_name': '微软雅黑',
            'font_size': 10,
            'border': True,  # 边框线
            'align': 'center',  # 水平居中
            'valign': 'vcenter',  # 垂直居中
            'bg_color': '#66DD11'  # 背景颜色
        }

        text = {
            'font_name': '微软雅黑',
            'font_size': 9,
            'border': True,
            'align': 'lift',  # 左对齐
            'valign': 'vcenter'
        }

        header_pm = wb.add_format(header)
        text_pm = wb.add_format(text)
        # wb.set_column('C:C', 15)  # C列宽度
        # wb.set_column('A:A', 15)
        # wb.set_column('B:B', 15)
        # wb.set_column('D:D', 15)
        # wb.set_column('E:E', 15)

        # "写入表头"
        # wb.write(0, 0, "湿度", header_pm)
        # ws.write(0, 1, "大量程照度", header_pm)
        # ws.write(0, 2, "自然光照度", header_pm)
        # ws.write(0, 3, "温度", header_pm)
        # ws.write(0, 4, "湿度", header_pm)

        "电流-循环写到表格中-单个参数"
        row = 0
        col = 3
        for t in back_current:
            if row == -1:
                wb_data.write(row + 1, col, t, header_pm)
                row += 1
            else:
                wb_data.write(row + 1, col, t, text_pm)
                row += 1

        "电能-循环写到表格中-单个参数"
        row = 0
        col = 2
        for h in back_electricity:
            if row == -1:
                wb_data.write(row + 1, col, h, header_pm)
                row += 1
            else:
                wb_data.write(row + 1, col, h, text_pm)
                row += 1

        "功率-循环写到表格中-单个参数"
        row = 0
        col = 1
        for h in back_power:
            if row == -1:
                wb_data.write(row + 1, col, h, header_pm)
                row += 1
            else:
                wb_data.write(row + 1, col, h, text_pm)
                row += 1

        """时间-循环写到表格中-单个参数"""
        row = 0
        col = 0
        for h in back_time:
            if row == -1:
                wb_data.write(row + 1, col, h, header_pm)
                row += 1
            else:
                wb_data.write(row + 1, col, h, text_pm)
                row += 1

    wb.close()


if __name__ == "__main__":
    log2xls("2022_07_11.log")
