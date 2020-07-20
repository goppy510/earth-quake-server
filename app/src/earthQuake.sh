#!/bin/bash

export PATH=/home/goppy/.pyenv/bin:$PATH
eval "$(pyenv init -)"
srcPath=/home/$(whoami)/earth-quake-server/app/src/
mkdir -p ${srcPath}/quick_xml 2>/dev/null
mkdir -p ${srcPath}/detail_xml 2>/dev/null
mkdir -p ${srcPath}/timelog 2>/dev/null

python3 earthQuake.py
