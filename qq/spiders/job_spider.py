import scrapy
from liepin.items import QQItem
import time
from scrapy.http import Request

class JobSpider(scrapy.Spider):
    name = "qq_job"
    allowed_domains = ["tencent.com"]
    sz_it_url = "https://www.liepin.com/zhaopin/?ckid=30e557e826adc95b&fromSearchBtn=2&industries=040%2C420%2C010%2C030&init=-1&flushckid=1&dqs=050090&headckid=30e557e826adc95b&d_pageSize=40&siTag=1B2M2Y8AsgTpgAmY7PhCfg~DS2r9wrNQTXRAG6o3QhqZg&d_headId=5d23a34b915688d7fd2f87a3adca1558&d_ckId=5d23a34b915688d7fd2f87a3adca1558&d_sfrom=search_unknown&d_curPage=0"
    qq_sz_it_url = "http://hr.tencent.com/position.php?keywords=&lid=2218&tid=87"
    start_urls =[qq_sz_it_url,
                 ]
    url_list = [qq_sz_it_url]

    # def start_requests(self):
    #     cnt = 0
    #     max_cnt = len(LiepinSpider.url_list)
    #     while cnt<max_cnt:
    #         url = LiepinSpider.url_list[cnt]
    #         yield Request(url=url, callback=self.parse)
    #         time.sleep(10)
    #         cnt+=1
    #         max_cnt = len(LiepinSpider.url_list)
    #         self.log('===max_nt = %d'%max_cnt)
    #     pass

    # def parse(self, response):
    #     job_info_list = response.css('div.job-info')
    #     for job_info in job_info_list:
    #         title = job_info.xpath('h3/a/text()').extract()[0].strip()
    #     pass

    # def parse(self, response):
    #     self.parse_qq(response)

    def parse(self, response):
        base_url = "http://hr.tencent.com/"
        job_info_list = response.css('tr.even')+response.css('tr.odd')
        for job_info in job_info_list:
            # item = QQItem()
            name = job_info.xpath('td')[0]
            # item['name'] = name.xpath('a/text()').extract()[0]
            # item['type'] = job_info.xpath('td/text()')[0].extract()
            # item['hire_num'] = job_info.xpath('td/text()')[1].extract()
            # item['pos'] = job_info.xpath('td/text()')[2].extract()
            # item['date'] = job_info.xpath('td/text()')[3].extract()
            url = base_url + name.xpath('a/@href').extract()[0]
            yield Request(url=url, callback=self.parse_item)
        next_page = response.css('div.pagenav a#next')
        if next_page is not None:
            post_fix = next_page.xpath('@href').extract()[0]
            url_page = base_url+post_fix
            time.sleep(2)
            self.log(url_page)
            # LiepinSpider.url_list.append(url_page)
            yield Request(url=url_page, callback=self.parse)

    def parse_item(self, response):
        item = QQItem()
        item['name'] = response.css('tr.h td').xpath('text()').extract()[0]
        item['type'] = response.css('tr.c.bottomline td').xpath('text()').extract()[1]
        item['hire_num'] = response.css('tr.c.bottomline td').xpath('text()').extract()[2]
        item['pos'] = response.css('tr.c.bottomline td').xpath('text()').extract()[0]
        item['duty'] = response.css('tr.c')[1].css('ul.squareli li').xpath('text()').extract()
        item['condition'] = response.css('tr.c')[2].css('ul.squareli li').xpath('text()').extract()
        item['link'] = response.url
        item['date'] = ""
        time.sleep(2)
        yield item
        pass
