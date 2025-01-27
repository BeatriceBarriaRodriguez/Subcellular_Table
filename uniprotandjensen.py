import subprocess
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def setup_driver():
    """Set up and return a headless Selenium WebDriver."""
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def jensennavigate(driver, uniprot_query):
    """Navigate to the JensenLab Search and extract ENSP number."""
    try:
        url = f"https://compartments.jensenlab.org/Search?query={uniprot_query}"
        driver.get(url)

        # Wait for the table to appear (up to 20 seconds)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.data'))
        )

        # Parse the page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        ensp_number = soup.find('td', {'class': 'identifier'}).find('a').text.strip()
        print(f"ENSP Number: {ensp_number}")
        return ensp_number
    except Exception as e:
        print(f"Error fetching ENSP number for {uniprot_query}: {e}")
        return None

def jensentable(driver, jensenNo):
    """Extract 'Predictions' table data from JensenLab."""
    try:
        url = f"https://compartments.jensenlab.org/Entity?figures=subcell_cell_%25%25&knowledge=10&textmining=10&predictions=10&type1=9606&type2=-22&id1={jensenNo}"
        driver.get(url)

        # Wait for the page to load and ensure tables are present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'table_title'))
        )

        # Parse with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Locate the 'Predictions' title and find the next table
        predictions_div = soup.find('div', class_='table_title', text='Knowledge')
        if predictions_div:
            predictions_table = predictions_div.find_next('table')

            if predictions_table:
                # Extract data from the table
                data = []
                rows = predictions_table.find_all('tr')
                
                # Skip the header row
                for row in rows[1:]:
                    columns = row.find_all('td')
                    if len(columns) >= 3:  # Ensure there are enough columns
                        name = columns[0].text.strip()
                        evidence = columns[1].text.strip()
                        confidence = columns[2].text.strip()
                        star = columns[3].text.strip()
                        data.append([name, evidence, confidence, star])

                # Return extracted data
                return data
        print("Predictions table not found.")
        return []
    except Exception as e:
        print(f"Error fetching Jensen table for {jensenNo}: {e}")
        return []

def subcellularlocalisations(file_path):
    """Main function to process subcellular localizations."""
    # Read input file
    df = pd.read_excel(file_path)

    # Initialize columns
    UniProt_Annotations = []
    GO_Annotations = []
    Jensentableoutputs = []

    # Set up WebDriver
    driver = setup_driver()

    for index, uniprot_query in enumerate(df['Protein.Group']):
        # Handle multiple UniProt IDs
        if ";" in uniprot_query:
            uniprot_query = uniprot_query.split(';')[0]

        # Fetch UniProt data
        command = f'curl -H "Accept: text/plain; format=flatfile" "https://rest.uniprot.org/uniprotkb/{uniprot_query}"'
        uniprot_response = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        uniprot_data = uniprot_response.stdout.decode()

        # Extract UniProt Annotations
        location_match = re.search(r'CC\s+-!-\s+SUBCELLULAR LOCATION:(.*?)CC\s+-!-\s+ALTERNATIVE PRODUCTS:', 
                                   uniprot_data, 
                                   re.DOTALL)
        if location_match:
            localization_section = location_match.group(1).strip()
            localization_section = re.sub(r'CC\s+', '', localization_section)  # Remove 'CC' prefixes
        else:
            localization_section = 'N/A'
        UniProt_Annotations.append(localization_section)

        # Extract GO Annotations
        go_matches = re.findall(r'DR\s+GO;\s+(GO:\d+);\s+([CFP]):(.*?);\s+(\w+):(\w+)\.', uniprot_data)
        if go_matches:
            go_descriptions = [desc.strip() for _, _, desc, _, _ in go_matches]  # Get only the descriptions
            go_annotations_text = "; ".join(go_descriptions)  # Join descriptions with a semicolon
        else:
            go_annotations_text = 'N/A'
        GO_Annotations.append(go_annotations_text)

        # JensenLab data extraction
        jensenNo = jensennavigate(driver, uniprot_query)
        if jensenNo:
            jensentableoutput = jensentable(driver, jensenNo)
            Jensentableoutputs.append(jensentableoutput)
        else:
            Jensentableoutputs.append([])

        print(f"Processed {uniprot_query}: {localization_section}, {go_annotations_text}")

    # Close the WebDriver
    driver.quit()

    # Add new columns to the DataFrame
    df['UniProt_Annotations'] = UniProt_Annotations
    df['GO_Annotations'] = GO_Annotations
    df['jensentableoutput'] = Jensentableoutputs

    # Save to Excel
    df.to_excel('2875_subcellular_localisation_withannotations.xlsx', index=False)
    print("Processing complete. Data saved.")

if __name__ == "__main__":
    file_path = '2875_subcellular_localisation.xlsx'
    subcellularlocalisations(file_path)
