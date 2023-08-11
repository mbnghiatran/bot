from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time
import logging


from undetected_chromedriver       import Chrome
from selenium.webdriver.common.by  import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support    import expected_conditions as EC

import sys

# Get the command-line arguments
args = sys.argv

# Check if the email and password were provided
if len(args) < 5:
    logging.info("Please provide the following arguments:")
    logging.info("\n- email")
    logging.info("\n- password")
    logging.info("\n- profile path")
    logging.info("\n- chrome portable path")
    exit()

# Retrieve the email and password from the command-line arguments
email, password, profile_path, chrome_executable_path = args[1:5]

# Use the email and password in your script
logging.info("Logging in with email:", email, "and password:", password, "and profile path:", profile_path)

def login(driver, user_data):
    service_login_url = "https://accounts.google.com/ServiceLogin"
    interactive_login_url = "https://accounts.google.com/InteractiveLogin"
    my_account_url = "https://myaccount.google.com" #https://myaccount.google.com/?utm_source=sign_in_no_continue&pli=1
        
    try:  ## Didn't login before
        # input email
        email_input = driver.find_element(By.XPATH, "//input[@type='email']")
        email_input.send_keys(user_data['gmail']['username'])
        # click next
        next_button = driver.find_element(By.ID, "identifierNext")
    except: ## Have login before
        next_button = driver.find_element(By.XPATH, "//button")
    finally:
        next_button.click()
        # input password
        password_input = driver.find_element(By.NAME, "Passwd")
        password_input.send_keys(user_data['gmail']['password'])
        # Submit the login form
        submit_button = driver.find_element((By.ID, 'passwordNext'))
        submit_button.click()
        WebDriverWait(driver, 10).until(EC.url_contains(my_account_url))

try:
    # driver_path = ChromeDriverManager(version="111.0.5563.64").install()
    service_login_url = "https://accounts.google.com/ServiceLogin"
    interactive_login_url = "https://accounts.google.com/InteractiveLogin"
    my_account_url = "https://myaccount.google.com" #https://myaccount.google.com/?utm_source=sign_in_no_continue&pli=1

    # create a WebDriver object using the ChromeOptions object
    driver = Chrome(use_subprocess=True, user_data_dir=profile_path, executable_path=chrome_executable_path)
    
    # navigate to a website
    driver.get(service_login_url)
    waiting_time = 10 # 10 seconds

    # Check the current URL
    current_url = driver.current_url
    login_successful = False
    if my_account_url in current_url:
        login_successful = True
    else:
        try:
            login(driver, usr_data)
            login_successful = True
        except:
            login_successful = False

    # Return result
    if login_successful:
        logging.info("Login successful")
        print('true')
    else:
        logging.warning("Login failed")
        print('false')
    
    driver.quit()

except Exception as e:
    # handle the error
    logging.error(f"An error occurred: {e}")
    # driver.quit()
    print('false')

# finally:
#     # close the browser window
#     if 'driver' in locals():
#         driver.close()