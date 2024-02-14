# WhatsApp Automation with Selenium

# This code automates sending WhatsApp messages to a list of phone numbers using Selenium. It opens the WhatsApp web interface, loads the chat window for each number, and sends a predefined message and an image (if provided).

### Prerequisites

# - Python 3 or higher
# - Selenium
# - Chrome WebDriver
# - A WhatsApp account

# ### Installation

# 1. Install Python 3 or higher from the official website.
# 2. Install Selenium using `pip install selenium`.
# 3. Install Chrome WebDriver using `pip install webdriver-manager`.

# ### Usage

# 1. Create a file named `numbers.txt` and add the phone numbers you want to send messages to, one number per line.
# 2. Create a file named `message.txt` and add the message you want to send.
# 3. (Optional) If you want to send an image, specify the path to the image in the `image_path` variable.
# 4. Run the script using `python whatsapp_automation.py`.


# The code starts by importing the necessary libraries.

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# The `login_time`, `new_msg_time`, `send_msg_time`, `country_code`, and `action_time` variables are used to control the timing of various actions performed by the script.

# Config
login_time = 30
new_msg_time = 15
send_msg_time = 1
country_code = 91
action_time = 1

# The `image_path` variable is used to specify the path to the image that you want to send.

# Give the path of the image
image_path = 'D:\\pick.png'

# The `driver` variable is used to control the Chrome browser.

# Create driver
driver = webdriver.Chrome(ChromeDriverManager().install())

# The `wait` variable is used to wait for elements to load on the WhatsApp web interface.
wait = WebDriverWait(driver, 10)

# Encode Message Text
with open('message.txt', 'r') as file:
    msg = file.read()

# Open browser with default link
link = 'https://web.whatsapp.com'
driver.get(link)
time.sleep(login_time)

# Loop Through Numbers List
with open('numbers.txt', 'r') as file:
    for n in file.readlines():
        num = n.rstrip()
        link = f'https://web.whatsapp.com/send/?phone={country_code}{num}'
        driver.get(link)
        time.sleep(new_msg_time)

        # Click on button to load the input DOM
        if image_path:
            attach_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[title="Attach"]')))
            attach_btn.click()
            time.sleep(action_time)

            # Find and send image path to input
            input_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))
            input_box.send_keys(image_path)
            time.sleep(action_time)

        # Find and type message
        msg_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[contenteditable="true"]')))
        msg_input.send_keys(msg)
        msg_input.send_keys(Keys.ENTER)

        # Add a delay to keep the chat open for a while before moving to the next one
        time.sleep(send_msg_time)

# Quit the driver
driver.quit()
