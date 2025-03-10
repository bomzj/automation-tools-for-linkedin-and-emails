# Email Scraper

The Email Scraper extracts email addresses from company websites listed in companies.json and updates the file with the scraped emails. The companies.json file is initially created by the LinkedIn Company Extractor.

## Requirements

- Python 3.12
- [Scrapy](https://scrapy.org/)

## Installation

1. Install Scrapy:
   ```sh
   pip install scrapy
   ```

## Usage

To scrape emails for companies and update `companies.json`, run:

```sh
python scrape_emails_update_companies.py companies.json
```

This will scrape emails and update the existing company data accordingly.