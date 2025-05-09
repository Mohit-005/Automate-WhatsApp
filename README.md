# WhatsApp Automation Bot with Selenium

This project automates sending WhatsApp messages to a list of phone numbers using Python and Selenium. It is designed for reliability, ease of use, and persistent login sessions.

## Features

- **Automated WhatsApp Messaging:** Send messages to multiple numbers automatically.
- **Persistent Login:** Only scan the QR code once! The bot remembers your session using a custom Chrome profile.
- **Accurate Message Delivery:** Always types in the correct chat input box, never in the search bar.
- **Flexible Message and Number Files:** Easily change your message or recipients by editing `message.txt` and `numbers.txt`.
- **Error Handling:** Skips invalid numbers and provides clear feedback.
- **Chunked Message Sending:** Handles long messages by sending them in small chunks.

## Setup

### Prerequisites

- Python 3.x
- Google Chrome

### Install Dependencies

```
pip install selenium webdriver-manager
```

### Project Files

- `Working.py` — Main automation script
- `numbers.txt` — List of phone numbers (one per line, no country code needed)
- `message.txt` — The message to send

## Usage

1. **Add Phone Numbers:**
   - Put your recipients in `numbers.txt`, one per line (e.g., `9876543210`).
2. **Write Your Message:**
   - Put your message in `message.txt`.
3. **Run the Script:**
   ```
   python Working.py
   ```
4. **First Run:**
   - Scan the WhatsApp QR code in the Chrome window that opens.
   - Your session will be saved for future runs (no repeated QR scans).
5. **Watch the Bot Work:**
   - The script will open each chat and send your message.

## How Persistent Login Works

- The script uses a custom Chrome user profile directory (`chrome_profile`).
- This means you only need to scan the QR code once; your session is reused every time you run the script.
- **Important:** _Do not commit the `chrome_profile` directory to version control or share it. It contains sensitive session data. Each user should generate their own session by running the script and scanning the QR code on their own machine._

## How Accurate Message Delivery Works

- The script uses a very specific selector to find the chat message input box:
  ```python
  'div[contenteditable="true"][aria-label="Type a message"][role="textbox"][tabindex="10"][data-tab="10"]'
  ```
- This ensures the message is always typed in the correct place, not in the search bar.

## Troubleshooting

- **Script types in the search bar:**
  - Make sure you are using the latest version of the script with the updated selector.
- **Repeated QR code requests:**
  - Ensure the `chrome_profile` folder is being created and used.
- **Invalid numbers:**
  - The script will skip numbers that are not valid WhatsApp users.
- **Connection issues:**
  - Sometimes WhatsApp may block automated requests or close connections. Try again after a short wait.

## Customization

- **Change the message:** Edit `message.txt`.
- **Change recipients:** Edit `numbers.txt`.
- **Change country code:** Edit the `country_code` variable in `Working.py`.

## Disclaimer

This project is for educational purposes only. Use responsibly and respect WhatsApp's terms of service.

---

**Enjoy automating your WhatsApp messages!**

## Note

- I'm not responsible if your WhatsApp account will affect or blocked in any way for this code.
- Please do not use this code to spam or scam people.

## LICENSE

[MIT License](LICENSE)
