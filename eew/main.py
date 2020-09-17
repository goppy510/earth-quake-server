#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from slack import Slacks
from line import Lines
from Eew import Eew
import datetime
import dateutil.parser
import os

class Mains():
    def __init__(self):
        self.__updated_time = None
        self.__local_time = None
        self.__time_path = 'updated_time_eew.txt'
        self.__eew = Eew()
        self.__slacks = Slacks()
        self.__lines = Lines()
        self.__json_data = self.__eew.get_json_data()


    def main(self):
        if self.__is_latest_time():
            self.__slacks.post_slack(self.__json_data)
            self.__lines.post(self.__json_data)
            self.__write_time_log(self.__updated_time)


    def __is_latest_time(self):
        report_time = str(self.__json_data['report_time'])
        if report_time:
            self.__updated_time = dateutil.parser.parse(report_time)
            if self.__is_exists_timelog():
                if self.__is_latest(report_time):
                    return True
                else:
                    return False
            else:
                return True


    # 最後に記録した時間が書かれたファイルを読み込む
    def __read_time_log(self):
        with open(self.__time_path, mode='r') as f:
            self.__local_time = f.read()
            self.__local_time = dateutil.parser.parse(self.__local_time)
            f.close()


    # xmlの時刻が更新されていた場合、その時刻をファイルに書き込む
    def __write_time_log(self, report_time):
        with open(self.__time_path, mode='w') as f:
            updated_time = report_time
            updated_str  = updated_time.strftime('%Y/%m/%d %H:%M:%S')
            f.write(updated_str)
            f.close()


    def __is_exists_timelog(self):
        if os.path.exists(self.__time_path):
            self.__read_time_log()
            return True
        return False


    def __is_latest(self, report_time):
        if self.__updated_time > self.__local_time:
            return True
        return False


if __name__ == '__main__':
    main = Mains()
    main.main()
