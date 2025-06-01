import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

COOKIE_NAME = "WorkstationJwtPartitioned"
COOKIE_VALUE = os.getenv("COOKIE_VALUE")
TARGET_URL = os.getenv("TARGET_URL")

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)
driver.get(TARGET_URL)

# Add cookie manually
cookie = {
    'name': COOKIE_NAME,
    'value': COOKIE_VALUE,
    'domain': ".google.com",
    'path': '/',
    'secure': True,
}
driver.add_cookie(cookie)
driver.refresh()

print("✅ কুকি সেট করা হয়েছে, পেজ রিলোড দেওয়া হলো...")

# অপেক্ষা করবো বাটন লোড হওয়া পর্যন্ত
try:
    wait = WebDriverWait(driver, 20)
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "main-target")))
    button.click()
    print("🚀 আরডিপি চালু করা হলো (main-target বাটনে ক্লিক করা হয়েছে)")
except Exception as e:
    print("❌ বাটন খুঁজে পাওয়া যায়নি:", e)

# ৫ মিনিট পর পর পেজ রিফ্রেশ হবে
while True:
    time.sleep(300)
    driver.refresh()
    print("🔄 রিফ্রেশ:", time.ctime())
