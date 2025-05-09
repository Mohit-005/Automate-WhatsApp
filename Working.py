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
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import sys
import os
import re


# The `login_time`, `new_msg_time`, `send_msg_time`, `country_code`, and `action_time` variables are used to control the timing of various actions performed by the script.

# Config
login_time = 30
new_msg_time = 15
send_msg_time = 3
country_code = "91"
action_time = 2

# Chrome user data directory
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
if not os.path.exists(user_data_dir):
    os.makedirs(user_data_dir)

def clean_phone_number(number):
    """Clean phone number by removing any non-digit characters"""
    return re.sub(r'\D', '', number.strip())

def send_message(driver, wait, message):
    """Find the correct message box div and send the message reliably."""
    try:
        # Wait for the correct message box div
        message_box = wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR,
            'div[contenteditable="true"][aria-label="Type a message"][role="textbox"][tabindex="10"][data-tab="10"]'
        )))
        message_box.click()
        time.sleep(0.5)
        # Clear any existing text (Ctrl+A then Backspace)
        message_box.send_keys(Keys.CONTROL, 'a')
        message_box.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        # Send message in smaller chunks
        chunk_size = 50
        for i in range(0, len(message), chunk_size):
            chunk = message[i:i + chunk_size]
            message_box.send_keys(chunk)
            time.sleep(0.5)
        time.sleep(1)
        message_box.send_keys(Keys.ENTER)
        return True
    except Exception as e:
        print(f"Error sending message: {str(e)}")
        return False

# The `image_path` variable is used to specify the path to the image that you want to send.

# Give the path of the image
image_path = None  # Disabled image sending for now

try:
    print("Initializing Chrome WebDriver...")
    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument(f'--user-data-dir={user_data_dir}')
    chrome_options.add_argument('--profile-directory=Default')
    
    # Initialize the Chrome WebDriver with the new syntax
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Create wait object with longer timeout
    wait = WebDriverWait(driver, 30)
    
    # Read message from file
    try:
        with open('message.txt', 'r', encoding='utf-8') as file:
            msg = file.read()
        print("Message loaded successfully")
    except FileNotFoundError:
        print("Error: message.txt file not found!")
        sys.exit(1)
    
    # Open WhatsApp Web
    print("Opening WhatsApp Web...")
    driver.get('https://web.whatsapp.com')
    print("Waiting for WhatsApp to load...")
    
    # Wait for WhatsApp to load completely
    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-tab="3"]')))
        print("WhatsApp loaded successfully")
    except TimeoutException:
        print("Please scan the QR code if you haven't already...")
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-tab="3"]')))
        print("WhatsApp loaded successfully after QR scan")
    
    time.sleep(5)  # Additional wait after WhatsApp loads
    
    # Read and process phone numbers
    try:
        with open('numbers.txt', 'r') as file:
            numbers = file.readlines()
        print(f"Found {len(numbers)} phone numbers to process")
    except FileNotFoundError:
        print("Error: numbers.txt file not found!")
        driver.quit()
        sys.exit(1)
    
    for n in numbers:
        try:
            num = clean_phone_number(n)
            if not num:  # Skip empty lines
                continue
                
            print(f"\nProcessing number: {num}")
            
            # Format the URL properly
            link = f'https://web.whatsapp.com/send?phone={country_code}{num}'
            print(f"Opening chat URL: {link}")
            driver.get(link)
            
            # Wait for chat to load
            print("Waiting for chat to load...")
            try:
                wait.until(EC.presence_of_element_located((By.ID, "main")))
                print("Chat loaded successfully")
                time.sleep(2)  # Wait a bit after chat loads
                
                # Send message using the new reliable function
                print("Sending message...")
                if send_message(driver, wait, msg):
                    print(f"Message sent successfully to {num}")
                else:
                    print(f"Failed to send message to {num}")
                
                time.sleep(send_msg_time)  # Wait after sending
                
            except TimeoutException:
                print(f"Could not load chat for number {num}. The number might be invalid.")
                continue
            
        except Exception as e:
            print(f"Error processing number {num}: {str(e)}")
            continue
    
except KeyboardInterrupt:
    print("\nScript interrupted by user")
except Exception as e:
    print(f"An error occurred: {str(e)}")
finally:
    # Always quit the driver
    try:
        print("\nClosing browser...")
        driver.quit()
        print("Browser closed successfully")
    except:
        pass
