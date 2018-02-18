#!/usr/bin/env python3

import configparser
import plurk_oauth
import os
import sqlite3
import time
import twitter
import urllib

class Twitter2Plurk(object):
    def __init__(self):
        pass

    def start(self):
        home = os.environ['HOME']
        f_conf = '{}/.config/twitter2plurk/config.ini'.format(home)
        f_db = '{}/.config/twitter2plurk/entry.sqlite3'.format(home)

        c = configparser.ConfigParser()
        c.read(f_conf)

        t_ak = c['default']['twitter_access_token']
        t_as = c['default']['twitter_access_token_secret']
        t_ck = c['default']['twitter_consumer_key']
        t_cs = c['default']['twitter_consumer_secret']
        t_user = c['default']['twitter_username']
        t = twitter.Api(access_token_key=t_ak, access_token_secret=t_as, consumer_key=t_ck, consumer_secret=t_cs)

        p_ak = c['default']['plurk_app_key']
        p_as = c['default']['plurk_app_secret']
        p_tk = c['default']['plurk_token']
        p_ts = c['default']['plurk_token_secret']
        p = plurk_oauth.PlurkAPI(p_ak, p_as)
        p.authorize(p_tk, p_ts)

        s = sqlite3.connect(f_db)

        sql_insert = 'INSERT INTO entry (twitter_id, created_at) VALUES (?, ?);'
        sql_select = 'SELECT COUNT(*) FROM entry WHERE twitter_id = ?;'

        for status in sorted(list(t.GetUserTimeline(screen_name=t_user)), key=lambda x: x.id):
            # Generate "text"
            text = status.text
            for u in status.urls:
                text = text.replace(u.url, u.expanded_url)

            # Generate "url"
            url = 'https://twitter.com/{}/status/{}'.format(urllib.parse.quote(t_user), urllib.parse.quote(status.id_str))

            c = s.cursor()

            c.execute(sql_select, (status.id_str, ))
            if 0 == c.fetchone()[0]:
                content = '{} # {}'.format(text, url)
                print('* content = {}'.format(content))

                res = p.callAPI('/APP/Timeline/plurkAdd', {
                    'content': content,
                    'qualifier': ':',
                })

                print('* type(res) = {}'.format(type(res)))
                print('* res = {}'.format(res))
                if type(res) is dict and res['plurk_id'] > 0:
                    c.execute(sql_insert, (status.id_str, int(time.time())))
                    s.commit()
                else:
                    s.rollback()

if '__main__' == __name__:
    t = Twitter2Plurk()
    t.start()
