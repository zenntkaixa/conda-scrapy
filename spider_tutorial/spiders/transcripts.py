import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

"""
Scrapy spider to crawl and scrape movie transcripts from subslikescript.com.
"""
class TranscriptsSpider(CrawlSpider):
    name = "transcripts" # Name of the spider
    allowed_domains = ["subslikescript.com"] # Restrict crawling to this domain
    start_urls = ["https://subslikescript.com/movies_letter-X"] # Starting URL

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,  # Sets a download delay of 0.5 seconds to avoid overwhelming the server
    }

    rules = (
        # Rule for extracting links to individual movie transcript pages.
        # It looks for links within the 'scripts-list' unordered list.
        Rule(LinkExtractor(restrict_xpaths=('//ul[@class="scripts-list"]//a')),
             callback="parse_item", # Callback method to parse the movie transcript page
             follow=True), # Follow links to other pages

        # Rule for extracting the link to the next page of movie listings.
        # It looks for the first anchor tag with rel="next".
        Rule(LinkExtractor(restrict_xpaths=('(//a[@rel="next"])[1]'))), # Follow the pagination links
    )

    """
    Parses the individual movie transcript page.
    Args:
        response (scrapy.http.Response): The response object.
    """
    def parse_item(self, response):
        article = response.xpath('//article[@class="main-article"]')
        transcript_list = article.xpath('./div[@class="full-script"]//p/text()').getall()
        transcript_string = ' '.join(transcript_list) # Combine all paragraphs into a single string

        # Yield the extracted data as a dictionary
        yield {
            'title': article.xpath('./h1/text()').get(),
            'plot': article.xpath('./p/text()').get(),
            'transcript': transcript_string,
            'url': response.url
        }
