#!/bin/bash

export PATH=/home/$(whoami)/.pyenv/bin:$PATH
eval "$(pyenv init -)"
srcPath=/home/$(whoami)/earth-quake-server/eew

python3 ${srcPath}/main.py
