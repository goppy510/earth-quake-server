#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
import slackweb
import sys, os
from earthquake import EarthQuakeDetail
from earthquake import EarthQuakeQuick

class Slacks():
    def __init__(self):
        self.__token  = config.goppy_slack_url
        self.__minint = 2
        self.__detail_title = "震源・震度に関する情報"
        self.__quick_title  = "震度速報"
        # 以下はslack系
        self.__icons = ["one", "two", "three", "four", "five", "six", "seven"]


    def post(self, data):
        if (data == False):
            return False
        title = data["title"]
        maxint = self.__parse_maxint(data["maxint"])
        body = None
        if (title == self.__detail_title):
            body = self.__create_slack_body_detail(data)
        if (title == self.__quick_title):
            body = self.__create_slack_body_quick(data)
        user_name = self.__create_slack_username(title)
        slack_conn = slackweb.Slack(url=self.__token)
        if maxint:
            icon = self.__create_slack_icon(maxint)
            slack_conn.notify(text=body, username=user_name, icon_emoji=icon)
        else:
            slack_conn.notify(text=body, username=user_name)


    # 最大震度パース
    def __parse_maxint(self, maxint):
        if (len(maxint) < 2):
            return maxint
        if (maxint[1:] == "+"):
            maxp = maxint[:1] + "強"
            return maxp
        if (maxint[1:] == "-"):
            maxp = maxint[:1] + "弱"
            return maxp


    # bodyに記入する揺れた地域と震度の情報をstringで羅列する
    def __create_area_list(self, data):
        city =  data["city"]
        city_name = []
        city_code = []
        city_maxint = []
        for i in city:
            city_name.append(i["name"])
            city_code.append(i["code"])
            city_maxint.append(self.__parse_maxint(i["maxint"]))
        maxint_city = ""
        for name, maxint in zip(city_name, city_maxint):
            if (int(maxint[:1]) >= self.__minint):
                maxint_city += name + " " + maxint + "\n"
            return maxint_city


    # 震源・震度に関する情報のslack本文
    def __create_slack_body_detail(self, data):
        maxint_city = self.__create_area_list(data)
        hypo_area   = data["hypocenter"]["name"]
        coor_pt     = data["hypocenter"]["coordinate"]
        east_pt     = coor_pt[1:5]
        north_pt    = coor_pt[6:11]
        depth       = coor_pt[12:14]
        max_int     = self.__parse_maxint(data["maxint"])
        if not max_int:
            max_int = "不明"
        if not maxint_city:
            maxint_city = "不明"
        body_event_time = "推定発生時刻： " + data["event_time"] + "\n\n"
        body_maxint     = "最大震度： " + " *" + str(max_int) + "* \n\n"
        body_mag        = "マグニチュード： M" + " *" + str(data["magnitude"]) + "* \n\n"
        body_hypo       = "震央地： " +  hypo_area + "\n"
        body_coor       = "経緯度： " + "東経 " + east_pt + " 度・北緯 " + north_pt + " 度 \n"
        body_depth      = "震源の深さ： " + depth + "km\n\n"
        body_area       = "震度"+ str(self.__minint) + "以上の観測地域： \n\n"
        body_area_name  = maxint_city + "\n"
        body            = body_event_time + body_maxint + body_mag + body_hypo + body_coor + body_depth + body_area + body_area_name
        return body

    # 震度速報のslack本文
    def __create_slack_body_quick(self, data):
        maxint_city = self.__create_area_list(data)
        max_int = self.__parse_maxint(data["maxint"])
        if not max_int:
            max_int = "不明"
        if not maxint_city:
            maxint_city = "不明"
        body_event_time = "推定発生時刻： " + data["event_time"] + "\n\n"
        body_maxint     = "最大震度： " + " *" + str(max_int) + "* \n\n"
        body_area       = "震度"+ str(self.__minint) + "以上の観測地域： \n\n"
        body_area_name  = maxint_city + "\n"
        body            = bbody_event_time + body_maxint + body_area + body_area_name
        return body


    # slackアイコン
    def __create_slack_icon(self, maxint):
        icon = ":" + self.__icons[int(maxint[:1])-1] + ":"
        return icon


    # slackのユーザー名
    def __create_slack_username(self, title):
        user_name = title
        return user_name
