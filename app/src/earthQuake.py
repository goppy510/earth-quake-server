#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from slack import Slacks
from line import Lines
from earthquake import EarthQuakeCommon, EarthQuakeDetail, EarthQuakeQuick
from datetime import datetime
import config
import xml.etree.ElementTree as ET
import pprint
import time
import dateutil.parser
import os

class EarthQuake:
    def __init__(self):
        self.__detail_title      = config.detail_title
        self.__quick_title       = config.quick_title
        self.__slack             = Slacks()
        self.__line              = Lines()
        self.__eq                = EarthQuakeCommon.EarthQuakeCommon()
        self.__eq_d              = EarthQuakeDetail.EarthQuakeDetail(self.__detail_title)
        self.__eq_q              = EarthQuakeQuick.EarthQuakeQuick(self.__quick_title)
        self.__eq_d_data         = self.__eq_d.get_eq()
        self.__eq_q_data         = self.__eq_q.get_eq()
        self.__time_path         = 'timelog/updated_time.txt'
        self.__detail_path       = 'detail_xml/detail_xml.txt'
        self.__quick_path        = 'quick_xml/quick_xml.txt'
        self.__latest_detail_xml = None
        self.__local_detail_xml  = None
        self.__latest_quick_xml  = None
        self.__local_quick_xml   = None
        self.__local_time        = None
        self.__updated_time      = None

    def execute(self):
        self.__updated_time      = self.__eq.get_update_time()
        self.__latest_detail_xml = self.__eq.get_xml_url(self.__detail_title)
        self.__execute_detail()
        self.__execute_quick()

    def __execute_detail(self):
        if (self.__eq_d_data):
            if (os.path.exists(self.__time_path)):
                self.__read_time_log()
                if (os.path.exists(self.__detail_path)):
                    self.__read_detail_xml()
                if (self.__updated_time > self.__local_time):
                    if (self.__local_detail_xml != self.__latest_detail_xml):
                        self.__post_detail()
            else:
                self.__post_detail()

    def __execute_quick(self):
        if (self.__eq_q_data):
            if (os.path.exists(self.__time_path)):
                self.__read_time_log()
                if (os.path.exists(self.__quick_path)):
                    self.__read_quick_xml()
                if (self.__updated_time > self.__local_time):
                    if (self.__local_quick_xml != self.__latest_quick_xml):
                        self.__post_quick()
            else:
                self.__post_quick()


    # 最後に記録した時間が書かれたファイルを読み込む
    def __read_time_log(self):
        with open(self.__time_path, mode='r') as f:
            self.__local_time = f.read()
            self.__local_time = dateutil.parser.parse(self.__local_time)
            f.close()

    # xmlの時刻が更新されていた場合、その時刻をファイルに書き込む
    def __write_time_log(self):
        with open(self.__time_path, mode='w') as f:
            updated_time = self.__updated_time
            updated_time_str = updated_time.strftime('%Y/%m/%d %H:%M:%S%z')
            f.write(updated_time_str)
            f.close()

    # 震度・震度に関する情報の最新xmlを読み込む
    def __read_detail_xml(self):
        with open(self.__detail_path, mode='r') as f:
            self.__local_detail_xml = f.read()
            f.close()

    # 震度・震度に関する情報の最新xmlを書き込む
    def __write_detail_xml(self):
        with open(self.__detail_path, mode='w') as f:
            latest_xml_url = self.__latest_detail_xml
            f.write(latest_xml_url)
            f.close()

    # 震度速報の最新xmlを読み込む
    def __read_quick_xml(self):
        with open(self.__quick_path, mode='r') as f:
            self.__local_quick_xml = f.read()
            f.close()

    # 震度速報の最新xmlを書き込む
    def __write_quick_xml(self):
        with open(self.__quick_path, mode='w') as f:
            latest_xml_url = self.__latest_quick_xml
            f.write(latest_xml_url)
            f.close()

    def __post_detail(self):
        self.__slack.post(self.__eq_d_data)
        self.__line.post(self.__eq_d_data)
        self.__write_time_log()
        self.__write_detail_xml()

    def __post_quick(self):
        self.__slack.post(self.__eq_q_data)
        self.__line.post(self.__eq_q_data)
        self.__write_time_log()
        self.__write_quick_xml()

if __name__ == '__main__':
    eq = EarthQuake()
    eq.execute()
