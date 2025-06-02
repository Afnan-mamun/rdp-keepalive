import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# --- এনভায়রনমেন্ট ভেরিয়েবল থেকে প্রয়োজনীয় তথ্য ---
# এই মানগুলো Render.com এর সেটিংসে (Environment Variables) দিতে হবে
COOKIE_NAME = "WorkstationJwtPartitioned"
COOKIE_VALUE = os.getenv("COOKIE_VALUE")
TARGET_URL = os.getenv("TARGET_URL")
VNC_URL_PREFIX = "https://80-firebase-second" # VNC URL এর শুরুর অংশ

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
driver.refresh() # কুকি কার্যকর করার জন্য প্রথম রিফ্রেশ
print("✅ কুকি সেট করা হয়েছে, প্রথম পেজ রিলোড দেওয়া হলো...")

# ধাপ ২: main-target বাটনে ক্লিক করা এবং দ্বিতীয় পেজ লোড হওয়া পর্যন্ত অপেক্ষা
try:
    wait = WebDriverWait(driver, 20)
    button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "main-target")))
    button.click()
    print("🚀 আরডিপি চালু করা হলো (main-target বাটনে ক্লিক করা হয়েছে)")
    
    # দ্বিতীয় পেজ লোড হওয়া পর্যন্ত অপেক্ষা করা (studio.firebase.google.com/second-...)
    wait.until(EC.url_contains("/second-"))
    print("🌐 দ্বিতীয় পেজ লোড হয়েছে: " + driver.current_url)

    # এখন VNC পেজ লোড হওয়ার জন্য অপেক্ষা করা
    VNC_LOAD_TIMEOUT = 45 # VNC লোড হওয়ার জন্য সর্বোচ্চ অপেক্ষা (সেকেন্ডে)
    start_time = time.time()
    vnc_loaded = False
    while time.time() - start_time < VNC_LOAD_TIMEOUT:
        if driver.current_url.startswith(VNC_URL_PREFIX):
            try:
                # VNC ক্যানভাস এলিমেন্ট লোড হয়েছে কিনা তা চেক করা
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.TAG_NAME, "canvas"))
                )
                vnc_loaded = True
                break
            except:
                pass # ক্যানভাস এখনও লোড হয়নি, অপেক্ষা করুন
        time.sleep(1) # প্রতি সেকেন্ডে চেক করুন

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
        # 1. VNC ক্যানভাস এলিমেন্ট সনাক্ত করা
        vnc_canvas = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "canvas"))
        )
        print("🎨 VNC ক্যানভাস এলিমেন্ট পাওয়া গেছে।")

        actions = ActionChains(driver)

        # 2. ক্যানভাসের উপর মাউস নড়াচড়া সিমুলেট করা
        actions.move_to_element(vnc_canvas).perform()
        print("🖱️ কার্সর VNC ক্যানভাসের কেন্দ্রে নেওয়া হলো।")
        time.sleep(2)

        for _ in range(3): # 3টি ভিন্ন স্থানে ক্লিক করুন
            x_offset = int(vnc_canvas.size['width'] * (0.2 + 0.6 * (time.time() % 1)))
            y_offset = int(vnc_canvas.size['height'] * (0.2 + 0.6 * (time.time() % 1)))

            actions.move_to_element_with_offset(vnc_canvas, x_offset, y_offset).click().perform()
            print(f"🖱️ ক্যানভাসে ক্লিক করা হলো (অফসেট: {x_offset}, {y_offset})।")
            time.sleep(2)

        # 3. ব্রাউজারের মধ্যে স্ক্রল করা (যদি VNC পেজ স্ক্রলযোগ্য হয়)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print("⏬ পেজ নিচে স্ক্রল করা হলো।")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, 0);")
        print("⏫ পেজ উপরে স্ক্রল করা হলো।")

    except Exception as e:
        print(f"❌ VNC সেশন সক্রিয় রাখার কার্যকলাপ ব্যর্থ: {e}")

    finally:
        time.sleep(300) # ৫ মিনিট অপেক্ষা (আপনার প্রয়োজন অনুযায়ী পরিবর্তন করুন)
