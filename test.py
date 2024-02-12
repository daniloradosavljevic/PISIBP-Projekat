from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://google.com")

WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.NAME, "q"))
)

input_element = driver.find_element(By.NAME, "q")
input_element.clear()
input_element.send_keys("pewdiepie" + Keys.ENTER)

WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "PewDiePie"))
)

link = driver.find_element(By.PARTIAL_LINK_TEXT, "PewDiePie")
link.click()

time.sleep(5)

driver.quit()