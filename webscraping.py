#Reference file includes the references that I have used to write this code
#webscraping.csv is the result when you run this code with scrape_product('ps5', 2)

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

from tqdm import tqdm

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options

options = Options()

#this option to prevent chrome closes automatically even when driver.quit() isn't used
options.add_experimental_option("detach", True)
options.add_experimental_option("excludeSwitches", ['enable-logging'])
options.add_argument("--incognito")
#ChromeDriverManager().install() so i dont have to download ChromeDriver and set up the path
driver = webdriver.Chrome(service=Service(
    ChromeDriverManager().install()), options=options)

driver.get('https://www.amazon.com/')
driver.implicitly_wait(5)
search_bar = driver.find_element(By.ID, 'twotabsearchtextbox')
search_bar.click()


def scrape_product(product, maxpages):

    search_bar.send_keys(product)
    search_bar.send_keys(Keys.RETURN)
    driver.implicitly_wait(5)

    product_name = []
    product_price = []
    product_ratings = []
    product_link = []

    condition = True
    page_number = 1
    while condition:

        if page_number <= maxpages:
            product_list = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
                By.XPATH, '//div[contains(@class, "s-result-item s-asin")]')))

            for i in tqdm(product_list):

                # Name
                name = i.find_element(
                    By.XPATH, './/span[contains(@class, "a-size-medium a-color-base a-text-normal")]')
                product_name.append(name.text)
                # Price
                whole_price = i.find_elements(
                    By.XPATH, './/span[contains(@class, "a-price-whole")]'
                )
                fraction_price = i.find_elements(
                    By.XPATH, './/span[contains(@class, "a-price-fraction")]'
                )
                if whole_price != [] and fraction_price != []:
                    total_price = '.'.join(
                        [whole_price[0].text, fraction_price[0].text])
                else:
                    total_price = 0
                product_price.append(total_price)

                # Review
                Review = i.find_elements(
                    By.XPATH, './/div[contains(@class, "a-row a-size-small")]/span'
                )
                if Review != []:
                    ratings = Review[0].get_attribute('aria-label')
                else:
                    ratings = 0
                    
                product_ratings.append(ratings)

                # Link

                link = i.find_element(
                    By.XPATH, './/a[contains(@class, "a-link-normal")]'
                ).get_attribute('href')

                product_link.append(link)

            next_button = driver.find_element(By.XPATH, "//*[text()='Next']")
            next_button.click()
            page_number += 1 #we are in while loop

        else:
            condition = False
            time.sleep(2)
            driver.quit()
#put everything we've got into a dictionary so we could convert it into a csv file
    pre = {'name of product': product_name,
           'price of product': product_price,
           'ratings of product': product_ratings,
           'link of product': product_link}

    final = pd.DataFrame(pre)
#change E:\python auto\webscraping.csv to directory where you want to export the csv
    final.to_csv('E:\python auto\webscraping.csv', index=False)


scrape_product('ps5', 2)

# print(product_name)
# print(product_price)
# print(product_ratings)
# print(product_link)

