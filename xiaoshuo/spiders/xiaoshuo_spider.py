# coding=utf-8

import scrapy
import re
from xiaoshuo.items import XiaoshuoItem

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjaGFubmVsX2lkIjoiMjcyNCIsInN1YiI6MzU3NjE4MzIxLCJpc3MiOiJodHRwOlwvXC93eDY4MTEzYTgyYzY2NTQwMjUueW91c2h1Z2UuY29tIiwiaWF0IjoxNTM0ODM1NDAyLCJleHAiOjE1MzU0NDAyMDIsIm5iZiI6MTUzNDgzNTQwMiwianRpIjoiT2MwWnBrNGdBb1BiTkNmWiJ9.KWpyPExzmOOMOySqDOvnR2r5eg-j65qmQvXUIw8jXnQ"
headers = {'Origin': 'https://wx68113a82c6654025.youshuge.com'}
l = []

class QuotesSpider(scrapy.Spider):
    name = "xiaoshuo"

    def start_requests(self):
        global token
        global headers
        global l

        # yield scrapy.Request(url=url, callback=self.parse)
        yield scrapy.FormRequest(
            url = "https://api.youshuge.com/new_home",
            formdata = {"token":token},
            callback = self.parse
        )

    def parse(self, response):
        if re.match('https://api.youshuge.com/new_home',response.url):
            s = response.body.decode('unicode_escape')
            while s != "}":
                s = s[s.find('"id":'):]
                if s[5:s.find(',"')]:
                    l.append(s[5:s.find(',"')])
                s = s[s.find(',"'):]
            else:
                for i in l[:1]:
                    yield scrapy.FormRequest(
                        url = "https://api.youshuge.com/getbookinfo",
                        formdata = {"token":token,"id":i},
                        callback = self.parse
                        )
        elif re.match('https://api.youshuge.com/getbookinfo',response.url):
            d = eval(response.body.decode('unicode_escape').replace('\\','').replace('\r\n','').replace('""','"').replace('null','""'))
            yield scrapy.FormRequest(
                url = "https://api.youshuge.com/getcontent",
                headers = headers,
                formdata = {"token":token,"bookid":str(d['data']['id']),'chapteid':str(d['data']['read_chapte'])},
                callback = self.parse
            )
        elif re.match('https://api.youshuge.com/getcontent',response.url):
            d = eval(response.body.decode('unicode_escape').replace('\\','').replace('\r\n','').replace('""','"').replace('null','""'))
            if d['msg'] != '余额不足':
                item = XiaoshuoItem()
                item['book_id'] = d['data']['book_id']
                item['chapte_id'] = d['data']['chapte']['id']
                item['chapte_name'] = d['data']['chapte_name']
                item['content'] = d['data']['content']
                yield item
                if d['data']['next_chapte']:
                    yield scrapy.FormRequest(
                        url = "https://api.youshuge.com/getcontent",
                        headers = headers,
                        formdata = {"token":token,"bookid":str(d['data']['book_id']),'chapteid':str(d['data']['next_chapte'])},
                        callback = self.parse
                    )
