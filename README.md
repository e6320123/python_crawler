# Automated-Job-Scraper-Pro

A robust web automation tool designed for professional market research and job opportunity analysis. Built with Python and Selenium.

## 🚀 Core Features
- **Stealth Execution**: Implemented Chrome DevTools Protocol (CDP) commands to bypass common WebDriver detection.
- **Dynamic Content Handling**: Utilizes Explicit Wait mechanisms to ensure stability on AJAX-heavy websites.
- **Data Persistence**: Supports automated data export to formatted text files (`.txt`) with timestamps.
- **Human-like Interaction**: Randomized delay intervals and scrolling behaviors to mimic human browsing.

## 🛠️ Tech Stack
- **Language**: Python 3.x
- **Automation**: Selenium WebDriver
- **Target Browser**: Microsoft Edge (Chromium-based)
- **Data Storage**: File System (TXT) / SQLite (Integration ready)

## 📋 How to Use
1. Install dependencies: `pip install selenium`
2. Configure `TARGET_URL` and `KEYWORDS` in `104_ job_crawler.py`.
3. Run the script: `python 104_ job_crawler.py`

## 🛡️ Anti-Bot Implementation
This project prioritizes stealth. By modifying `navigator.webdriver` property and injecting custom scripts, it achieves a high success rate in crawling protected job portals.
