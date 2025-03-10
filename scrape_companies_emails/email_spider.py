import scrapy
from scrapy.linkextractors import LinkExtractor
import re
from urllib.parse import urlparse, urlunparse

class EmailSpider(scrapy.Spider):
    name = 'email_spider'

    def __init__(self, start_urls, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Split the comma-separated start URLs into a list
        if isinstance(start_urls, str):
            self.start_urls = start_urls.split(',')
        else:
            self.start_urls = start_urls
        
        # Set to store already found emails
        self.found_emails = set()

    def parse(self, response):
        # Extract emails using regex
        email_domain = domain(response.url).replace('www.', '')
        email_pattern = rf'[\w\.-]+@{email_domain}'
        emails = re.findall(email_pattern, response.text)
        
        # Only yield emails that haven't been found yet
        for email in emails:
            if email not in self.found_emails:
                self.found_emails.add(email)
                yield { 'email': email }

        # Follow links only from the start pages (depth 0)
        if response.meta.get('depth', 0) == 0:
            le = LinkExtractor(
                # Avoid crawling external links e.g. youtube
                allow_domains = domain(response.url), 
                # Avoid duplicate crawling of already visited pages
                process_value=remove_fragment,
            )
            for link in le.extract_links(response):
                yield scrapy.Request(link.url, callback=self.parse)

def domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def remove_fragment(url):
    parsed = urlparse(url)
    return urlunparse(parsed._replace(fragment=''))