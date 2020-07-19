#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
import slackweb
import sys, os
from earthquake import EarthQuakeDetail
from earthquake import EarthQuakeQuick

class Slacks():
    def __init__(self):
        self.__eq_d = EarthQuakeDetail.EarthQuakeDetail()
        self.__eq_q = EarthQuakeQuick.EarthQuakeQuick()
        self.__token = config.goppy_slack_url
        self.__title       = None
        self.__event_time  = None
        self.__hypo_area   = None
        self.__coor_pt     = None
        self.__east_pt     = None
        self.__north_pt    = None
        self.__depth       = None
        self.__magnitude   = None
        self.__max_int     = None
        self.__city_name   = None
        self.__city_code   = None
        self.__city_maxint = None
        self.__city_name    = []
        self.__city_code    = []
        self.__city_maxint  = []
        self.__minint      = 2
        # 以下はslack系
        self.__maxint_city = ""
        self.__user_name   = None
        self.__body        = None
        self.__icon        = None
        self.__icons       = ["one", "two", "three", "four", "five", "six", "seven"]

    def test(self):
        self.__set_detail_data()
        self.__create_area_list()


    def post_detail(self):
        self.__set_detail_data()
        self.__create_slack_username()
        self.__create_slack_icon()
        self.__create_slack_body_detail()
        slack_conn = slackweb.Slack(url=self.__token)
        user_name = self.__user_name
        icon = self.__icon
        body = self.__body
        slack_conn.notify(text=body, username=user_name, icon_emoji=icon)


    def post_quick(self):
        self.__set_quick_data()
        self.__create_slack_icon()
        self.__create_slack_body_quick()
        self.__create_slack_username()
        slack_conn = slackweb.Slack(url=self.__token)
        user_name  = self.__user_name
        icon       = self.__icon
        body       = self.__body
        slack_conn.notify(text=body, username=user_name, icon_emoji=icon)


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


    # 震度速報取得
    def __set_quick_data(self):
        eq = self.__eq_q.get_eq()
        area = eq["area"]
        self.__title        = eq["title"]
        self.__event_time   = eq["event_time"]
        self.__max_int      = self.__parse_maxint(eq["maxint"])
        for i in area:
            self.__city_name.append(i["name"])
            self.__city_code.append(i["code"])
            self.__city_maxint.append(self.__parse_maxint(i["maxint"]))


    # 震源・震度に関する情報取得
    def __set_detail_data(self):
        eq = self.__eq_d.get_eq()
        city = eq["city"]
        self.__title        = eq["title"]
        self.__event_time   = eq["event_time"]
        self.__hypo_area    = eq["hypocenter"]["name"]
        self.__coor_pt      = eq["hypocenter"]["coordinate"]
        self.__east_pt      = self.__coor_pt[1:5]
        self.__north_pt     = self.__coor_pt[6:11]
        self.__depth        = self.__coor_pt[12:14]
        self.__magnitude    = eq["magnitude"]
        self.__max_int      = self.__parse_maxint(eq["maxint"])
        for i in city:
            self.__city_name.append(i["name"])
            self.__city_code.append(i["code"])
            self.__city_maxint.append(self.__parse_maxint(i["maxint"]))


    # bodyに記入する揺れた地域と震度の情報をstringで羅列する
    def __create_area_list(self):
        for name, maxint in zip(self.__city_name, self.__city_maxint):
            if (int(maxint[:1]) >= self.__minint):
                self.__maxint_city += name + " " + maxint + "\n"


    # 震源・震度に関する情報のslack本文
    def __create_slack_body_detail(self):
        self.__create_area_list()
        self.__body = "推定発生時刻： " + self.__event_time + "\n\n" \
                    + "最大震度： " + " *" + str(self.__max_int) + "* \n\n" \
                    + "マグニチュード： M" + " *" + str(self.__magnitude) + "* \n\n" \
                    + "震源地： " +  self.__hypo_area + "\n" \
                    + "経緯度： " + "東経 " + self.__east_pt + " 度・北緯 " + self.__north_pt + " 度 \n" \
                    + "震源の深さ： " + self.__depth + "km\n\n" \
                    + "震度"+ str(self.__minint) + "以上の観測地域： \n\n" \
                    + self.__maxint_city + "\n" \


    # 震度速報のslack本文
    def __create_slack_body_quick(self):
        self.__body = "推定発生時刻： " + self.__event_time + "\n\n" \
                    + "最大震度： " + " *" + str(self.__max_int) + "* \n\n" \
                    + "震度"+str(self.__minint)+"以上の観測地域： \n\n" \
                    + self.__maxint_city + "\n" \


    # slackアイコン
    def __create_slack_icon(self):
        self.__icon = ":" + self.__icons[int(self.__max_int[:1])-1] + ":"


    # slackのユーザー名
    def __create_slack_username(self):
        self.__user_name = self.__title
