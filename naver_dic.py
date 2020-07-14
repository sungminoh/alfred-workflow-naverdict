#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 smoh10 <smoh2044@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""



# -*- coding:utf-8 -*-

import urllib
import json
import unicodedata
import re
from workflow import Workflow

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class NaverDic(Workflow):
    URL = u'https://ac.dict.naver.com/enendict/ac?_callback=window.__jindo2_callback.$8430&q=%s&q_enc=utf-8&st=11001&r_format=json&r_enc=utf-8&r_lt=11001&r_unicode=0&r_escape=1'

    def __init__(self):
        super(NaverDic, self).__init__()

    def search(self, query):
        unicode_query = u'%s' % query
        escaped_query = urllib.quote(unicodedata.normalize('NFC', unicode_query).encode('utf-8'))
        unparsed = re.match(r'window[^\(]*\((.*)\)', urllib.urlopen(self.URL % escaped_query).read(), re.DOTALL).groups()[0]
        obj = json.loads(unparsed)
        for item in obj["items"][0]:
            if len(item) < 2:
                continue
            en = item[0][0]
            ko = item[1][0]
            ko = ko.replace('<b>', '')
            ko = ko.replace('</b>', '')
            word = u'%s: %s' % (en, ko)
            self.add_item(word, '네이버 영어 사전에서 &quot;%s&quot; 검색' % en, arg=en, icon='icon.png', valid=True)
        return self


def main():
    NaverDic().search(' '.join(sys.argv[1:])).send_feedback()


if __name__ == '__main__':
    main()
