#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from slack import Slacks
from earthquake import EarthQuakeCommon
from datetime import datetime
import xml.etree.ElementTree as ET
import pprint
import time
import dateutil.parser
import os

class EarthQuake:
    def __init__(self):
        self.__slack = Slacks()
        self.__eq = EarthQuakeCommon.EarthQuakeCommon()
        self.__path = 'timelog/updated_time.txt'
        self.__local_time = None
        self.__updated_time = None

    def execute(self):
        self.__updated_time = self.__eq.get_update_time()
        if (os.path.exists(self.__path)):
            self.__read_time_log()
            if (self.__updated_time > self.__local_time):
                self.__post()
        else:
            self.__post()

    def __read_time_log(self):
        with open(self.__path, mode='r') as f:
            self.__local_time = f.read()
            self.__local_time = dateutil.parser.parse(self.__local_time)
            f.close()

    def __write_time_log(self):
        with open(self.__path, mode='w') as f:
            updated_time = self.__updated_time
            updated_time_str = updated_time.strftime('%Y/%m/%d %H:%M:%S%z')
            f.write(updated_time_str)
            f.close()

    def __post(self):
        self.__write_time_log()
        self.__slack.post_detail()

eq = EarthQuake()
eq.execute()
