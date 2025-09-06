import selenium
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from amazoncaptcha import AmazonCaptcha

##### to keep the window opened use the following two commands  #####
options = webdriver.ChromeOptions()
options.add_experimental_option('detach',True)
#----------------------------------------------------------------#

def scrap(product_review, driver):
    for i in range(19):
        titles = driver.find_elements(By.XPATH,
                                            '//a[@class="a-link-normal s-line-clamp-2 s-link-style a-text-normal"]')

        for title in titles:
            new_url = title.get_attribute("href")
            new_driver = webdriver.Chrome(options=options, service=Service(path))
            new_driver.get(new_url)
            SolveCaptcha(new_driver)
            item_review = new_driver.find_elements(By.XPATH, '//div[@data-hook="review-collapsed"]//span')
            for review in item_review:
                revText = review.text
                product_review.append(revText)

            new_driver.quit()

        try:
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,
                                                                                      '//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-button-accessibility s-pagination-separator"]')))
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)
        except Exception as e:
            # print(f"Next button error: {e}")
            driver.quit()
            break

    return product_review

def SolveCaptcha(driver):
    try:
        if driver.find_element(By.XPATH,
                               '//p[@class="a-last"]').text == "Sorry, we just need to make sure you're not a robot. For best results, please make sure your browser is accepting cookies.":

            image_link = driver.find_element(By.XPATH, '//div[@class="a-row a-text-center"]//img').get_attribute('src')
            captcha = AmazonCaptcha.fromlink(image_link)
            captcha_value = AmazonCaptcha.solve(captcha)
            input_field = driver.find_element(By.XPATH, '//input[@id="captchacharacters"]')
            input_field.send_keys(captcha_value)
            button = driver.find_element(By.XPATH, '//button[@class="a-button-text"]')
            button.click()
            print("captcha cleared")

    except:
        print("captcha not found")

product_review = []
start = time.time()
url = "https://www.amazon.in"
path = r"C:\Program Files\chromedriver-win64\chromedriver.exe"
# add options to the Chrome
driver = webdriver.Chrome(options = options, service= Service(path))
driver.get(url)

################## Bypass Amazon Captcha #############################
SolveCaptcha(driver)

search_bar = driver.find_element(By.XPATH, '//input[@id="twotabsearchtextbox"]')
search_bar.send_keys("tv")
apply_search = driver.find_element(By.ID, 'nav-search-submit-button')
apply_search.click()
product_review = scrap(product_review,driver)

search_bar = driver.find_element(By.XPATH, '//input[@id="twotabsearchtextbox"]')
search_bar.clear()
search_bar.send_keys("laptops")
apply_search = driver.find_element(By.ID, 'nav-search-submit-button')
apply_search.click()
product_review = scrap(product_review,driver)

df = pd.DataFrame({"reviews": product_review})
print(df)

df.to_csv("amazon_reviews_2.csv", index=False)
end = time.time()
print(end-start)
