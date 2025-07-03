from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os
import undetected_chromedriver as uc
import time
import random

IN_FOLDER_PATH = "./data_in"
OUT_FOLDER_PATH = "./data_out"
input_files = [f for f in os.listdir(IN_FOLDER_PATH) if os.path.isfile(os.path.join(IN_FOLDER_PATH, f))]

print(input_files)

driver = uc.Chrome()
driver.get("https://codex.flywire.ai/?dataset=fafb")

try:
    # Change the selector below to something that's ONLY present after login
    WebDriverWait(driver, timeout=500).until(
        EC.presence_of_element_located((By.ID, "filter_string"))  # Example element
    )
    print("Login successful!")
except:
    print("Timeout waiting for user to log in.")
for file_in in input_files:
    with open(os.path.join(IN_FOLDER_PATH, file_in), "r") as data:
        for line in data:
            time.sleep(random.randint(200, 500) / 1000)
            driver.get(f"https://codex.flywire.ai/app/cell_details?dataset=fafb&cell_names_or_id={line}")
            out_elem = driver.find_element(By.XPATH, "//*[@id=\"contentBody\"]/div[1]/div[1]/div[2]/table/tbody/tr[4]/td[2]/small")
            text = out_elem.text
            val = text.split(" ")[3]
            print(val)
            with open(os.path.join(OUT_FOLDER_PATH, file_in), "a") as res_file:
                res_file.write(line.replace(" ", "").replace("\t", "").replace("\n", "") + ',' + val + ",\n")

print("Finished fetching data!")
driver.quit()