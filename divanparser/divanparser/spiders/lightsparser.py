import scrapy


class LightsparserSpider(scrapy.Spider):
    name = "lightsparser"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet"]

    def parse(self, response):
        lights = response.css('div.WdR1o')

        for svet in lights:
            root = svet.css('div.lsooF')
            prices = root.xpath('div[@class="pY3d2"]/div/span[@class="ui-LD-ZU KIkOH" and @data-testid="price"]')

            yield {
            'name' : root.css('span::text').get(),
            'price' : prices.xpath('text()').get().strip(),
            'currency' : prices.xpath('span/text()').get().strip(),
            'url' : svet.css('a').attrib['href'],
            'abs_url': root.xpath('link[@itemprop="url"]/@href').get().strip()
            }
