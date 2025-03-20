# Worldometers Scraper

A Scrapy spider to scrape population data by country from [Worldometers](https://www.worldometers.info).

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/zenntkaixa/conda-scrapy.git

2. Navigate to the project directory:
    ```bash
   cd spider_tutorial
   
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
5. Run the spider (for worldometers):
    ```bash
   scrapy crawl worldometers -O population_data.csv
   
# Scrapy Spider for Movie Transcripts

This Scrapy project is designed to scrape movie transcripts from [subslikescript.com](https://subslikescript.com) and store the data in either an **SQLite** or **MongoDB** database. The spider crawls through movie listings, extracts transcript details, and saves them for further analysis.

---

## Features
- **CrawlSpider**: Automatically follows pagination links and extracts movie details.
- **SQLite Pipeline**: Stores scraped data in an SQLite database.
- **MongoDB Pipeline**: Stores scraped data in a MongoDB database.
- **Custom Settings**: Configurable settings for download delay, pipelines, and more.

---

## Prerequisites
Before running the spider, ensure you have the following installed:
- **Python 3.8+**
- **Scrapy**: Install via `pip install scrapy`.
- **SQLite3**: Usually comes pre-installed with Python.
- **MongoDB** (optional, for MongoDB pipeline): Install MongoDB locally or use a cloud-based service like MongoDB Atlas.
- **PyMongo** (optional, for MongoDB pipeline): Install via `pip install pymongo`.

---

## Project Structure
spider_tutorial/
├── spider_tutorial/
│ ├── spiders/
│ │ └── transcripts_spider.py # Spider script
│ ├── pipelines.py # Pipelines for SQLite and MongoDB
│ ├── settings.py # Scrapy settings
│ └── init.py
├── scrapy.cfg # Scrapy configuration file
└── README.md # This file


---

## Setup Instructions

### 1. Clone the Repository
Clone this repository to your local machine:
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Set Up the Environment
Create a virtual environment and install the required dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install scrapy pymongo
```

3. Configure the Database
SQLite
No additional setup is required. The SQLite database (transcripts.db) will be created automatically when the spider runs.

MongoDB (Optional)
Set up a MongoDB database (local or cloud-based).

Update the MongoDB connection string in pipelines.py:

```python
self.client = pymongo.MongoClient('mongodb+srv://admin:adminPassword@cluster0.mojz3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
self.db = self.client['My_Database']
```
Replace the connection string with your MongoDB credentials.

----------------------------------------------------------------
### Running the Spider
1. Run with SQLite Pipeline (Default)
To run the spider and store data in the SQLite database:

```bash
scrapy crawl transcripts
The scraped data will be saved in transcripts.db. You can view it using a SQLite browser or the command line:
```
```bash
sqlite3 transcripts.db
sqlite> SELECT * FROM transcripts;
```

2. Run with MongoDB Pipeline (Optional)
To enable the MongoDB pipeline, update settings.py:
```python
ITEM_PIPELINES = {
    "spider_tutorial.pipelines.MongodbPipeline": 300,
}
```

Then run the spider:
```bash
scrapy crawl transcripts
```

The scraped data will be stored in the transcripts collection of the My_Database database. Use a MongoDB client (e.g., MongoDB Compass) to view the data.

### Custom Settings
You can customize the spider's behavior by modifying settings.py. For example:

Download Delay: Adjust DOWNLOAD_DELAY to control the delay between requests.

Pipelines: Enable or disable pipelines by updating ITEM_PIPELINES.

Example:

```python
ITEM_PIPELINES = {
    "spider_tutorial.pipelines.SQLitePipeline": 300,  # Enable SQLite pipeline
    "spider_tutorial.pipelines.MongodbPipeline": 301,  # Enable MongoDB pipeline
}
```
Example Output
The scraped data will include the following fields:
- title: Movie title
- plot: Movie plot
- transcript: Full transcript
- url: URL of the transcript page

Example:

```json
{
    "title": "Inception",
    "plot": "A thief who steals corporate secrets through the use of dream-sharing technology...",
    "transcript": "Cobb: You mustn't be afraid to dream a little bigger, darling...",
    "url": "https://subslikescript.com/movie/Inception"
}
```
### Troubleshooting
**Common Issues**
1. Database Connection Issues:
   - Ensure the database (SQLite or MongoDB) is properly configured and accessible.
   - For MongoDB, verify the connection string and credentials.

2. Scraping Errors:
   - Check the logs for any errors and adjust the XPath selectors if necessary.
   - Ensure the website structure hasn't changed.

3. Rate Limiting:
   - If the website blocks your requests, increase the DOWNLOAD_DELAY in settings.py.

### Contributing
Contributions are welcome! If you find any issues or have suggestions for improvements, please:

1. Open an issue on GitHub.
2. Fork the repository and submit a pull request.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Acknowledgments
Scrapy for providing a powerful web scraping framework.

subslikescript.com for the movie transcript data.