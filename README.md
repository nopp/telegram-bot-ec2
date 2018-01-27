# Telegram Bot for EC2

This bot have two actions: start/stop EC2 instance, basically the script will check on mysql database if user have permission to stop/start a specific instance.

* Import schema.sql on MySQL.
* Create a bot token on Telegram.

## INSTALL

* git clone https://github.com/nopp/telegram-bot-ec2.git
* cd telegram-bot-ec2
* pip install -r requirements.txt

Example: We'll allow email user@teste.com with 123456 password to start/stop an instance i-1212121212121.

Create an user on user table
============================
* INSERT INTO user VALUES ('user@teste.com',MD5('123456'))
  
Create "link" between idUser and idInstance
===========================================
* SELECT id FROM user WHERE email = 'user@test.com'
* 1
* INSERT INTO resource VALUES ('1','i-1212121212121') 

RUNNING BOT
===========

	# python ec2bot.py telegramToken ec2Region accessKey secretKey mysqlHost mysqlUser mysqlPassword mysqlDB 

RUNNING ON DOCKER
=================

	# docker container run -d -e token='xxx' -e region='xxx' -e akey='accessKey' -e skey='secretKey' -e mysqlHost='xxx' -e mysqlUser='xxx' -e mysqlPassword='xxx' -e mysqlDB='xxx' nopp/telegram-bot-ec2:latest


SCREENSHOT
==========
![Image Alt](http://i63.tinypic.com/2nsbdx4.png)
