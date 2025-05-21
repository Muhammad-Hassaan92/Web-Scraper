import setuptools, sys
sys.modules['distutils'] = setuptools._distutils
sys.modules['distutils.version'] = setuptools._distutils.version

import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

def scrape_website(url):
    print("Launching stealth Chrome...")

    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-infobars")
    options.add_argument("--start-maximized")

    driver = uc.Chrome(options=options)

    try:
        driver.get(url)
        print(f"Loaded {url}...")
        time.sleep(2)
        html = driver.page_source
        return html
    finally:
        print("Closing Chrome...")
        driver.quit()

def extract_body_content(html):
    soup = BeautifulSoup(html, 'html.parser')
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

def split_dom_content(dom_content, max_length=1000000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
