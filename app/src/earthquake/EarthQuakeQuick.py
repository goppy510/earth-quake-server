#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import config
import EarthQuakeCommon
import datetime
import xml.etree.ElementTree as ET
import pprint
import time
import urllib.request

class EarthQuakeQuick:
    def __init__(self):
        self.__target_title = config.detail_title
        self.eq_common = EarthQuakeCommon(self.__target_title)
        self.xml_url = self.eq_common.get_xml_url()
        self.__pref_row = 2
        self.__area_row = 3

    def get_eq(self):
        result = {}

        # テスト用
        url = 'http://www.data.jma.go.jp/developer/xml/data/361b530f-d7db-3d79-a4e3-a8191de8c47a.xml'
        parsed = self.eq_common.parse_url(self.xml_url)
        parsed = self.eq_common.parse_url(url)

        head = parsed[1]
        event_id   = head[3].text
        event_time = self.eq_common.parse_time_str(str(event_id)) # 発生時刻取得
        result["title"]      = head[0].text # title取得
        result["event_time"] = event_time

        body        = parsed[2]
        intensity   = body[0]
        observation = intensity[0]

        max_int = observation[1].text
        result["max_int"] = max_int

        result["area"] = []
        for ob in observation[2:]:
            for pref in ob[3:]:
                area_name   = pref[0].text
                area_code   = pref[1].text
                area_maxint = pref[2].text
                result["area"].append({
                    "name": area_name,
                    "code": area_code,
                    "maxint": area_maxint
                })
        result["area"].sort(key=lambda x: x["maxint"], reverse=True)
