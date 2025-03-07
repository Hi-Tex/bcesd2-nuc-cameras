# Import Selenium items needed for automated Chrome interactions
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Import screeninfo to calculate the display size to adjust Chrome window
from screeninfo import get_monitors

# Import os package to get username/password from env file
import os
from dotenv import load_dotenv

# Get monitor size to determine Chrome window size
for m in get_monitors():

    if (m.is_primary):
        screen_width  = m.width
        screen_height = m.height
        break

# Add Selenium options
options = Options()

# Leave Chrome open after script completes
options.add_experimental_option("detach", True)

# Remove "Chrome is being controlled by automated test software" notification
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])

# Avoid caching issues by launcing window incogneto mode
options.add_argument("--incognito")

# Disable SSL validation since it's an internal URL
options.add_argument("--ignore-certificate-errors")

# Open Chrome in Full Screen
options.add_argument("--kiosk")

# Instantiate Chrome driver with options
driver = webdriver.Chrome(options=options)

# Get Unifi credentials from environment variable
load_dotenv(load_dotenv(".env"))
unifi_username = os.getenv("Unifi_Username")
unifi_password = os.getenv("Unifi_Password")

# Open the Unifi website
unifi_url = os.getenv("Unifi_URL")
driver.get(unifi_url)

# Add a wait to allow pages to finish loading before interacting
WebDriverWait(driver=driver, timeout=10).until(
    EC.element_to_be_clickable((By.NAME, "username"))
)


# Fill out logon form
username_field = driver.find_element(By.XPATH, "//input[@name='username']")
username_field.send_keys(unifi_username)

password_field = driver.find_element(By.XPATH, "//input[@name='password']")
password_field.send_keys(unifi_password)

submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
submit_button.click()
