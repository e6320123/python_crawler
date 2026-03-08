"""
Project: automated_job_collector
Description: A professional web scraper for market research using Selenium.
Author: [Your Name/U-Shu]
"""

import os
import time
import random
import ctypes
import winsound
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================= Configuration =================
TARGET_URL = "https://www.104.com.tw/jobs/search/?area=6001008000&jobcat=2007001000,2007002000&jobsource=joblist_search&keyword=Selenium+%E8%87%AA%E5%8B%95%E5%8C%96&mode=s&order=15&page=1"
KEYWORDS = ["QA", "自動化", "測試", "SDET", "Python", "AI"]
MAX_SEARCH = 3  # Target record count for detailed reconnaissance

# Random delay configurations for anti-bot measures
SCROLL_DELAY = (1, 5)
PAGE_LOAD_DELAY = (3, 8)
SCROLL_ITERATIONS = 1
# =================================================

def setup_driver():
    """Initialize Edge WebDriver with stealth configurations."""
    options = webdriver.EdgeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Edge(options=options)
    
    # Bypass WebDriver detection
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })
    return driver

def save_to_txt(data_list):
    """Export scraped data to a formatted text file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"job_report_{timestamp}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"--- Automated Job Collection Report ({datetime.now()}) ---\n")
        f.write(f"Total Records Captured: {len(data_list)}\n")
        f.write("-" * 50 + "\n\n")
        
        for i, (title, company, salary, address, url) in enumerate(data_list, 1):
            f.write(f"[{i}] {title}\n")
            f.write(f"    Company: {company}\n")
            f.write(f"    Salary:  {salary}\n")
            f.write(f"    Address: {address}\n")
            f.write(f"    Link:    {url}\n\n")
    
    print(f"\n[System] Report successfully exported to {filename}")

def main():
    driver = setup_driver()
    wait = WebDriverWait(driver, 10)
    scraped_results = []

    try:
        print("[Status] Navigating to target index...")
        driver.get(TARGET_URL)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.jb-link")))

        # Implement dynamic scrolling for lazy loading content
        for i in range(SCROLL_ITERATIONS):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(*SCROLL_DELAY))
            print(f"--- Completed scroll iteration {i+1}")

        # Extract qualified job links
        job_elements = driver.find_elements(By.CSS_SELECTOR, "a.jb-link")
        target_urls = [job.get_attribute("href") for job in job_elements 
        if any(kw.lower() in job.text.lower() for kw in KEYWORDS)]

        print(f"[Status] Identified {len(target_urls)} qualified links. Processing top {MAX_SEARCH}...")

        # Detailed data extraction
        for i, url in enumerate(target_urls[:MAX_SEARCH]):
            print(f"--- Scraping details ({i+1}/{MAX_SEARCH}): {url}")
            driver.get(url)
            
            try:
                wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
                time.sleep(random.uniform(*PAGE_LOAD_DELAY)) # Human-like dwell time

                job_title = driver.find_element(By.TAG_NAME, "h1").text.strip()
                company = "N/A" # Default placeholder
                
                # Dynamic parsing of information tables
                labels = driver.find_elements(By.CLASS_NAME, "job-description-table__label")
                datas = driver.find_elements(By.CLASS_NAME, "job-description-table__data")
                
                salary, address = "TBD", "TBD"
                for label, data in zip(labels, datas):
                    label_text = label.text.strip()
                    if "薪資" in label_text:
                        salary = data.text.strip().split('\n')[0]
                    elif "地點" in label_text:
                        address = data.text.strip().replace('地圖', '').strip()
                
                scraped_results.append((job_title, company, salary, address, url))
                print(f"    Successfully captured: {job_title}")
                
            except Exception as e:
                print(f"    [Error] Critical failure on detail page: {e}")

        # Finalize and export
        if scraped_results:
            save_to_txt(scraped_results)
            ctypes.windll.user32.MessageBoxW(0, f"Successfully processed {len(scraped_results)} records.", "Mission Accomplished", 0x40)

    finally:
        print("[Status] Terminating session and cleaning up...")
        driver.quit()

if __name__ == "__main__":
    main()
