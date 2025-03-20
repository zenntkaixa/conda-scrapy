# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import sqlite3

import pymongo
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

"""
Pipeline to store scraped items in a MongoDB database.
"""
class MongodbPipeline:
    collection_name = 'transcripts'

    """
    Open the MongoDB connection when the spider starts.
    """
    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb+srv://admin:adminPassword@cluster0.mojz3.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
        self.db = self.client['My_Database'] # Connect to the database

    """
    Close the MongoDB connection when the spider finishes.
    """
    def close_spider(self, spider):
        self.client.close()

    """
    Insert the item into the MongoDB collection.
    """
    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(item)
        return item

"""
Pipeline to store scraped items in an SQLite database.
"""
class SQLitePipeline:
    """
    Open the SQLite connection and create the table if it doesn't exist.
    """
    def open_spider(self, spider):
        self.connection = sqlite3.connect('transcripts.db') # Connect to the SQLite database
        self.c = self.connection.cursor()

        # Create the transcripts table if it doesn't exist
        try:
            self.c.execute('''
                CREATE TABLE transcripts(
                    title TEXT,
                    plot TEXT,
                    transcript TEXT,
                    url TEXT
                )
            ''')
            self.connection.commit()
        except sqlite3.OperationalError: # If the table already exists, skip creation
            pass

    """
    Close the SQLite connection when the spider finishes.
    """
    def close_spider(self, spider):
        self.connection.close()

    """
    Insert the item into the SQLite database.
    """
    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO transcripts (title, plot, transcript, url)
                VALUES (?,?,?,?)
        ''', (
            item.get('title'),
            item.get('plot'),
            item.get('transcript'),
            item.get('url')
        ))
        self.connection.commit() # Commit the transaction
        return item