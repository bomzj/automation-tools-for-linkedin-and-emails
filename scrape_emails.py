from scrapy.crawler import CrawlerProcess, Crawler
from scrapy import signals
import json, sys
from email_spider import EmailSpider, domain

def update_companies_with_emails(file_path, spider):
    # Load the original JSON file
    with open(file_path, 'r') as f:
        companies = json.load(f)
    
    # Create a dictionary to map domains to emails
    domain_to_emails = {}
    for email in spider.found_emails:
        # Extract domain from email
        email_domain = email.split('@')[1]
        
        if email_domain not in domain_to_emails:
            domain_to_emails[email_domain] = []
        domain_to_emails[email_domain].append(email)
    
    # Update each company with relevant emails
    for company in companies:
        if 'url' in company:
            company_domain = domain(company['url']).replace('www.', '')
            # Find emails for this domain
            company['emails'] = domain_to_emails.get(company_domain, [])
    
    # Save the updated JSON back to the file
    with open(file_path, 'w') as f:
        json.dump(companies, f, indent=2)
        
    print(f"Updated {file_path} with found emails")


## Settings

settings = {
    # Let's override some Scrapy settings for better performance
    "DEPTH_LIMIT": 1,  # Limit the depth of the crawl
    "DOWNLOAD_TIMEOUT": 10,  # Short timeout to fail fast
    "RETRY_TIMES": 1,  # Only retry once
    "REDIRECT_MAX_TIMES": 3,  # Limit redirect

    # Additional custom EmailScraper settings
    
    "MAX_PAGES_PER_DOMAIN": 50, # Maximum number of pages to crawl per domain
   
    "PRIORITY_URL_KEYWORDS": [  # Keywords that indicate a high priority URL to crawl first
        'career',
        'job',
        'work',
        'employment',
        'join',
        'opportunity',
        'recruiting',
        'apply',
        'opening',
        'position',
        'talent',
        'vacancy',
        'vacancies',
        'hiring',
        'work',
        'contact',
        'about',
        'connect',
        'team',
        'hiring',
        'hire'
    ]
}


## Main

# Collect start urls from companies input file
input_file = sys.argv[1] or 'companies.json'

with open(input_file, 'r') as f:
    data = json.load(f)
    start_urls = [item['url'] for item in data if 'url' in item]

if not start_urls:
    print("No URLs found in the input file")
    sys.exit(1)

print(f"Starting to crawl {len(start_urls)} URLs...")

process = CrawlerProcess(settings)
process.crawl(EmailSpider, start_urls=start_urls)
crawler: Crawler = list(process.crawlers)[0]
spider_closed = lambda spider: update_companies_with_emails(input_file, spider)
crawler.signals.connect(spider_closed, signal=signals.spider_closed)

process.start()  # the script will block here until the crawling is finished