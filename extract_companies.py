import json
import re
import time
import random
import traceback
from playwright.sync_api import sync_playwright, Page
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def merge_query_params(url, params):
    parsed_url = urlparse(url)
    existing_params = parse_qs(parsed_url.query)
    merged_params = {**existing_params, **params}
    updated_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        urlencode(merged_params, doseq=True),  # doseq=True ensures that multiple values are properly encoded
        parsed_url.fragment
    ))
    return updated_url

def random_sleep(min, max):
    random_sleep_time = random.uniform(min, max)
    time.sleep(random_sleep_time)

def login(page, email, password):
    page.goto('https://www.linkedin.com/')
    page.type('#session_key', email)
    page.type('#session_password', password)
    random_sleep(6, 10)
    page.click('button[type=submit]')

def page_num(page):
    val = parse_qs(urlparse(page.url).query).get('page')
    return int(val[0]) if val else 1

def is_last_page(page: Page):
    try:
        # If there is no pagination then this is the last page
        page.locator('.artdeco-pagination').wait_for()
        return page.locator('[aria-label="Next"][disabled]').count() == 1
    except:
        print('Pagination not found. So this is probably the last page.')
        return True

def next_page(page: Page):
    updated_url = merge_query_params(page.url, { 'page': page_num(page) + 1 })
    page.goto(updated_url)

def parse_company_from_company_details_page(page: Page):
    try:
        company = {}
        company['linkedin_id'] = re.search(r'company/(\d+)', page.url).group(1)
        company['name'] = page.locator('[data-x--account--name]').text_content().strip()
        company['industry'] = page.locator('.account-top-card__account-info [data-anonymize="industry"]').text_content().strip()
        company['url'] = page.locator('[data-control-name="visit_company_website"]').get_attribute('href')
    except Exception as e:
        li_url = page.url.split('?')[0]
        print(f"Couldn't parse some attributes of the company on {li_url} page.")
        print(e)
    return company

def next_company(page: Page):
    while True:
        # 25 is the limit of search results per page
        for i in range(25):
            try:
                search_result = page.locator('.artdeco-list__item').nth(i)

                # Scroll down to current search result in order to trigger its loading
                search_result.evaluate("node => node.scrollIntoView({ behavior: 'smooth', block: 'start' })")

                # Wait until search result is fully loaded
                search_result.locator('[data-anonymize="company-name"]').wait_for()
            except:
                return None
            
            # Go to company details page
            random_sleep(6, 10)
            search_result.locator('[data-control-name="view_company_via_result_name"]').click()
            page.wait_for_url('**/sales/company/**')

            yield parse_company_from_company_details_page(page)
            
            # Return back to search results page
            random_sleep(6, 10) 
            page.go_back()

        if is_last_page(page): break
        else: next_page(page)


## Settings

linkedin_email = "your_linkedin_email",
linkedin_password = "your_linkedin_password",

# Linkedin Sales Navigator companies search results page URL
start_url = "https://www.linkedin.com/sales/search/company?query=(spellCorrectionEnabled%3Atrue%2Ckeywords%3Asitecore)"


## MAIN

with sync_playwright() as playwright:
    print('Launching Chrome browser...')
    browser = playwright.chromium.launch(headless = False, args= ['--start-maximized'], slow_mo = 50)
    page = browser.new_page(no_viewport = True)
    
    print('Logging in...')
    login(page, linkedin_email, linkedin_password)
    print('Successfully logged in!')
    
    # Check if manual verification is required and wait for user input
    if not re.search(r'feed', page.url):
        print('Waiting until manual verification is done...')

    page.wait_for_url("**/feed/**", timeout=0)

    # Go to search results page
    print('Navigating to search results page.')
    random_sleep(6, 10)
    page.goto(start_url)
    
    print('Start parsing companies...')
    
    try:
        companies = []

        for company in next_company(page):
            companies.append(company)
        
        print('Parsing finished sucessfully!')
    except Exception as e:
        print(f'An error occurred at page {page_num(page)}.')
        print(traceback.format_exc())
    finally:
        with open('companies.json', 'w') as output_file:
            json.dump(companies, output_file, indent=4)
        print(f'{len(companies)} companies were parsed and saved to "companies.json" file.')

    browser.close()