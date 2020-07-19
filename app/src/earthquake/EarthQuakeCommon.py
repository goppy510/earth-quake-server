#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from pytz import timezone
import xml.etree.ElementTree as ET
from . import config
import pprint
import time
import urllib.request
import dateutil.parser

class EarthQuakeCommon:
    def __init__(self):
        self.__entries_row = 8


    # 任意のタイトルに応じたタイトルがあるエントリのxmlリンクを返す
    def get_xml_url(self, target_title):
        target_title = target_title
        entries = self.__get_entry()
        xml_url = None
        for entry in entries:
            title = entry[0].text
            if (title == target_title):
                link = entry[4]
                xml_url = link.attrib['href']
        return xml_url


    # eqvolの更新時刻を取得する
    def get_update_time(self):
        eqvol_xml = self.__parse_eqvol()
        updated_raw = eqvol_xml[2].text
        updated_time = dateutil.parser.parse(updated_raw)
        return updated_time


    def parse_url(self, url):
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        return root


    # YYYY/MM/DDThh24:m:s+09:00形式の時刻をYYYY/MM/DD hh24:mm:ssにする
    def parse_time(self, date):
        dt = datetime.strptime(date, '%Y/%m/%d %H:%M:%S')
        return dt


    # YYYYMMDDhh24msをYYYY/MM/DD hh24:mm:ssに変換する
    def parse_time_str(self, date):
        dt = date[:4] + "/" + date[4:6] + "/" + date[6:8] + " " + date[8:10] + ":" + date[10:12] + ":" + date[12:14]
        return dt


    # 地震火山xmlの取得
    def __read_eqvol(self):
        evol_url = config.jma_eqvol_url
        return evol_url


    # evol_urlをパースする
    def __parse_eqvol(self):
        eqvol_url = self.__read_eqvol()
        eqvol_xml = self.parse_url(eqvol_url)
        return eqvol_xml


    # 一覧からentry部分を取得する
    def __get_entry(self):
        eqvol_xml = self.__parse_eqvol()
        eq_title = config.eqvol_title
        entries_row = self.__entries_row
        entries = []
        for entry in eqvol_xml[entries_row:]:
            entries.append(entry)
        return entries
