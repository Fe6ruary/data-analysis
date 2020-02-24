# -*- coding: utf-8 -*-
import scrapy
from huxiuv1.items import Huxiuv1Item
import json
from lxml import etree


class Huxiu1Spider(scrapy.Spider):
    name = 'huxiu_1'
    #allowed_domains = ['huxiu.com']  #可爬取范围


    #start_urls = ['http://www.huxiu.com/index.php/']

    def start_requests(self):

        url = 'https://www.huxiu.com/v2_action/article_list'

        start_urls = 'http://www.huxiu.com/index.php/'
        yield scrapy.Request(start_urls, callback=self.parse)

        for i in range(2, 10):
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=url,
                formdata={"huxiu_hash_code": "cef610cd939cb93c4e756f78cad5a946", "page": str(i)},
                callback=self.parse_2,

                )


    def parse(self, response):  #response 为start_url请求后的反馈



        cl = response.xpath('//div[@class="mod-info-flow"]/div/div[contains(@class,"mob-ctt")]')

        for sel in cl:
            item = Huxiuv1Item()
            #item['title'] = sel.xpath('h2/a/text()').extract_first()
            item['link'] = sel.xpath('h2/a/@href').extract_first()
            url = response.urljoin(item['link'])
            item['desc'] = sel.xpath('div[@class="mob-sub"]/text()').extract_first()
            #print(item['title'], item['link'], item['desc'])
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_2(self, response):
        item = Huxiuv1Item()
        data = json.loads(response.text)
        s = etree.HTML(data['data'])

        titles = s.xpath('//a[@class="transition msubstr-row2"]/text()')
        links = s.xpath('//a[@class="transition msubstr-row2"]/@href')

        for i in range(len(titles)):
            link = links[i]
            title = titles[i]
            print(title)
            url = 'https://www.huxiu.com' + link
            print(url)
            yield scrapy.Request(url, callback=self.parse_article)





    def parse_article(self, response):

        item = Huxiuv1Item()
        item['title'] = response.xpath('//h1/text()').extract_first()
        item['link'] = response.url
        item['posttime'] = response.xpath('//span[@class="article__time"]/text()').extract_first()
        item['content'] = response.xpath('//div[@class="article__content"]/p/text()').extract()



        yield item




