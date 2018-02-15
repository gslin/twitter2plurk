#!/usr/bin/env python3

import configparser
import os

class Twitter2Plurk(object):
    def __init__(self):
        pass

    def start(self):
        f = '{}/.config/twitter2plurk/config.ini'.format(os.environ['HOME'])

        c = configparser.ConfigParser()
        c.read(f)

        self.twitter_ac = c['default']['twitter_access_token'])
        self.twitter_as = c['default']['twitter_access_token_secret'])
        self.twitter_ck = c['default']['twitter_consumer_key'])
        self.twitter_cs = c['default']['twitter_consumer_secret'])

if '__main__' == __name__:
    t = Twitter2Plurk()
    t.start()
