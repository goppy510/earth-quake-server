#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
import requests


class Eew():
    def __init__(self):
        self.__common_uri = 'http://www.kmoni.bosai.go.jp/webservice/hypo/eew/'


    def get_json_data(self):
        endpoint = self.__create_endpoint()
        json_data = requests.get(endpoint).json()
        return json_data


    def __create_endpoint(self):
        extension = '.json'
        nowtime  = self.__get_current_date()
        endpoint = self.__common_uri + str(nowtime) + extension
        return endpoint


    def __get_current_date(self):
        date_time = datetime.now().strftime('%Y%m%d%H%M%S')
        return date_time
