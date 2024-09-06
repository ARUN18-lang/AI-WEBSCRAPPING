import selenium.webdriver as webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chrome.remote_connection import ChromeRemoteConnection
from bs4 import BeautifulSoup
import time

SBR_WEBDRIVER = 'https://brd-customer-hl_2f7c269a-zone-ai_scrape:uiisdwxf6lby@brd.superproxy.io:9515'

def scrape_web(website):
    print('Launching chrome browser...')

    sbr_connection = ChromeRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        print('Connected: Navigating to {website}...')
        driver.get(website)
        print('Waiting captcha to solve...')
        solve_res = driver.execute('executeCdpCommand', {
            "cmd": 'Captcha.waitForSolve',
            "params": {'detectTimeout': 10000},
        })
        print('Captcha solve status', solve_res['value']['status'])
        print('Navigated Scraping page content...')
        html = driver.page_source
        return html

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""

def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()
    
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_doc_content(doc_content, max_length=6000):
    return [
        doc_content[i : i + max_length] for i in range(0, len(doc_content), max_length)
    ]

