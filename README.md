# Worldometers Scraper

A Scrapy spider to scrape population data by country from [Worldometers](https://www.worldometers.info).

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/zenntkaixa/conda-scrapy.git

2. Navigate to the project directory:
    ```bash
   cd worldometers-scraper
   
3. Create and activate a virtual environment:
    ```
   python -m venv .venv
    source .venv/bin/activate  # On macOS/Linux
    .venv\Scripts\activate     # On Windows
   ```
4. Install dependencies:
    ```bash
    pip install scrapy
    ```
5. Run the spider:
    ```bash
   scrapy crawl worldometers -o population_data.csv