import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = [f'https://{domain}/' for domain in allowed_domains]

    def parse(self, response):
        for link in response.css(
            'section#numerical-index tbody > tr a[href*="pep-"]'
        ):
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        row = response.css('h1.page-title::text').get().strip().split(' – ')
        number = row[0].split(' ')[1]
        title = row[1]
        status = response.css('dt:contains("Status") + dd abbr::text').get()
        yield PepParseItem(number=number, name=title, status=status)
