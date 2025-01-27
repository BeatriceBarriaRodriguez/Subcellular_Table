from selenium import webdriver
from bs4 import BeautifulSoup
import time

# Open the webpage using Safari
driver = webdriver.Safari()
url = "https://compartments.jensenlab.org/Entity?figures=subcell_cell_%%&knowledge=10&textmining=10&predictions=10&type1=9606&type2=-22&id1=ENSP00000263849"
driver.get(url)

# Wait for the page to load fully
time.sleep(5)  # Adjust time as necessary

# Parse the page source
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Locate the table rows containing predictions
predictions = []
table = soup.find('table')  # Find the first table if there are multiple

if table:
    rows = table.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 0:  # Ensure there is at least one cell
            prediction = cells[0].get_text(strip=True)  # Assuming predictions are in the first cell
            if prediction:
                predictions.append(prediction)

# Print the list of predictions
print("Predictions:")
for prediction in predictions:
    print(prediction)

# Close the browser
driver.quit()