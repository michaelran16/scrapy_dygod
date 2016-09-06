# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlerDygodSpider(CrawlSpider):
    name = 'crawler_dygod'
    allowed_domains = ['www.dygod.net']
    start_urls = ['http://www.dygod.net/html/gndy/oumei/index.html']

    rules = (
        # 欧美电影 item list
        Rule(LinkExtractor(allow='\/html\/gndy\/oumei\/')),
        # 精品电影 item page
        Rule(LinkExtractor(allow='\/html\/gndy\/dyzz\/\d+\/\d+\.html'), callback='parse_item', follow=True),
        # 综合电影 item page
        Rule(LinkExtractor(allow='\/html\/gndy\/jddy\/\d+\/\d+\.html'), callback='parse_item', follow=True),
    )

    # rules = (
    #     Rule(LinkExtractor(allow=('\/search.php.*page=', ), )),
    #     Rule(LinkExtractor(allow=('\/details\/', )), callback='parse_item'),
    # )

    def parse_item(self, response):
        i = {}

        self.logger.info('now crawling item page: %s', response.url)
        result = response.xpath('//div[@class="co_area2"]')

        i['title'] = result.xpath('div[@class="title_all"]/h1/text()').extract()
        # TODO: fix the image xpath
        # i['image'] = result.xpath('div[@class="co_content8"]/ul/div[@id="Zoom"]/p/img/@src').extract()
        # i['image'] = result.xpath('div[@class="co_content8"]/ul/div/text()').extract()
        i['image'] = result.xpath('//div[@id="Zoom"]/p/img/@src').extract()

        # i['download_link'] = result.xpath('//div[@id="description"]').extract()
        return i
