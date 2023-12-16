import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = "pep"
    allowed_domains = ["peps.python.org"]
    start_urls = ["https://peps.python.org",]

    def parse(self, response):
        rows = response.css('table.pep-zero-table tbody tr')
        for row in rows:
            link = row.css('td:nth-child(2) a::attr(href)').get()

            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        row = response.css('h1.page-title::text').get().strip().split(' – ')
        number = row[0].split(' ')[1]
        title = row[1]
        status = response.css('dt:contains("Status") + dd abbr::text').get()
        data = {
            'number': number,
            'name': title,
            'status': status,
        }
        yield PepParseItem(data)
