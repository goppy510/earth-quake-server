#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from slack import Slacks
from Eew import Eew


def main():
    eew = Eew()
    slacks = Slacks()
    json_data = eew.get_json_data()
    slacks.post_slack(json_data)


if __name__ == '__main__':
    main()
