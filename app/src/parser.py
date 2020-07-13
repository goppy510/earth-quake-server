#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
import datetime
import xml.etree.ElementTree as ET
import feedparser
import pprint
import time
import re
import json
import collections as cl

# 結果用の辞書用意
result = cl.OrderedDict()

# YYYY/MM/DDThh24:m:s+09:00形式の時刻をYYYY/MM/DD hh24:mm:ssにする
def parse_time(date):
    year   = date[0:4]
    month  = date[5:7]
    day    = date[8:10]
    hour   = date[11:13]
    minute = date[14:16]
    str_time = year + "/" + month + "/" + day + " " + hour + ":" + minute
    return str_time


# xmlのurlをパースする
def parse_url(url):
    parsed = feedparser.parse(url)
    return parsed


# "震源・震度に関する情報"なら詳細情報を取得
def get_detail_info(url):
    eqvol_url = parse_url(url)
    # for info in eqvol_url.entries:
        # if (info.title == "震源・震度に関する情報"):
        #     result['title'] = info.title

        # detail_url = info.links[0].href
    detail_url = "http://www.data.jma.go.jp/developer/xml/data/301b884d-e14b-39d3-bd7b-41ddbb20c1aa.xml"
    detail_parsed = parse_url(detail_url)

    detail_feed = detail_parsed.feed
    # 解析のためにxmlの最初のタグにrootタグを設定
    detail_summary = "<root>\n" + detail_feed.summary + "\n</root>"

    detail_root = ET.fromstring(detail_summary)

    #earthquakeタグ
    for data in detail_root.iter("earthquake"):
        origin_time_default   = data[0].text
        origin_time_formed    = parse_time(origin_time_default)
        result['origin_time'] = origin_time_formed

        # hypocenterタグ
        # 震源地情報取得
        hypocenter      = data.find("hypocenter")
        area            = hypocenter.find("area")
        area_name       = area.find("name").text
        coordinate      = area.find("coordinate")
        coordinate_name = coordinate.attrib["description"]
        coordinate_pt   = coordinate.text

        result['hypocenter'] = cl.OrderedDict({
                            'area': area,
                            'area_name': area_name,
                            'coordinate': coordinate,
                            'coordinate_name': coordinate_name,
                            'coordinate_pt': coordinate_name
                            })

        # マグニチュード取得
        magnitude = data.find("magnitude").text
        result['magnitude'] = magnitude


    # intensityタグ
    for data in detail_root.iter("intensity"):
        observation = data.find("observation")
        # 発生地震全体の最大震度取得
        max_seismic_intensity = observation.find("maxint").text
        result['max_seismic_intensity'] = max_seismic_intensity

        # 全cityタグ以下を取得(地震詳細を取得する)
        for i, obs_child in enumerate(observation.iter("city")):
            # 市町村名取得
            city_name = obs_child.find("name").text
            # 市町村コード取得
            city_code = obs_child.find("code").text
            # 市町村の最大震度取得
            city_maxint = obs_child.find("maxint").text

            result['city'+ str(i)] = cl.OrderedDict({
                            'name': city_name,
                            'code': city_code,
                            'maxint': city_maxint
                            })

    return result


base_url = config.jma_eqvol_url
res = get_detail_info(base_url)
pprint.pprint(res)


# リンク先から地震の詳細情報を取得する
detail_url = "http://www.data.jma.go.jp/developer/xml/data/301b884d-e14b-39d3-bd7b-41ddbb20c1aa.xml"
detail_parsed = feedparser.parse(detail_url)
