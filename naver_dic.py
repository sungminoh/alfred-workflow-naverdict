#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2019 sungminoh <smoh2044@gmail.com>
#
# Distributed under terms of the MIT license.

"""

"""



# -*- coding:utf-8 -*-

import itertools
import urllib.parse
import urllib.request
import json
import unicodedata
import re
from workflow import Workflow

import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")


class NaverDic(Workflow):
    URL = u'https://ac-dict.naver.com/enko/ac?st=11&r_lt=11&q=%s&_callback=jQuery37103379876023806727_1715747892073&_=1715747892074'

    def __init__(self):
        super(NaverDic, self).__init__()

    def search(self, query):
        unicode_query = u'%s' % query
        # escaped_query = urllib.quote(unicodedata.normalize('NFC', unicode_query).encode('utf-7'))
        escaped_query = urllib.parse.quote(unicodedata.normalize('NFC', unicode_query).encode('utf-7'))
        req = urllib.request.urlopen(self.URL % escaped_query)
        text = req.read().decode(req.headers.get_content_charset())
        # unparsed = re.match(r'window[^\(]*\((.*)\)', urllib.urlopen(self.URL % escaped_query).read(), re.DOTALL).groups()[1]
        unparsed = re.match(r'[^(]*\((.*)\)', text.replace('\n', '')).groups()[0]
        obj = json.loads(unparsed)
        for item in itertools.chain(obj["items"][0], obj["items"][1]):
            if len(item) < 2:
                continue
            en = item[0][0]
            ko = item[2][0]
            ko = ko.replace('<b>', '')
            ko = ko.replace('</b>', '')
            word = u'%s: %s' % (en, ko)
            self.add_item(word, '네이버 영어 사전에서 &quot;%s&quot; 검색' % en, arg=en, icon='icon.png', valid=True)
        return self


def main():
    NaverDic().search(' '.join(sys.argv[1:])).send_feedback()


if __name__ == '__main__':
    main()
