import scrapy
from ..items import ScrapyprojectItem

class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    start_urls = [
        "http://quotes.toscrape.com/login"
    ]
    def parse(self, response):
       token = response.css('form input::attr(value)').extract_first()
       return FormRequest.from_response(response,formdata={
           'csrf_token' : token,
           'username' : 'hey',
           'password' : 'ssss'
       },callback=self.start_scrapping)

    def start_scrapping( self , response):
        items = ScrapyprojectItem()
        all_div_quotes = response.css('div.quote')
        for quotes in all_div_quotes:
            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tag = quotes.css('.tag::text').extract()
            items['title'] = title
            items['author'] = author
            items['tag'] = tag
            yield items
        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, callback = self.parse)
