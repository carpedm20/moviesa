__author__ = 'Taehoon Kim'
__date__ = '2014.02.28'
from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.item import Item, Field

from scrapper.items import *
import urllib
import sys, os

import datetime, time

MOVIE_RANK_URL = "http://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=%s&date=%s"
PEOPLE_RANK_URL = "http://movie.naver.com/movie/sdb/rank/rpeople.nhn?date=%s"

MOVIE_DATA = ['cnt', 'cur', 'pnt']

START_YEAR = 2005
START_MONTH = 2
START_DATE = 7

cur_date = datetime.date(START_YEAR, START_MONTH, START_DATE) 
# cur_date_str = cur_date.strftime("%Y%m%d")

LOOP = 0
RANK = Rank()

class Naver(Spider):
    name = "naver"
    allowed_domains = ["movie.naver.com"]
    start_urls = [MOVIE_RANK_URL %('cnt', cur_date.strftime("%Y%m%d"))]

    def parse(self, response):
        global cur_date, RANK, LOOP

        if cur_date == datetime.date.today() - datetime.timedelta(days=1):
            return
        else:
            LOOP += 1

        cur_url = response.url

        sel = Selector(response)
        items = list()

        trs = sel.xpath("//tbody/tr")

        rank = 1
        for tr in trs:
            if 'rpeople' not in cur_url:
                link = tr.xpath("./td[@class='title']/div/a")
            else:
                link = tr.xpath("./td[@class='title']/a")

            if len(link) is 0:
                continue
            else:
                link = link[0]

            item = None
            if 'cnt' in cur_url:
                item = CntMovie()
                RANK['date'] = cur_date.strftime("%Y%m%d")
            elif 'cur' in cur_url:
                item = CurMovie()
            elif 'pnt' in cur_url:
                item = PntMovie()
            elif 'rpeople' in cur_url:
                item = People()

            if 'rpeople' not in cur_url:
                title = link.xpath('./@title')[0].extract()
            else:
                title = link.xpath('./text()')[0].extract()
                try:
                    birth = tr.xpath("./td[@class='ac']/img/@alt")[0].extract()
                    item['birth'] = birth
                except:
                    item['birth'] = ''
                
            href = link.xpath('./@href')[0].extract()

            item['rank'] = rank
            item['code'] = href[href.find('code=')+5:]
            item['title'] = title

            rank += 1
            items.append(dict(item))

        if 'cnt' in cur_url:
            RANK['cnt'] = items
            next_url = MOVIE_RANK_URL %('cur', cur_date.strftime("%Y%m%d"))
        elif 'cur' in cur_url:
            RANK['cur'] = items
            next_url = MOVIE_RANK_URL %('pnt', cur_date.strftime("%Y%m%d"))
        elif 'pnt' in cur_url:
            RANK['pnt'] = items
            next_url = PEOPLE_RANK_URL %cur_date.strftime("%Y%m%d")
        elif 'rpeople' in cur_url:
            RANK['people'] = items
            yield RANK

            RANK = Rank()
            cur_date += datetime.timedelta(days=1)
            next_url = MOVIE_RANK_URL %('cnt', cur_date.strftime("%Y%m%d"))

        yield Request(next_url, self.parse)
