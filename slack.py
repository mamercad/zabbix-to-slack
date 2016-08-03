#!/usr/bin/env python

import datetime
import logging
import json
import re
import requests
import sys

try:

  # slack api endpoint
  SLACK_API = 'https://slack.com/api/chat.postMessage'
  SLACK_USERNAME = 'Zabbix'
  SLACK_ICON = 'https://github.com/mamercad/zabbix-to-slack/raw/master/zabbix.png'

  # zabbix color lookup
  COLOR = {
    'OK': '#00AA00',
    'PROBLEM': {
      'Not classified': '#97AAB3',
      'Information': '#7499FF',
      'Warning': '#FFC859',
      'Average': '#FFA059',
      'High': '#E97659',
      'Disaster': '#E45959'
    }
  }

  # enable logging
  logging.basicConfig(filename='/tmp/slack.log', level=logging.DEBUG)

  # parse the command line args
  AUTHTOKEN_COMMA_CHANNEL = sys.argv[1]
  SUBJECT_NAME = sys.argv[2]
  MESSAGE_FULL = sys.argv[3]

  # logging start
  logging.debug('{} {} {}'.format('='*20, str(datetime.datetime.now()), '='*20))
  logging.debug(sys.argv)

  # parse the args further
  (AUTH_TOKEN, SLACK_CHANNEL) = AUTHTOKEN_COMMA_CHANNEL.split(',')
  (SUBJECT, NAME) = SUBJECT_NAME.split(': ')
  (TRIGGER, STATUS, SEVERITY, URL, VALUE, EVENT) = MESSAGE_FULL.split('____')

  # logging.debug(TRIGGER + ',' + STATUS + ',' + SEVERITY + ',' + URL + ',' + VALUE + ',' + EVENT)

  DISPLAY_COLOR = ''
  if SUBJECT == 'PROBLEM':
    DISPLAY_COLOR = COLOR['PROBLEM'][SEVERITY]
  else:
    DISPLAY_COLOR = COLOR['OK']

  # prepare slack payload
  payload = {
      'token': AUTH_TOKEN,
      'channel': SLACK_CHANNEL,
      'username': SLACK_USERNAME,
      'as_user': 'false',
      'icon_url': SLACK_ICON,
      'text': SUBJECT_NAME,
      'attachments': json.dumps([
          {
              'fields': [
                  {'title': 'Trigger', 'value': TRIGGER, 'short': 'true'},
                  {'title': 'Trigger status', 'value': STATUS, 'short': 'true'},
                  {'title': 'Trigger severity', 'value': SEVERITY, 'short': 'true'},
                  {'title': 'Trigger URL', 'value': URL, 'short': 'true'},
                  {'title': 'Item value', 'value': VALUE, 'short': 'true'},
                  {'title': 'Original event ID', 'value': EVENT, 'short': 'true'}
              ],
              'color': DISPLAY_COLOR
          }
      ])
  }

  # logging.debug(json.dumps(payload))

  # post the alert to slack
  r = requests.post(SLACK_API, data=payload)
  logging.debug(r.status_code)
  logging.debug(r.json())

except Exception as e:

  logging.debug(e, exc_info=True)
