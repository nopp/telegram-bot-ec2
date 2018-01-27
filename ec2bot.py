#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Telegram Bot EC2
#
import sys
from lib.ec2bot import *

pvtBot = Ec2Bot()
if len(sys.argv) < 9:
    print("Usage: python ec2bot.py telegramToken ec2Region accessKey secretKey mysqlHost mysqlUser mysqlPassword mysqlDB\n")
else:
    pvtBot.startBot(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8])
