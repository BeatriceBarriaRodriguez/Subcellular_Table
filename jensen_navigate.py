from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def jensennavigate(uniprot_query):
    # Setup WebDriver
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    # Navigate to the URL
    url = 'https://compartments.jensenlab.org/Search?query={uniprot_query}'
    driver.get(url)

    # Wait for the table to appear (up to 20 seconds)
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'table.data'))
    )

    # Get the page source after the table is loaded
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Locate the ENSP number inside the 'identifier' class
    ensp_number = soup.find('td', {'class': 'identifier'}).find('a').text.strip()

    print(f"ENSP Number: {ensp_number}")

    # Close the driver
    driver.quit()

if __name__ == "__main__":
    file_path = '2875_subcellular_localisation.xlsx'
    subcellularlocalisations(file_path)
