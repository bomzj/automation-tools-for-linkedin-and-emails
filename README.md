# Linkedin Lead Miner

This repository contains a collection of automation tools designed to streamline various tasks related to Linkedin and email management. Each tool serves a specific purpose and can be used individually or in combination with others.

## 1. Extract Companies(Leads) from Linkedin Sales Navigator

The Linkedin Company Extractor is an automation tool that allows users to scrape and extract company data from Linkedin Sales Navigator. This tool simplifies the process of gathering company information for purposes such as market research, lead generation, and competitor analysis.

### Setup

To use the Linkedin Companies Extractor, follow these steps:

1. Ensure you have Python 3.12 installed. If not, download and install it from the [official Python website](https://www.python.org/).
   
2. Install the Playwright Pytest plugin:

    ```bash
    pip install pytest-playwright
    ```
3. Install the required browsers for Playwright:
		
    ```bash
    playwright install
    ```

### How to use

 1. In `Settings` section of `extract_companies.py` configure your Linkedin login credentials and Sales Navigator start url(search results page 1) 
    
2. Run the companies extractor script:
    
    	   python extract_companies.py

3. `companies.json` will be created with all scraped linkedin companies


## 2. Scrape emails from companies websites

The Email Scraper extracts email addresses for companies and updates the `companies.json` file (initially created by the LinkedIn Company Extractor) with this data.

### Setup

1. Install Scrapy:
   ```sh
   pip install scrapy
   ```

### How to use

1. In `Settings` section of `scrape_emails.py` configure your settings.

2. To scrape emails for all companies listed in `companies.json`, run:

```sh
python scrape_emails.py
```

This will scrape emails and append to `companies.json`.


## 3. Cold mail companies with Gmail

Send mails to companies listed in `companies.json` with Gmail API by using personal gmail account.

### Setup

#### Setup Gmail API
  
1. Create a Google Cloud project https://developers.google.com/workspace/guides/create-project#project

2. Enable Gmail API for this project https://developers.google.com/gmail/api/quickstart/python#enable_the_api

3. Configure the OAuth consent screen https://developers.google.com/gmail/api/quickstart/python#configure_the_oauth_consent_screen

4. Authorize credentials for a desktop application https://developers.google.com/gmail/api/quickstart/python#authorize_credentials_for_a_desktop_application

5. Install the Google client library https://developers.google.com/gmail/api/quickstart/python#install_the_google_client_library


### How to use

1. In `Settings` section of `send_emails.py` update email template and most relevant email keywords as needed.

2. To start cold mailing, run:

```sh
python send_emails.py
```

This will send emails to companies at 3-minute intervals to comply with Gmail's sending policy.