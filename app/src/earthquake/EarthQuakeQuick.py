#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from . import config
import datetime
import xml.etree.ElementTree as ET
import pprint
import time
import urllib.request


def get_eq():
    evol_url = config.jma_eqvol_url
    result   = get_eq_info(evol_url)
    return result

# 結果用の辞書用意
result = {}

# "震度速報"を取得
def get_eq_info(url):
    evol_url = url
    ev_parsed = parse_url(evol_url)
    # for info in eqvol_url.entries:
        # if (info.title == "震度速報"):
        #     result['title'] = info.title

        # detail_url = info.links[0].href
    quick_url = "http://www.data.jma.go.jp/developer/xml/data/361b530f-d7db-3d79-a4e3-a8191de8c47a.xml"
    parsed    = parse_url(quick_url)

    # 結果
    result = {}

    # HEAD情報取得
    head = parsed[1]
    # タイトル取得
    title = head[0].text
    result["title"] = title

    # 発生時刻
    event_id = head[3].text
    event_time = parse_time(str(event_id))
    result["event_time"] = event_time

    # BODYタグ
    body = parsed[2]
    intensity = body[0]
    observation = intensity[0]
    # 最大震度
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

    return result

# YYYY/MM/DDThh24:m:s+09:00形式の時刻をYYYY/MM/DD hh24:mm:ssにする
def parse_time(date):
    year   = date[0:4]
    month  = date[4:6]
    day    = date[6:8]
    hour   = date[8:10]
    minute = date[10:12]
    sec    = date[12:14]
    str_time = year + "/" + month + "/" + day + " " + hour + ":" + minute + ":" + sec
    return str_time


# xmlのurlをパースする
def parse_url(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()
    root = ET.fromstring(xml_data)
    return root
