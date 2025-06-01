import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

COOKIE_NAME = "WorkstationJwtPartitioned"
COOKIE_VALUE = os.getenv("COOKIE_VALUE")
TARGET_URL = os.getenv("TARGET_URL")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=chrome_options)
driver.get(TARGET_URL)

cookie = {
    'name': COOKIE_NAME,
    'value': COOKIE_VALUE,
    'domain': ".cloudworkstations.dev",
    'path': '/',
    'secure': True,
}
driver.add_cookie(cookie)
driver.get(TARGET_URL)

print("✅ Keepalive শুরু হয়েছে...")

while True:
    driver.get(TARGET_URL)
    print("🔄 Refreshed:", time.ctime())
    time.sleep(300)
