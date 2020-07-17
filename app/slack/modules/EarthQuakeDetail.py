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

# "震源・震度に関する情報"なら詳細情報を取得
def get_eq_info(url):
    eqvol_url = parse_url(url)
    # for info in eqvol_url.entries:
        # if (info.title == "震源・震度に関する情報"):
        #     result['title'] = info.title

        # detail_url = info.links[0].href
    detail_url = 'https://www.gpvweather.com/jmaxml-view.php?k=%E9%9C%87%E6%BA%90%E3%83%BB%E9%9C%87%E5%BA%A6%E3%81%AB%E9%96%A2%E3%81%99%E3%82%8B%E6%83%85%E5%A0%B1&p=%E6%B0%97%E8%B1%A1%E5%BA%81&ym=2020-03&f=2020-03-12T17%3A23%3A34-37530bda-c9f6-3a0e-acb1-a2cfe9ef5eb0.xml'
    parsed     = parse_url(detail_url)

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

    # hypocenterタグ(震源地情報)
    hypo = body[0][2]
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

    intensity = body[1]
    observation = intensity[0]

    # 最大震度
    max_int = observation[1].text
    result["maxint"] = max_int

    # 市町村と震度
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
