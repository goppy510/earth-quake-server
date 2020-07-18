#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config
import slackweb
import sys, os
from modules import EarthQuakeDetail

def post():
    slack_url  = config.goppy_slack_url
    slack      = slackweb.Slack(url=slack_url)
    user_name  = "震源・震度に関する情報"
    post_data  = create_post_data()
    message    = post_data[0]
    icon       = post_data[1]

    slack.notify(text=message, username=user_name, icon_emoji=icon)

def parse_maxint(maxint):
    if (len(maxint) < 2):
        return maxint
    if (maxint[1:] == "+"):
        maxp = maxint[:1] + "強"
        return maxp
    if (maxint[1:] == "-"):
        maxp = maxint[:1] + "弱"
        return maxp

def create_post_data():
    eq = EarthQuakeDetail.get_eq()
    event_time    = eq["event_time"]
    hypo_area     = eq["hypocenter"]["name"]
    coordinate_pt = eq["hypocenter"]["coordinate"]
    east_pt       = coordinate_pt[1:5]
    north_pt      = coordinate_pt[6:11]
    depth         = coordinate_pt[12:14]
    magnitude     = eq["magnitude"]
    max_int       = parse_maxint(eq["maxint"])
    city_name     = []
    city_code     = []
    city_maxint   = []
    for i in eq["city"]:
        city_name.append(i["name"])
        city_code.append(i["code"])
        city_maxint.append(parse_maxint(i["maxint"]))

    maxint_city = ""
    for name, maxint in zip(city_name, city_maxint):
        if (int(maxint[:1]) > 1):
            maxint_city += name + " " + maxint + "\n"

    message = "推定発生時刻： " + event_time + "\n\n" \
            + "最大震度： " + " *" + str(max_int) + "* \n\n" \
            + "震源地： " +  hypo_area + "\n" \
            + "経緯度： " + "東経 " + east_pt + " 度・北緯 " + north_pt + " 度 \n" \
            + "震源の深さ： " + depth + "km\n\n" \
            + "震度2以上の観測地域： \n\n" \
            + maxint_city + "\n" \

    icons = ["one", "two", "three", "four", "five", "six", "seven"]
    icon = ":" + icons[int(max_int[:1])-1] + ":"

    return message, icon

post()
