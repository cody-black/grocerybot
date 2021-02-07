from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from pynput import keyboard
import os
import re
import time

PROFILE_PATH = "/home/username/.mozilla/firefox/whatever-your-profile-is"

# Attempt to read from the grocery list and exit if it can't be found
try:
    grocery_list_file = open("list.txt", "r")
except FileNotFoundError:
    print('Error: Grocery list file "list.txt" not found, exiting')
    exit()

# Read in items and amounts from grocery list file
grocery_list = []
for line in grocery_list_file:
    amt = -1
    result = re.search(r"(.*)\sx(\d+)", line)
    if result is not None:
        item = result.group(1)
        amt = int(result.group(2))
    else:
        item = line.strip('\n')
        amt = 1
    grocery_list.append((item, amt))

# Attempt to load a profile so the user doesn't have to log in every time
try:
    driver = webdriver.Firefox(executable_path=os.getcwd() + "/geckodriver", firefox_profile=FirefoxProfile(PROFILE_PATH))
except:
    print("Error reading Firefox profile, continuing with temp profile")
    driver = webdriver.Firefox(executable_path=os.getcwd() + "/geckodriver")

# Open the website and wait for the user to make sure everything is correct
driver.get("https://www.walmart.com/grocery")
input("Press enter after you are signed in and have the correct store location selected")

while True:
    response = input("Choose mode:\n1. Auto mode: automatically adds the first search result to the cart.\n2. Assist mode: automatically searches for each item, but allows you to pick which result to add to the cart.\n")
    if response == "1":
        auto_mode = True
        break
    elif response == "2":
        auto_mode = False
        break
    else:
        print("Invalid choice, please try again.")

if auto_mode:
    for item, amt in grocery_list:
        # Wait for the page to load enough for the search bar
        search = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element_by_css_selector(".Search__searchField___3eXaL"))
        time.sleep(0.25)
        print('Searching for "{}"'.format(item.strip('\n')))
        # Search for current item from the list
        search.clear()
        search.send_keys(item + Keys.ENTER)
        try:
            # Wait for the page to load enough for the add to cart button
            xpath = "/html/body/div/div[1]/div/div/main/div[1]/table/tbody/tr/td[2]/div/div[1]/div/div[3]/div/div/button"
            cart_button = WebDriverWait(driver, timeout=3).until(lambda d: d.find_element_by_xpath(xpath))
            time.sleep(0.25)
            # Add first result to cart
            print('Adding {} of first result for "{}" to cart.'.format(amt, item.strip('\n')))
            cart_button.click()
            # Add multiple of the same item, if needed
            if (amt > 1):
                plus_button = driver.find_element_by_css_selector(".AddToCart__incrementBtn___21NpA")
                for _ in range(amt - 1):
                    # Wait a little bit to try to avoid bot detection
                    time.sleep(0.25)
                    plus_button.click()
        except TimeoutException:
            try:
                driver.find_element_by_css_selector(".NoResults__noResultsTitle___2aXqM")
                print("No results, moving to next item")
            except NoSuchElementException:
                print("Error: timed out, moving to next item")
else:
    for item, amt in grocery_list:
        # Wait for the page to load enough for the search bar
        search = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element_by_css_selector(".Search__searchField___3eXaL"))
        print('Searching for "{}". Press q anywhere to move to the next item.'.format(item.strip('\n')))
        # Search for current item from the list
        search.clear()
        search.send_keys(item + Keys.ENTER)
        # Waits until q is (pressed and) released
        while True:
            with keyboard.Events() as events:
                event = events.get()
                if format(event) == "Release(key='q')":
                    break

input("Press enter to exit")
driver.quit()
grocery_list_file.close()
