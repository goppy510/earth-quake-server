#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from datetime import datetime
from slack import Slacks
from line import Lines
from Eew import Eew


def main():
    eew = Eew()
    slacks = Slacks()
    lines = Lines()
    json_data = eew.get_json_data()
    slacks.post_slack(json_data)
    lines.post(json_data)


if __name__ == '__main__':
    main()
