#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import EarthQuakeCommon
import datetime
import xml.etree.ElementTree as ET
import pprint
import time
import urllib.request


class EarthQuakeQuick:
    def __init__(self, target_title):
        self.__target_title = target_title
        self.__eq_c = EarthQuakeCommon.EarthQuakeCommon()
        self.__xml_url = self.__eq_c.get_xml_url(self.__target_title)
        self.__pref_row = 2
        self.__area_row = 3

    def get_eq(self):
        result = {}

        # テスト用
        url = 'http://www.data.jma.go.jp/developer/xml/data/361b530f-d7db-3d79-a4e3-a8191de8c47a.xml'
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

        max_int = observation[1].text
        result["maxint"] = max_int

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
        result["city"].sort(key=lambda x: x["maxint"], reverse=True)
        return result
