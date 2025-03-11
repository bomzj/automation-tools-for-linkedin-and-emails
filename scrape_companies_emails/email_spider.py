from collections import defaultdict
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
        
        self.start_urls = ensure_urls_valid(self.start_urls)

        # Use default values that will be overridden by from_crawler()
        self.max_pages_per_domain = 50
        self.priority_url_keywords = []

        # Set to store already found emails
        self.found_emails = set()

         # Counter to track pages crawled per domain
        self.pages_crawled_per_domain = defaultdict(int)

    def parse(self, response):
        current_domain = domain(response.url)

        # Extract emails using regex
        email_domain = current_domain.replace('www.', '')
        email_pattern = rf'[\w\.-]+@{email_domain}'
        emails = re.findall(email_pattern, response.text)
        
        # Only yield emails that haven't been found yet
        for email in emails:
            if email not in self.found_emails:
                self.found_emails.add(email)
                yield { 'email': email }

        # Increment the counter for this domain
        self.pages_crawled_per_domain[current_domain] += 1

        # Follow links only if we haven't reached the max pages for this domain
        if self.pages_crawled_per_domain[current_domain] > self.max_pages_per_domain:
            return 
        
        # Follow links only from the start pages (depth 0)
        if response.meta.get('depth', 0) == 0:
            le = LinkExtractor(
                # Avoid crawling external links e.g. youtube
                allow_domains=[current_domain], 
                # Avoid duplicate crawling of already visited pages
                process_value=remove_fragment,
            )
            links = le.extract_links(response)
            
            # Prioritize links containing keywords
            prioritized_links = prioritize_links(links, self.priority_url_keywords)
            
            for link in prioritized_links:
                # Double-check we're not exceeding the limit
                if self.pages_crawled_per_domain[current_domain] < self.max_pages_per_domain:
                    yield scrapy.Request(link.url, callback=self.parse)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        # Set these attributes after the spider is created
        spider.max_pages_per_domain = crawler.settings.get('MAX_PAGES_PER_DOMAIN', 50)
        spider.priority_url_keywords = crawler.settings.get('PRIORITY_URL_KEYWORDS', [])
        return spider

def domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def remove_fragment(url):
    parsed = urlparse(url)
    return urlunparse(parsed._replace(fragment=''))

def ensure_urls_valid(urls):
    # Avoid missing scheme errors
    valid_urls = []
    for url in urls:
        if not url.startswith(("http://", "https://")):
            url = "https://" + url  # Assume HTTPS by default
        valid_urls.append(url)
    return valid_urls

def prioritize_links(links, priority_keywords):
    """Sort links based on highest priority keyword found
    
    1. Only checks for first matching keyword
    2. Priority is based on keyword position in priority_keywords list
    3. URLs without any keyword match have lowest priority
    """
    def priority_score(link):
        url = link.url.lower()
        
        # Check each keyword in order
        for index, keyword in enumerate(priority_keywords):
            if keyword.lower() in url:
                # Return index (position) in the keywords list
                # Lower index means higher priority
                return index
                
        # If no keywords match, return a value higher than any index
        return len(priority_keywords) + 1
    
    # Sort links by priority score (lower is better)
    return sorted(links, key=priority_score)