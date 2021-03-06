# How to Setup a crawler for www.dygod.net

## Quick setup

reference [here](http://doc.scrapy.org/en/latest/topics/commands.html?highlight=template#genspider)

    scrapy startproject scrapy_dygod
    cd scrapy_dygod
    scrapy genspider -l
    scrapy genspider -t crawl crawler_dygod www.dygod.net


Now go ahead and make some modifications to 

1. items.py
1. spider/crawler_dygod.py
1. pipelines.py

# Coding!

## items.py

Look at one of the item page, what information do we need? 

    class ScrapyDygodItem(scrapy.Item):
        title = scrapy.Field()
        image = scrapy.Field()
        download_link = scrapy.Field()
        pass

So far, so good. 

## spider/crawler_dygod.py

### part 1: crawling rules

> __[callback](http://doc.scrapy.org/en/latest/topics/spiders.html#crawling-rules)__ is a callable or a string to be called for each link extracted with the specified link_extractor. 
>
> This callback receives a response as its first argument and must return a list containing Item and/or Request objects (or any subclass of them).

> __[follow](http://doc.scrapy.org/en/latest/topics/spiders.html#crawling-rules)__ is a boolean which specifies if links should be followed from each response extracted with this rule. 
>
> __If callback is None__ follow defaults to __True__, otherwise it defaults to __False__.

The most basic crawling rule I come up with is like this: 

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

Now, we just need to implement parse_item() function. 

At this stage, we are ready to test the crawler. However before doing so, one last step is to set a time gap of delay in settings.py

    DOWNLOAD_DELAY = 3

(otherwise you will received error like this:)

    [<twisted.python.failure.Failure twisted.internet.error.ConnectionDone: Connection was closed cleanly.>]

or 

    Connection to the other side was lost in a non-clean fashion: Connection lost.

### part 2: parse_item() function

Important to know how xpath() works. Here are some key points:

1. For absolute path, use "//"; for relative path, do not use "/"

1. We can assign a section xpath to another xpath variable, eg

    result = response.xpath('//div[@class="co_area2"]')

1. xpath() can extract by class, id or by property

    xpath('div[@class="co_content8"]/ul/div[@id="Zoom"]/p/img/@src').extract()

## pipelines.py

# Useful stuff

## Learn xpath by examples

    result.xpath('//div[@class="items"]/div/div')
    result.xpath('//div[@id="Zoom"]/p/img/@src').extract()
    result.xpath('span[@class="pl_lst_rt"]/text()').extract()[0]
    result.xpath('img/@src').extract()[0])
    result.xpath('a/@href').extract()[0]
    result.xpath('div[2]/a/text()').extract()

## log to command line

In the crawler class, do:

    self.logger.info('now crawling item page: %s', response.url)

If not in the crawler class, define your own logger:

    import logging
    logger = logging.getLogger('pipeline')

    logger.warning("Item dropped because no title: " + item['url'])

## Suppress item logging

Set LOG_LEVEL = 'INFO' if you wish to suppress item content logging in console

    # CRITICAL, ERROR, WARNING, INFO, DEBUG
    LOG_LEVEL = 'INFO'

## scrapy parse command

We can use command line to debug: 

    scrapy parse --spider=crawler_dygod -c parse_item --pipelines http://www.dygod.net/html/gndy/jddy/20130718/42744.html

in the format of

    =====
      scrapy parse [options] <url>

    Parse URL (using its spider) and print the results

    Options
    =======
    --help, -h              show this help message and exit
    --spider=SPIDER         use this spider without looking for one
    -a NAME=VALUE           set spider argument (may be repeated)
    --pipelines             process items through pipelines
    --nolinks               don't show links to follow (extracted requests)
    --noitems               don't show scraped items
    --nocolour              avoid using pygments to colorize the output
    --rules, -r             use CrawlSpider rules to discover the callback
    --callback=CALLBACK, -c CALLBACK
                            use this callback for parsing, instead looking for a
                            callback
    --depth=DEPTH, -d DEPTH
                            maximum depth for parsing requests [default: 1]
    --verbose, -v           print each depth level one by one

## the .gitignore file

Reference: [scrapy-example-project](https://github.com/mattes/scrapy-example-project/blob/master/.gitignore):

    .DS_Store
    *.pyc
    *.egg-info
    build
    setup.py

# Run your crawler

    scrapy crawl crawler_dygod

Or

    scrapy crawl crawler_dygod -o output.json

## deploy to scrapinghub

We can deploy the crawlers to cloud and run on cloud.

    shub login
    shub deploy

Acquire your __Target project ID__ from "Code & Deploys" Section of https://app.scrapinghub.com 

After the deploy, use scrapinghub to run your crawler.

Job Done! 
