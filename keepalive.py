import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# --- অ্যাকাউন্ট-নির্দিষ্ট তথ্য সরাসরি এখানে সেট করা হয়েছে ---
# **সতর্কতা: এটি নিরাপত্তার জন্য ঝুঁকি তৈরি করে।**
# **আপনার কুকি ভ্যালু এখানে সরাসরি উন্মুক্ত থাকবে।**
COOKIE_NAME = "WorkstationJwtPartitioned"
COOKIE_VALUE = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2Nsb3VkLmdvb2dsZS5jb2xvd29ya3N0YXRpb25zIiwiYXVkIjoiZmlyZWJhc2Utc2Vjb25kLTE3NDg3MjAyNjAyNDIuY2x1c3Rlci1lamQyMmtxbnk1aHR1djVkZm93b3lpcHQ1Mi5jbG91ZHdvcmtzdGF0aW9ucy5kZXYiLCJpYXQiOjE3NDg4NDIxMTYsImV4cCI6MTc0ODkyODUxNn0.JRuXciKCv63b8Jm_XTmhqhkLN_JCVw1pIEoLdn81tXiGTU6Tld_XoTrC4OkB7KMl_rX3IoevRy9A1TB2Xsrf-yTbK9AACzibBhprfjjkTLFMJlEd4sCjA_mPAFYVvxfpkL0G3mgW5jcOriMor89w_yqTcV7L7BQY7WeWjdhnNcc5Ys2Kzv4UKOcHURLW_UIPky9j6QJ9FGqGNEyq9u3jbeCtL0O29Yn2r1yZoP8ha_L2bejhj5aFuRjO96jVFtooB0P5F3-_9blZG5wXiy7T4SE73io7JFQ_YTO8Lv9lOVfgnMNQEu9hbgRksY1UA3yPaaFwh09_pj4B-H6SIDT-WA"
TARGET_URL = "https://studio.firebase.google.com/?utm_source=firebase_studio_marketing&utm_medium=et&utm_campaign=FY25-Q2-firebasestudio_nextlaunch&utm_content=hero_tryfirebasestudio&utm_term=-&pli=1"
VNC_URL_PREFIX = "https://80-firebase-second" # VNC URL এর শুরুর অংশ (এটি সম্ভবত একই থাকবে)

# --- Selenium সেটআপ ---
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")

driver = webdriver.Chrome(options=chrome_options)

# ধাপ ১: প্রথম URL-এ যাওয়া এবং কুকি যোগ করা
driver.get(TARGET_URL)
cookie = {
    'name': COOKIE_NAME,
    'value': COOKIE_VALUE,
    'domain': ".google.com",
    'path': '/',
    'secure': True,
}
driver.add_cookie(cookie)
driver.refresh()
print("✅ কুকি সেট করা হয়েছে, প্রথম পেজ রিলোড দেওয়া হলো...")

# ধাপ ২: main-target বাটনে ক্লিক করা এবং দ্বিতীয় পেজ লোড হওয়া পর্যন্ত অপেক্ষা
try:
    wait = WebDriverWait(driver, 20)
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "main-target")))
    button.click()
    print("🚀 আরডিপি চালু করা হলো (main-target বাটনে ক্লিক করা হয়েছে)")
    
    # দ্বিতীয় পেজ লোড হওয়া পর্যন্ত অপেক্ষা করা
    wait.until(EC.url_contains("/second-"))
    print("🌐 দ্বিতীয় পেজ লোড হয়েছে: " + driver.current_url)

    # এখন VNC পেজ লোড হওয়ার জন্য অপেক্ষা করা
    VNC_LOAD_TIMEOUT = 45
    start_time = time.time()
    vnc_loaded = False
    while time.time() - start_time < VNC_LOAD_TIMEOUT:
        if driver.current_url.startswith(VNC_URL_PREFIX):
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "canvas"))
                )
                vnc_loaded = True
                break
            except:
                pass
        time.sleep(1)

    if vnc_loaded:
        print("✅ VNC রিমোট উবুন্টু সিস্টেম লোড হয়েছে: " + driver.current_url)
    else:
        print("❌ VNC পেজ লোড হতে ব্যর্থ বা ক্যানভাস পাওয়া যায়নি। বর্তমান URL: " + driver.current_url)
        driver.quit()
        exit()

except Exception as e:
    print(f"❌ প্রাথমিক ধাপ সম্পন্ন করা যায়নি: {e}")
    driver.quit()
    exit()

# --- VNC পেজে সক্রিয় থাকার জন্য লুপ ---
while True:
    try:
        vnc_canvas = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
        print("🎨 VNC ক্যানভাস এলিমেন্ট পাওয়া গেছে।")

        actions = ActionChains(driver)

        actions.move_to_element(vnc_canvas).perform()
        print("🖱️ কার্সর VNC ক্যানভাসের কেন্দ্রে নেওয়া হলো।")
        time.sleep(2)

        for _ in range(3):
            x_offset = int(vnc_canvas.size['width'] * (0.2 + 0.6 * (time.time() % 1)))
            y_offset = int(vnc_canvas.size['height'] * (0.2 + 0.6 * (time.time() % 1)))

            actions.move_to_element_with_offset(vnc_canvas, x_offset, y_offset).click().perform()
            print(f"🖱️ ক্যানভাসে ক্লিক করা হলো (অফসেট: {x_offset}, {y_offset})।")
            time.sleep(2)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("⏬ পেজ নিচে স্ক্রল করা হলো।")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        print("⏫ পেজ উপরে স্ক্রল করা হলো।")

    except Exception as e:
        print(f"❌ VNC সেশন সক্রিয় রাখার কার্যকলাপ ব্যর্থ: {e}")

    finally:
        time.sleep(300)