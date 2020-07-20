#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import EarthQuakeCommon
import datetime
import xml.etree.ElementTree as ET
import pprint
import time
import urllib.request


class EarthQuakeDetail:
    def __init__(self, target_title):
        self.__target_title = target_title
        self.__eq_c = EarthQuakeCommon.EarthQuakeCommon()
        self.__xml_url = self.__eq_c.get_xml_url(self.__target_title)
        self.__pref_row = 2
        self.__area_row = 3

    def get_eq(self):
        result = {}

        # テスト用
        url = 'https://www.gpvweather.com/jmaxml-view.php?k=%E9%9C%87%E6%BA%90%E3%83%BB%E9%9C%87%E5%BA%A6%E3%81%AB%E9%96%A2%E3%81%99%E3%82%8B%E6%83%85%E5%A0%B1&p=%E6%B0%97%E8%B1%A1%E5%BA%81&ym=2020-03&f=2020-03-12T17%3A23%3A34-37530bda-c9f6-3a0e-acb1-a2cfe9ef5eb0.xml'
        if (self.__xml_url == None):
            return False
        parsed = self.__eq_c.parse_url(self.__xml_url)
        # parsed = self.__eq_c.parse_url(url)

        control = parsed[0]
        result["title"] = control[0].text

        head = parsed[1]
        event_id   = head[3].text
        event_time = self.__eq_c.parse_time_str(str(event_id)) # 発生時刻取得
        result["event_time"] = event_time

        body        = parsed[2]
        intensity   = body[0]
        observation = intensity[0]

        hypo      = body[0][2]
        hypo_area = hypo[0]
        hypo_name = hypo_area[0].text # 震源地エリア名
        hypo_code = hypo_area[1].text # エリアコード
        hypo_coord = hypo_area[2].text # 経緯
        result["hypocenter"] = {
            "name": hypo_name,
            "code": hypo_code,
            "coordinate": hypo_coord
        }

        # マグニチュード
        magnitude = body[0][3].text
        result["magnitude"] = magnitude

        intensity   = body[1]
        observation = intensity[0]
        max_int     = observation[1].text
        result["maxint"] = max_int # 最大震度

        result["city"] = []
        for ob in observation[2:]:
            for city in ob[3:]:
                city_name   = city[0].text
                city_code   = city[1].text
                city_maxint = city[2].text

                result["city"].append({
                    "name": city_name,
                    "code": city_code,
                    "maxint": city_maxint
                })
        result['city'].sort(key=lambda x: x["maxint"], reverse=True)
        return result
