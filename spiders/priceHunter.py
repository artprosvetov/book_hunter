# -*- coding: utf-8 -*-
import scrapy
from ..items import PriceMonitorItem


class PricehunterSpider(scrapy.Spider):
    name = "priceHunter"
    allowed_domains = ["labirint.ru"]
    start_urls = [
    'http://www.labirint.ru/search/%D0%94%D0%BE%D1%81%D1%82%D0%BE%D0%B5%D0%B2%D1%81%D0%BA%D0%B8%D0%B9%20%D0%A4%D0%B5%D0%B4%D0%BE%D1%80%20%D0%9C%D0%B8%D1%85%D0%B0%D0%B9%D0%BB%D0%BE%D0%B2%D0%B8%D1%87/?id_genre=-1&nrd=1&display=annotation',
    'http://www.labirint.ru/search/%D0%BB%D0%B5%D0%B2%20%D1%82%D0%BE%D0%BB%D1%81%D1%82%D0%BE%D0%B9/?display=annotation',
    'http://www.labirint.ru/search/%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80%20%D0%9F%D1%83%D1%88%D0%BA%D0%B8%D0%BD/?id_genre=-1&nrd=1&display=annotation',
    'http://www.labirint.ru/search/%D1%88%D0%B5%D0%BA%D1%81%D0%BF%D0%B8%D1%80/?id_genre=-1&nrd=1&display=annotation']

    def parse(self, response):
        for href in response.css('div.products-row > div.product-annotation ::attr(href)'):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_detail_page)
            


    def parse_detail_page(self, response):
        book = PriceMonitorItem() 
        test_autor = response.css('div.product-author > a ::attr(title)').extract()
        test_autor = ' '.join(test_autor)
        test_title = response.css('span.product-title ::text').extract()
        test_title = ' '.join(test_title)
        if len(test_autor) < 64 and len(test_title)<64:           
            book['title'] = test_title #response.css('span.product-title ::text').extract()
            book['autor'] = test_autor #response.css('div.product-author > a ::attr(title)').extract()
            book['price'] = response.css('span.price-val > span ::text').extract()
            book['pub_house'] = response.css('div.product-pubhouse > a > span ::text').extract()[0]
            #book['series'] = response.css('div.product-pubhouse > a > span ::text').extract()[1]
            #book['description'] = response.css('div.annotation ::text').extract()
            book_id = response.css('div.product::attr(data-product-id)').extract()[0]          
            book['url'] = 'http://www.labirint.ru/books/' + book_id
            book['img'] = 'http://img1.labirint.ru/books/' + book_id + '/big.jpg'
            yield book
            
          