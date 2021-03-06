#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
import os
import json
import requests
import datetime
import dateutil.parser


class Lines():
    def __init__(self):
        self.__token        = config.line_token
        self.__updated_time = None
        self.__local_time   = None
        # os.chdir('earth-quake-server/eew')
        # self.__time_path    = os.getcwd() + '/updated_time_eew.txt'
        self.__time_path    = 'updated_time_eew.txt'
        self.__minint = 2
        self.__title = "緊急地震速報"
        self.__headers = {'Authorization': 'Bearer ' + self.__token}


    def post(self, json_data):
        report_time = str(json_data['report_time'])
        if report_time:
            self.__updated_time = dateutil.parser.parse(report_time)
            if self.__is_exists_timelog():
                if self.__is_latest(report_time):
                    self.__send(json_data)
                else:
                    return False
            else:
                self.__send(json_data)


    def __send(self, json_data):
        api_url = self.__get_api_url()
        hypo_type   = str(json_data['request_hypo_type'])
        report_num  = str(json_data['report_num'])
        intensity   = str(json_data['calcintensity'])
        report_time = str(json_data['report_time'])
        intensity   = int(str(json_data['calcintensity'])[:1])
        alertflg    = str(json_data['alertflg'])
        title   = self.__title + '(' + report_time + ')'
        body        = self.__create_body(json_data)
        message = title + "\n\n" + body
        payload = {
            'message': message,
        }
        # 緊急地震速報かつ第一報かつ予想震度が2以上ならslackに通知する
        if hypo_type == 'eew' and ((report_num == '1' and intensity >= self.__minint) or alertflg =='警報'):
            requests.post(api_url, headers=self.__headers, data=payload)


    def __is_exists_timelog(self):
        if os.path.exists(self.__time_path):
            self.__read_time_log()
            return True
        return False


    def __is_latest(self, report_time):
        if self.__updated_time > self.__local_time:
            return True
        return False


    def __create_body(self, json_data):
        origin_time   = self.__parse_time(str(json_data['origin_time']))
        region_name   = str(json_data['region_name'])
        depth         = str(json_data['depth'])
        magunitude    = float(json_data['magunitude'])
        latitude      = float(json_data['latitude'])
        longitude     = float(json_data['longitude'])
        calcintensity = str(json_data['calcintensity'])
        is_cancel     = bool(json_data['is_cancel'])
        alertflg      = str(json_data['alertflg'])

        # 本文のパーツ作成
        body_mention       = "@ALL" + "\n\n"
        body_alertflg      = "種別： " + alertflg + "\n"
        body_origin_time   = "地震発生時刻： " + " *" + origin_time + "* \n\n"
        body_calcintensity = "推定最大震度： " + " *" + calcintensity + "* \n\n"
        body_magunitude    = "マグニチュード： M" + " *" + str(magunitude) + "* \n\n"
        body_region        = "震央地： " +  region_name + "\n"
        body_coor          = "経緯度： " + "東経 " + str(longitude) + " 北緯 " + str(latitude) + "\n"
        body_depth         = "震源の深さ： " + depth + "\n\n"
        body               = body_mention + body_alertflg + body_origin_time + body_calcintensity + body_magunitude + body_region + body_coor + body_depth
        return body


    # YYYYMMDDhh24msをYYYY/MM/DD hh24:mm:ssに変換する
    def __parse_time(self, date):
        dt = date[:4] + "/" + date[4:6] + "/" + date[6:8] + " " + date[8:10] + ":" + date[10:12] + ":" + date[12:14]
        return dt


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