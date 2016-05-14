# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import logging
import urllib
from quant.core.Spider import *
from quant.core.Spider import *
UA = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"


class TouTiaoDetailSpider(SpiderEngine):

    def __init__(self):
        SpiderEngine.__init__(self)

    def get_info(self, vid):
        pass
        #self.get_from_news(url)
        #self.get_wx_url(vid)

    def run(self):
        print sys.argv
        self.tools.setup_logging(sys.argv[1], True, True)
        quncms_db = self.config['mysql']['quncms']
        mysql = sMysql(quncms_db['host'], quncms_db['user'], quncms_db['password'], quncms_db['dbname'])

        while 1:
            data = mysql.fetch_one("select * from video_contents where is_done=0")
            if data is None:
                break

            url = "http://www.toutiao.com%s" % data['item_seo_url']
            print url
            logging.debug('===%s===url:%s' % (data['itemid'], url))
            status = urllib.urlopen("http://www.toutiao.com/i6282880816871637505/").code
            if status == 404:
                mysql.dbQuery("DELETE FROM video_contents where itemid=%s" % data['itemid'])
            else:
                html = self.sGet(url, 'utf-8')
                tag = self.sMatch("tt-videoid='", "'", html, 0)
                if len(tag) == 0:
                    up = {'is_done': 1}
                else:
                    up = {'video_url': tag[0], 'is_done': 1}

                mysql.dbUpdate('video_contents', up, "itemid=%s" % data['itemid'])