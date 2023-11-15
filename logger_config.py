# -*- coding: utf-8 -*-
# @Project : Spider_doc
# @Time    : 2023/11/15 10:35
# @Author  : infinityay
# @File    : logger_config.py
# @Software: PyCharm 
# @Contact me: https://github.com/Infinityay or stu.lyh@outlook.com
# @Comment :

# logger_config.py

import logging


class CustomLogger:
    def __init__(self, log_file='error.log', console_level=logging.INFO,
                 file_save_level=logging.ERROR):

        # log_file 指的是文件保存的位置
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # 创建一个用于输出到控制台的处理程序
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)

        # 创建一个用于输出到文件的处理程序
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(file_save_level)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)

        # 添加处理程序到日志记录器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger


