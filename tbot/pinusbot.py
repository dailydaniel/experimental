#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import argparse

from functools import reduce
import re

from telegram.ext import Updater
from telegram.ext import CommandHandler  
from telegram.ext import MessageHandler, Filters

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--token', default='', type=str)
    parser.add_argument('-u', '--username', default='', type=str)
    parser.add_argument('-p', '--password', default='', type=str)
    parser.add_argument('-i', '--ip', default='', type=str)
    return parser


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

def message(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=convert(update.message.text))

def convert(text: str):
    text = [convertToPinus(word).lower() for word in text.split()]
    return reduce(lambda a, b: a + ' ' + b, text)


def convertToPinus(text: str):
    gl = 'аАоОуУэЭыЫюЮяЯиИеЕёЁaAeEyYuUiIoO'
    gl = list(gl)
    pattern = 'хуй'

    for i, letter in enumerate(list(text)):
        if letter in gl:
            if i < len(text) - 1:
                if list(text)[i+1] in gl:
                    pattern += text[i+1:]
                    return pattern
                else:
                    pattern += text[i:]
                    return pattern
            else:
                pattern += text[i:]
                return pattern


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
    
    TOKEN = namespace.token
    REQUEST_KWARGS={
        'proxy_url': namespace.ip,
        # Optional, if you need authentication:
        'urllib3_proxy_kwargs': {
            'username': namespace.username,
            'password': namespace.password,
        }
    }
    updater = Updater(TOKEN, request_kwargs=REQUEST_KWARGS)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    # echo_handler = MessageHandler(Filters.text, echo)
    # dispatcher.add_handler(echo_handler)

    mes = MessageHandler(Filters.text, message)
    dispatcher.add_handler(mes)

    updater.start_polling()
