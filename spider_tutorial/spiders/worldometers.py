import scrapy

class WorldometersSpider(scrapy.Spider):
    name = "worldometers" # Name of the spider
    allowed_domains = ["www.worldometers.info"] # Restrict crawling to this domain
    start_urls = ["https://www.worldometers.info/world-population/population-by-country"] # Starting URL

    def parse(self, response):
        """
        Parse the main page to extract country names and links to their population data.
        """
        # Extract all country elements from the table
        countries = response.xpath('//td/a')

        for country in countries:
            # Extract the country name
            country_name = country.xpath('.//text()').get()
            # Extract the relative link to the country's population page
            link = country.xpath('.//@href').get()

            # Follow the link to the country's population page and pass the country name in the meta data
            yield response.follow(
                url=link,
                callback=self.parse_country,
                meta={'country': country_name} # Pass the country name to the next callback
            )

    def parse_country(self, response):
        """
        Parse the country-specific page to extract population data by year.
        """
        # Retrieve the country name from the meta data
        country = response.request.meta['country']
        # Extract all rows from the first table with the specified class
        rows = response.xpath('(//table[contains(@class, "table table-striped table-bordered table-hover table-condensed table-list")])[1]/tbody/tr')
        for row in rows:
            # Extract the year from the first column
            year = row.xpath('.//td[1]/text()').get()
            # Extract the population from the second column (inside a <strong> tag)
            population = row.xpath('.//td[2]/strong/text()').get()

            # Yield the extracted data as a dictionary
            yield {
                'country': country,
                'year': year,
                'population': population
            }
