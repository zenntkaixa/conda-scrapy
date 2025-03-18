import scrapy
from scrapy import Request


"""
Scrapy spider to scrape book details from Audible's search results.
"""
class AudibleSpider(scrapy.Spider):
    name = "audible" # Name of the spider
    allowed_domains = ["www.audible.com"] # Restrict crawling to this domain
    start_urls = ["https://www.audible.com/search"] # Starting URL

    """
    Override the start_requests method to add custom headers.
    """
    def start_requests(self):
        yield scrapy.Request(
            url= 'https://www.audible.com/search',
            callback= self.parse,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'} # Custom headers to mimic a real browser
        )

    """
    Parse the search results page and extract book details.
    """
    def parse(self, response):
        # Extract all product containers using XPath
        product_container = response.xpath('//div[@class="adbl-impression-container "]//li[contains(@class, "productListItem")]')

        # Loop through each product container
        for product in product_container:
            book_title = product.xpath('.//h3[contains(@class, "bc-heading")]/a/text()').get()
            book_author = product.xpath('.//li[contains(@class, "authorLabel")]//a/text()').getall()
            book_length = product.xpath('.//li[contains(@class, "runtimeLabel")]/span/text()').get()

            # Yield the extracted data as a dictionary
            yield {
                'title': book_title,
                'author': book_author,
                'length': book_length
            }

        # Extract the URL for the next page if the "Next" button is not disabled
        pagination = response.xpath('//ul[contains(@class, "pagingElements")]')
        next_page_url = pagination.xpath('.//span[contains(@class, "nextButton")]/a[not(@aria-disabled="true")]/@href').get()

        # Follow the next page link if it exists and is not disabled
        if next_page_url:
            yield response.follow(
                url=next_page_url,
                callback=self.parse, # Use the same parse method to handle the next page
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36'} # Include custom headers for the next request
            )