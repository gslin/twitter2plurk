#!/usr/bin/env python3

import os

class Twitter2Plurk(object):
    def __init__(self):
        pass

    def start(self):
        f = '{}/.config/twitter2plurk/config.ini'.format(os.environ['HOME'])

if '__main__' == __name__:
    t = Twitter2Plurk()
    t.start()
