#!/usr/bin/python
import os
import socket
import telepot
import datetime
from telepot.loop import MessageLoop
from telepot.delegate import pave_event_space, per_chat_id, create_open


UDP_BIND_IP = '0.0.0.0'
UDP_BIND_PORT = 514
BUFFER_SIZE = 1024
TELEGRAM_BOT_KEY = '1854081083:AAGXNqB_eNjm-ca8fZ4LqgAmYTd6XI1hgf0'
TELEGRAM_IDS = [
]

def load_chat_ids():
	global TELEGRAM_IDS
	with open('chat_ids', 'r') as f:
		TELEGRAM_IDS = [int(chat_id.rstrip("\n")) for chat_id in f.readlines() if chat_id.rstrip("\n") != '']

def save_chat_ids():
	global TELEGRAM_IDS
	with open('chat_ids', 'w') as f:
		f.writelines([str(chat_id)+"\n" for chat_id in TELEGRAM_IDS])

def write_log(msg):
	now = datetime.datetime.now()
	date = '{}-{}-{} {}:{}:{}'.format(
		now.year,
		now.month,
		now.day,
		now.hour,
		now.minute,
		now.second
	) 
	
	logfile = 'logs/{}-{}-{}.txt'.format(now.year, now.month, now.day)
	
	with open(logfile, 'a') as f:
		f.write("{date}: {message}\n".format(date=date, message=msg))
		
load_chat_ids()

bot = telepot.Bot(TELEGRAM_BOT_KEY)

def announce(message):
	global TELEGRAM_IDS
	write_log(message)
		
	for telegram_id in TELEGRAM_IDS:
		print('Sending {message} to {telegram_id}'.format(
			message=message,
			telegram_id=telegram_id
			)
		)
		
		try:
			bot.sendMessage(telegram_id, message)
		except telepot.exception.TelegramError:
			print('Bot error: [{}] {}'.format(telegram_id, message))
			write_log('Bot error: [{}] {}'.format(telegram_id, message))

def handle(msg):
	global TELEGRAM_IDS
	content_type, chat_type, chat_id = telepot.glance(msg)
	
	if chat_id not in TELEGRAM_IDS:
		TELEGRAM_IDS.append(chat_id)
		save_chat_ids()
		
		message = '/!\\ NEW USER USES BOT: {} /!\\'.format(chat_id)
		announce(message)

def main():
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_BIND_IP, UDP_BIND_PORT))

	while True:
		data, addr = sock.recvfrom(BUFFER_SIZE) 
		
		address = addr[0]
		log = data.decode('ascii')
		
		message = '{address}: {log}'.format(
			address=address,
			log=log
		)
		
		announce(message)
		
	main()
	
if __name__ == '__main__':
	MessageLoop(bot, handle).run_as_thread()
	main()
