FROM alpine:3.7

LABEL maintainer "Carlos Augusto Malucelli <malucellicarlos@gmail.com"

RUN apk update \
		&& apk add py-pip git py-mysqldb bash \
		&& git clone https://github.com/nopp/telegram-bot-ec2.git \
		&& cd telegram-bot-ec2 \
		&& pip install -r requirements.txt \
		&& chmod +x ec2bot.py

WORKDIR /telegram-bot-ec2

COPY run.sh /telegram-bot-ec2

RUN chmod +x /telegram-bot-ec2/run.sh

ENTRYPOINT ["./run.sh"]
