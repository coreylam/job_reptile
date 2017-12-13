##1. 创建项目文档##
在目标路径下，打开命令行，使用如下命令创建项目，例如项目名称为 "tutorial"：

	scrapy startproject tutorial

*- 创建项目时，会自动创建对应的目录，所以没有必要自己先预先创建项目名称的目录*

##2. 使用pycharm创建项目##
由于是在windows下采用pycharm的IDE进行开发，因此直接在pycharm上创建一个项目，目录为第一步用命令创建的目录。

如果不想用IDE，也可以直接用文本编辑器编辑，或者使用其他IDE。

##3. 修改item##
使用第一步的命令创建项目后，会有默认的item类，如果有必要的话，可自行的该类中添加对应的item字段，如：

	class DmozItem(scrapy.Item):
	    # define the fields for your item here like:
	    # name = scrapy.Field()
	    title = scrapy.Field()
	    link = scrapy.Field()
	    desc = scrapy.Field()

##4. 创建spider##
在 `spiders/` 目录下创建对应的spider文件，如 `demo_spider.py`

	import scrapy
	from tutorial.items import DmozItem
	
	class DmozSpider(scrapy.Spider):
	    name = "dmoz"
	    allowed_domains = ["dmoz.org"]
	    start_urls = [
	        "http://dmoztools.net/Computers/Programming/Languages/Python/Books/",
	    ]

	    def parse(self, response):
	        for sel in response.xpath('//ul/li'):
	            item = DmozItem()
	            item['title'] = sel.xpath('a/text()').extract()
	            item['link'] = sel.xpath('a/@href').extract()
	            item['desc'] = sel.xpath('text()').extract()
	            yield item


上述代码简要说明如下： 

1) `from tutorial.items import DmozItem`：导入 `Item` 类

2) `name = "dmoz"`：spider的名字，在一个项目中，每个spider的名字都必须是唯一的，这个名字在运行时需要被指定，如要运行上述spider的命令为： `scrapy crawl dmoz`

3) `strat_urls`： 用来指定目标url的数组，scrapy会根据这个数组中的url，逐个去产生Request请求，可以说是“爬虫”的入口或者起始点；除了通过数组方式指定外，也可以用函数的方式生成，指定对应的url和回调函数，例如：

	def start_requests(self):
	   url_page = "http://dmoztools.net/Computers/Programming/Languages/Python/Books/"
	   yield scrapy.Request(url=url_page, callback=self.parse)

4）`yield item`：产生item数据，用于将item输出

5）另外还有一种简便的方法可以直接在命令行中创建spider，进入的项目目录，然后使用如下命令创建spider文件，例如：

	scrapy genspider example example.com
这样就可以自动在 `spiders/` 目录下创建一个 "example.py"的文件，文件内容如下

	# -*- coding: utf-8 -*-
	import scrapy
	
	
	class ExampleSpider(scrapy.Spider):
	    name = 'example'
	    allowed_domains = ['example.com']
	    start_urls = ['http://example.com/']
	
	    def parse(self, response):
	        pass


##5. 使用shell进行调试##

对于大部分情况来说，可能不像例子这样，直接就把 parse 函数写出来了，中间肯定要一点一点去提取相关的有用信息，确认ok之后再一点一点往 parse 函数里面添， shell 的调用方式为在命令行下输入如下命令：

	scrapy shell http://目标url

这部分参见另外的文章，在此不做赘述。

##6. 运行spider##

调试完成之后，就可以把爬虫运行起来了，运行方式如下：

	scrapy crawl dmoz

如果需要把结果输出，可以采用 `-o` 设置输出文件，如：

	scrapy crawl dmoz -o dmoz.json

##说明##
- 本文中的例子的代码来自[Scrapy说明文档][1]中的例子，不过用自己的语言和理解重新整理了思路，便于入手理解，但不是很全面，详细的内容可以参考官方文档；
[1]:http://scrapy.readthedocs.io/en/latest/
