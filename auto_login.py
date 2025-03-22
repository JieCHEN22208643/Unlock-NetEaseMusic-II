# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00C8A2726B0329A85E0FEE3083EAE82F4C0DFA7E3CD8C6C2F3662A47851369E2BB9E8E1F1968E45A03251EF4C7B9C5AA1D8E3E2C57CE8E99794D4D8C4509375031D569B88ED0049827F43317AACB66FEDE8B0F2056659F2786046E5D828BAAC128B93E539B7810512B677B17391B4F9A4115AA908B7ED4487E1AF7B574A2F3706CAF3FBC279284528874B736F1AB141E01EEAA1AA6EFEB25B7B7C0BD78920EF8E7C570D0059A054A7DB0F203660B9F8C80FF6E52337E95AF02CD78FCFFE75596F0CFA39A6ABB1449BC99FA894D414D4918568FB57678C77B32A56035E3B04664EBF6789E2025FFE2E1888FF4224D9DA283E3F64A2B7896FCEF37D78AC24062774EAD7BD86A291107DB2AA4647167FEE05B06216D063F58F1341E78AC83221DC606830C32233D0AACC193372D2462726D3CA956FCB2975CBC56FFA8186A33EC8CDBE1DD945656E1790A1F9BD2EAD14AEC17A249B11DD6BD9D247361BB493E73B4DF"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
