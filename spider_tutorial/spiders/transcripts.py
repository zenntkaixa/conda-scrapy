import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class TranscriptsSpider(CrawlSpider):
    name = "transcripts"
    allowed_domains = ["subslikescript.com"]
    start_urls = ["https://subslikescript.com/movies_letter-X"]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,  # Sets a download delay of 0.5 seconds
    }

    rules = (
        # Rule for extracting links to individual movie transcript pages.
        # It looks for links within the 'scripts-list' unordered list.
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="scripts-list"]//a')), callback="parse_item", follow=True),
        # Rule for extracting the link to the next page of movie listings.
        # It looks for the first anchor tag with rel="next".
        Rule(LinkExtractor(restrict_xpaths=('(//a[@rel="next"])[1]'))),
    )

    """
    Parses the individual movie transcript page.
    Args:
        response (scrapy.http.Response): The response object.
    """
    def parse_item(self, response):
        article = response.xpath('//article[@class="main-article"]')

        yield {
            'title': article.xpath('./h1/text()').get(),
            'plot': article.xpath('./p/text()').get(),
            # 'transcript': article.xpath('./div[@class="full-script"]//p/text()').getall(),
            'url': response.url
        }
