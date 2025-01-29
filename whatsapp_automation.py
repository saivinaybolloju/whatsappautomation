
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pywhatkit as kit

# Initialize the ChromeDriver using Service and ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://web.whatsapp.com/')

# Wait for WhatsApp Web to load
time.sleep(15)  # Adjust this delay as needed to ensure WhatsApp Web is fully loaded

# Define targets (both saved contacts and unsaved phone numbers)
target_contacts = ['Naveen Clg Intern Batch','Tarun RPA','Madhav RPA']
target_unsaved_numbers =["+917093144791","+917989719032"]  # Ensure numbers are in international format with country code
MSG = "HELLO MAWA IDI AUTOMATED MESSAGE"

wait = WebDriverWait(driver, 30)
actions = ActionChains(driver)

# Function to send message to a saved contact
def send_message_to_contact(target_name):
    try:
        # Locate the search box and enter the contact name
        search_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))

        # Click and clear multiple times to ensure it's focused
        for _ in range(3):
            search_box.click()
            search_box.clear()
            time.sleep(1)  # Small delay to ensure the element is ready

        # Use ActionChains to send keys
        actions.move_to_element(search_box).click().send_keys(target_name).perform()
        time.sleep(2)  # Wait for search results to appear

        # Select the contact from search results
        contact_xpath = f'//span[@title="{target_name}"]'
        contact_element = wait.until(EC.element_to_be_clickable((By.XPATH, contact_xpath)))
        contact_element.click()
        
        # Locate the input box and send the message
        input_box = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
        input_box.send_keys(MSG + " "+ Keys.ENTER)
        time.sleep(1)
    
    except TimeoutException:
        print(f"Target '{target_name}' not found or not clickable. Skipping to next target.")
    except ElementClickInterceptedException:
        print(f"Target '{target_name}' was intercepted. Skipping to next target.")
    except WebDriverException as e:
        print(f"WebDriverException occurred: {str(e)}. Skipping to next target.")

# Function to send message to an unsaved number
def send_message_to_unsaved_number(target_number, message):
    try:
        # Send message to an unsaved number using pywhatkit
        kit.sendwhatmsg_instantly(target_number, message, 15, True, 5)
        print(f"Message sent to {target_number}")
    except Exception as e:
        print(f"An error occurred while sending message to {target_number}: {str(e)}")

# Send messages to saved contacts
for contact in target_contacts:
    send_message_to_contact(contact)
    time.sleep(1)  # Wait a bit to avoid issues with multiple messages

# Send messages to unsaved numbers
for number in target_unsaved_numbers:
    send_message_to_unsaved_number(number, MSG)
    time.sleep(1)  # Wait a bit to avoid issues with multiple messages

driver.quit()








































import sqlite3
import os

# Check if the database file exists
db_file = 'whatsapp_contacts.db'
new_db_created = not os.path.exists(db_file)

# Connect to the database (it will create the file if it doesn't exist)
conn = sqlite3.connect(db_file)
c = conn.cursor()

# Drop the contacts table if it exists
c.execute('DROP TABLE IF EXISTS contacts')

# Create a new contacts table
c.execute('''
    CREATE TABLE contacts (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        message TEXT NOT NULL
    )
''')

# Insert sample data
contacts = [
    ('SHIVA CSD B ACE', 'Hello Mowa, how are you?'),
    ('Varun RPA', 'Hello Varun, how are you?'),
    ('Maa', 'Hi Maa, sending automated message.'),
    ('Ajay', 'Hi AJJI, sending automated message.'),
    ('Potti Vikas CSD ACE', 'Hello Vikas, how are you?'),
    ('Karan Anna', 'Hello Anna, how are you?'),
    # Add more contacts and messages as needed
]

c.executemany('INSERT INTO contacts (name, message) VALUES (?, ?)', contacts)

# Commit the transaction and close the connection
conn.commit()
conn.close()

# Print status message
if new_db_created:
    print("A new database has been created, the contacts table has been dropped, recreated, and sample data has been inserted.")
else:
    print("The existing database has been modified, the contacts table has been dropped, recreated, and sample data has been inserted.")


















import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

# Helper function to convert characters to surrogate pairs
def to_surrogate_pair(unicode_str):
    result = []
    for char in unicode_str:
        if ord(char) > 0xFFFF:
            char = ord(char) - 0x10000
            result.append(chr((char >> 10) + 0xD800))
            result.append(chr((char & 0x3FF) + 0xDC00))
        else:
            result.append(char)
    return ''.join(result)

# Connect to the SQLite database
conn = sqlite3.connect('whatsapp_contacts.db')
c = conn.cursor()

# Fetch contacts and messages from the database
c.execute('SELECT name, message FROM contacts')
rows = c.fetchall()

conn.close()

# Initialize the ChromeDriver using Service and ChromeDriverManager
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get('https://web.whatsapp.com/')

# Wait for WhatsApp Web to load
time.sleep(10)  # Adjust this delay as needed to ensure WhatsApp Web is fully loaded

# Process each contact and send the message
for row in rows:
    target_name = to_surrogate_pair(row[0])
    MSG = to_surrogate_pair(row[1])

    try:
        print(f"Processing contact: {target_name}")

        # Find the search bar
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        
        # Clear any existing text in the search bar
        search_box.clear()
        for _ in range(50):
            search_box.send_keys(Keys.BACKSPACE)

        time.sleep(2)
        search_box.send_keys(target_name)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)

        # Wait for the contact to be visible and click it
        target_element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{target_name}"]'))
        )

        for attempt in range(5):
            try:
                target_element.click()
                break
            except ElementClickInterceptedException:
                if attempt < 4:
                    time.sleep(3)  # Wait before retrying
                else:
                    raise

        # Find the message input box and send the message
        input_box = WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        input_box.send_keys(MSG + Keys.ENTER)
        time.sleep(3)
        print(f"Message sent to: {target_name}")

    except TimeoutException:
        print(f"Target '{target_name}' not found. Skipping to next target.")
        continue
    except WebDriverException as e:
        print(f"WebDriverException for target '{target_name}': {e}")
        continue

driver.quit()




















import pywhatkit
from datetime import datetime

now = datetime.now()

chour = now.strftime("%H")
mobile = input('Enter Mobile No of Receiver : ')
message = input('Enter Message you wanna send : ')
hour = int(input('Enter hour : '))
minute = int(input('Enter minute : '))

pywhatkit.sendwhatmsg(mobile,message,hour,minute)
