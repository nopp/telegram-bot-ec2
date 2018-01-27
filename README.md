# Telegram Bot for EC2

This bot have two actions: start/stop EC2 instance, basically the script will check on mysql database if user have permission to stop/start a specific instance.

* Import schema.sql on MySQL.
* Create a bot token on Telegram.

Example: We'll allow email user@teste.com with 123456 password to start/stop an instance i-1212121212121.

Create an user on user table:
=============================
* INSERT INTO user VALUES ('user@teste.com',MD5('123456'))
  
Create "link" between idUser and idInstance:
============================================
* SELECT id FROM user WHERE email = 'user@test.com'
* 1
* INSERT INTO resource VALUES ('1','i-1212121212121') 
user/password = admin

RUNNING BOT:
===========

	# python ec2bot.py telegramToken ec2Region accessKey secretKey mysqlHost mysqlUser mysqlPassword mysqlDB 

