#!/usr/bin/env python3

import configparser
import os
import twitter

class Twitter2Plurk(object):
    def __init__(self):
        pass

    def start(self):
        f = '{}/.config/twitter2plurk/config.ini'.format(os.environ['HOME'])

        c = configparser.ConfigParser()
        c.read(f)

        t_ak = c['default']['twitter_access_token']
        t_as = c['default']['twitter_access_token_secret']
        t_ck = c['default']['twitter_consumer_key']
        t_cs = c['default']['twitter_consumer_secret']
        t_user = c['default']['twitter_username']

        self.t = twitter.Api(access_token_key=t_ak, access_token_secret=t_as, consumer_key=t_ck, consumer_secret=t_cs)

        for status in sorted(list(self.t.GetUserTimeline(screen_name=t_user)), key=lambda x: x.id):
            text = status.text
            for u in status.urls:
                text = text.replace(u.url, u.expanded_url)

if '__main__' == __name__:
    t = Twitter2Plurk()
    t.start()
