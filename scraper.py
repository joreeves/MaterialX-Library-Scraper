# %%

import os
from tqdm import tqdm

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from utils import pause, download_wait

#%%

download_path = "D:\\Downloads\\"

assert os.path.exists(download_path), "Download path does not exist"

op = webdriver.ChromeOptions()
op.add_argument('--no-sandbox')
op.add_argument('--verbose')
op.add_argument("--disable-notifications")
op.add_experimental_option("prefs", {
  "download.default_directory": download_path,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True})
op.add_argument('--disable-gpu')
op.add_argument('--disable-software-rasterizer')
# op.add_argument('--headless')

# %%

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=op)
driver.get("https://matlib.gpuopen.com/main/materials/all")

wait = WebDriverWait(driver, 10)

wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "vue-recycle-scroller__item-view")))

pause()

# %%

"""
This website splits elements into a grid based on window size
"""

# Get each row
rows = driver.find_elements(By.CLASS_NAME, "vue-recycle-scroller__item-view")

# Get the y position of each row
ypos = []
for r in rows:
    style = r.get_attribute("style")

    # find the integer in the style attribute
    # this is the y position of the row
    y = int(style.split('transform: translateY(')[-1].split("px);")[0])
    ypos.append(abs(y))

# find the index of the smallest y position in the list
# this is the first row
first_row = ypos.index(min(ypos))

# %%

# Get the first element in the first row
first_ele = rows[first_row].find_element(By.XPATH, "./div/div[1]")

# Click on the first element
first_ele.click()

# Wait for the download window to appear
wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*[@id="app"]/div[3]/div')))

pause()

# %%

# Get the download window
download_window = driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div')

n_files  = int(driver.find_element(By.CLASS_NAME, 'v-chip__content').text)
pbar = tqdm(total=n_files)

scraping = True

while scraping:
    wait.until(EC.visibility_of_all_elements_located((By.XPATH, '//*/table/tbody')))

    # Get the download table
    download_table = download_window.find_element(By.XPATH, '//*/table/tbody')

    # Get all of the rows in the table
    # Each row is a different resolution
    table_ele = download_table.find_elements(By.XPATH, "./tr[*]")

    # Get the last element in the table
    # This is the highest resolution
    last_ele = table_ele[-1].find_element(By.XPATH, "./td[3]/i")
    last_ele.click()

    pbar.update(1)

    download_wait(download_path)

    pause(10)

    # Click on the next button
    try:
        download_window.find_element(By.CLASS_NAME, 'mdi-chevron-double-right').click()
    except:
        scraping = False

# %%
