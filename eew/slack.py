#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
import slackweb
import sys, os
import json
import requests


class Slacks():
    def __init__(self):
        self.__token  = config.incoming_webhook_url
        self.__minint = 2
        # 以下はslack系
        self.__title = "緊急地震速報"
        self.__icons = ["one", "two", "three", "four", "five", "six", "seven"]


    def post_slack(self, json_data):
        __json_data = json_data
        hypo_type   = str(json_data['request_hypo_type'])
        report_num  = str(json_data['report_num'])
        if ('alertflg' in json_data.keys()):
            alertflg    = str(json_data['alertflg'])
            user_name = self.__title + '(' + alertflg + ')'
            body      = self.__create_body(__json_data)
            icon = self.__create_icon(__json_data)
            # 緊急地震速報かつ第一報かつ予想震度が2以上ならslackに通知する
            # if hypo_type == 'eew' and (report_num == '1' or alertflg =='警報'):
            if hypo_type == 'eew' and report_num == '1':
                slack_conn.notify(text=body, username=user_name, icon_emoji=icon)


    def __create_body(self, json_data):
        origin_time   = self.__parse_time(str(json_data('origin_time')))
        region_name   = str(json_data('region_name'))
        depth         = str(json_data.get('depth'))
        magnitude     = float(json_data.get('magnitude'))
        latitude      = float(json_data.get('latitude'))
        longitude     = float(json_data.get('longitude'))
        calcintensity = str(json_data.get('calcintensity'))
        is_cancel     = bool(json_data.get('is_cancel'))

        # 本文のパーツ作成
        body_origin_time   = "地震発生時刻： " + " *" + origin_time + "* \n\n"
        body_calcintensity = "推定最大震度： " + " *" + calcintensity + "* \n\n"
        body_magnitude     = "マグニチュード： M" + " *" + magnitude + "* \n\n"
        body_region        = "震央地： " +  region_name + "\n"
        body_coor          = "経緯度： " + "東経 " + str(longitude) + " 北緯 " + str(latitude) + "\n"
        body_depth         = "震源の深さ： " + depth + "\n\n"
        body               = body_origin_time + body_calcintensity + body_magnitude + body_region + body_coor + body_depth
        return body


    # YYYYMMDDhh24msをYYYY/MM/DD hh24:mm:ssに変換する
    def __parse_time(self, date):
        dt = date[:4] + "/" + date[4:6] + "/" + date[6:8] + " " + date[8:10] + ":" + date[10:12] + ":" + date[12:14]
        return dt


    # slackアイコン
    def __create_icon(self, json_data):
        intensity = str(json_data['calcintensity'])
        icon = ":" + self.__icons[int(intensity[:1])-1] + ":"
        return icon
