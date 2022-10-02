import logging
import os
import time

path = os.path.dirname(os.path.realpath(__file__))  # 获取本地路径
log_path = os.path.join(path, 'logs')  # log_path是存放日志的路径
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(log_path):
    os.mkdir(log_path)


class Log:
    def __init__(self):
        # 文件的命名
        self.logname = os.path.join(log_path, './%s.log' % time.strftime('%Y_%m_%d'))
        self.logger = logging.getLogger('调光控制器SitTest')
        self.logger.setLevel(logging.INFO)
        # 日志输出格式
        # self.formatter = logging.Formatter(f'%(asctime)s -| %(name)s -| {log_path}| %(levelname)s -| %(message)s')
        self.formatter = logging.Formatter(f'%(asctime)s -| %(name)s -| %(levelname)s -| %(message)s')

    def __console(self, level, message):
        """
        创建控制台、本地日志输出；配置文件输出level
        :param level:
        :param message:
        :return:
        """
        # 创建一个fileHander，用于写入本地
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')
        # fh =  RotatingFileHandler(self.logname, maxBytes=1 * 1024, backupCount=3)     # 按照文件大小分割日志文件
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输入到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 避免日志重复
        self.logger.removeHandler(fh)
        self.logger.removeHandler(ch)
        # 关闭打开文件
        fh.close()

    def debug(self, message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)


# log = Log()
# log.debug('debug')
# log.warning('warning')
# log.error('error')
# log.info('info')
