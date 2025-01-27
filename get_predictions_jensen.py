from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd

# Initialize WebDriver
driver = webdriver.Chrome()

jensenNo = "ENSP00000255764"

# Open the URL
url = 'https://compartments.jensenlab.org/Entity?figures=subcell_cell_%25%25&knowledge=10&textmining=10&predictions=10&type1=9606&type2=-22&id1=' + jensenNo
driver.get(url)

# Wait for the page to load and ensure tables are present
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'table_title'))
)

# Get the page source
html = driver.page_source

# Parse with BeautifulSoup
soup = BeautifulSoup(html, 'html.parser')

# Locate the 'Predictions' title and find the next table
predictions_div = soup.find('div', class_='table_title', text='Knowledge')
if predictions_div:
    predictions_table = predictions_div.find_next('table')

    if predictions_table:
        # Extract data from the table
        data = []
        rows = predictions_table.find_all('tr')
        
        # Skip the header row (rows[1:])
        for row in rows[1:]:
            columns = row.find_all('td')
            print (columns)
            if len(columns) >= 4:  # Ensure there are enough columns
                name = columns[0].text.strip()
                source = columns[1].text.strip()
                evidence = columns[2].text.strip()
                confidence = columns[3].text.strip()
                data.append([name, source, evidence, confidence])

        # Create a DataFrame
        df = pd.DataFrame(data, columns=['Name', 'Source', 'Evidence', 'Confidence'])
        print(df)
    else:
        print("Predictions table not found.")
else:
    print("'Predictions' title not found.")

# Close WebDriver
driver.quit()
