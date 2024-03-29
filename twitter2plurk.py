#!/usr/bin/env python3

import configparser
import html
import os
import plurk_oauth
import re
import requests
import sqlite3
import time

from lxml.html.clean import Cleaner

class Twitter2Plurk(object):
    def __init__(self):
        pass

    def start(self):
        home = os.environ['HOME']
        f_conf = '{}/.config/twitter2plurk/config.ini'.format(home)
        f_db = '{}/.config/twitter2plurk/entry.sqlite3'.format(home)

        c = configparser.ConfigParser()
        c.read(f_conf)

        jsonfeed_url = c['default']['twitter_rssbridge_jsonfeed_url']
        items = requests.get(jsonfeed_url).json()['items']

        p_ak = c['default']['plurk_app_key']
        p_as = c['default']['plurk_app_secret']
        p_tk = c['default']['plurk_token']
        p_ts = c['default']['plurk_token_secret']
        p = plurk_oauth.PlurkAPI(p_ak, p_as)
        p.authorize(p_tk, p_ts)

        s = sqlite3.connect(f_db)

        sql_insert = 'INSERT INTO entry (twitter_id, created_at) VALUES (?, ?);'
        sql_select = 'SELECT COUNT(*) FROM entry WHERE twitter_id = ?;'

        cl = Cleaner(allow_tags=['a'])

        for item in items:
            # Skip if it's retweet.
            if item['title'].startswith('@'):
                continue

            # Print out details.
            print('* item = {}'.format(item))

            # Craft "text".
            #
            # First to remove all tags except "a" and root's "div".
            text = cl.clean_html(item['content_html'])

            # Remove root's "div".
            text = text.replace('<div>', '').replace('</div>', '')

            # Replace each "a" element with its href link and unescape.
            tokens = re.split(r'<a href="(.*?)">(?:.*?)</a>', text, flags=re.DOTALL)
            for i in range(1, len(tokens), 2):
                tokens[i] = re.sub(r'<a href="(.*?)">.*?</a>', r'\1', tokens[i], flags=re.DOTALL)
                tokens[i] = html.unescape(tokens[i])
            text = ''.join(tokens)

            # Generate parameters.
            id_str = item['url'].split('/')[-1]
            url = item['url']

            c = s.cursor()

            c.execute(sql_select, (id_str, ))
            if 0 == c.fetchone()[0]:
                content = '{}\n\n{}'.format(text, url)
                print('* content = {}'.format(content))

                res = p.callAPI('/APP/Timeline/plurkAdd', {
                    'content': content,
                    'qualifier': ':',
                })

                print('* type(item) = {}'.format(type(item)))
                print('* item = {}'.format(item))
                print('* type(res) = {}'.format(type(res)))
                print('* res = {}'.format(res))
                if type(res) is dict and res['plurk_id'] > 0:
                    c.execute(sql_insert, (id_str, int(time.time())))
                    s.commit()
                else:
                    s.rollback()

if '__main__' == __name__:
    t = Twitter2Plurk()
    t.start()
