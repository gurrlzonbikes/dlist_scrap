# -*- coding: utf-8 -*-

# Scrapy settings for disqusScraper project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'disqusScraper'

SPIDER_MODULES = ['disqusScraper.spiders']
NEWSPIDER_MODULE = 'disqusScraper.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'disqusScraper (+http://www.yourdomain.com)'
DOWNLOAD_DELAY = 0.25
LOG_ENABLED = True
#DOWNLOAD_HANDLERS = {
#    's3': 'scrapy.core.downloader.handlers.s3.S3DownloadHandler'
#}

LOG_ENCODING = 'utf-8'
LOG_FILE = 'spider_log.txt'
#FEED_URI = "s3://crawler-piwik/feeds/%(name)s/%(time)s.json"
FEED_FORMAT = "json"


FEED_EXPORTERS_BASE = {
    'json': 'scrapy.contrib.exporter.JsonItemExporter',
    'jsonlines': 'scrapy.contrib.exporter.JsonLinesItemExporter',
    'csv': 'scrapy.contrib.exporter.CsvItemExporter',
    'xml': 'scrapy.contrib.exporter.XmlItemExporter',
    'marshal': 'scrapy.contrib.exporter.MarshalItemExporter',
}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawler_piwik (+http://www.yourdomain.com)'
EXTENSIONS = {
   'scrapy.telnet.TelnetConsole': None
}