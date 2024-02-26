
# Extract Companies from Linkedin Sales Navigator

The Linkedin Companies Extractor is an automation tool that enables you to scrape(parse) and extract company data from Linkedin Sales Navigator. This tool is designed to simplify the process of gathering company information for various purposes such as market research, lead generation, and competitor analysis.

## Installation

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

## How to use

 1. Rename `config.json.example` to `config.json` and configure your Linkedin credentials with predefined Sales Navigator url that will be treated as start url (page 1) for search results
    
  2. Run the companies extractor script:
    
    	   python extract_companies.py

    

