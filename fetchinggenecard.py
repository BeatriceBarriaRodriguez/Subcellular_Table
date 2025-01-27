import requests
from bs4 import BeautifulSoup

def scrape_genecard(gene_name):
    url = f"https://www.genecards.org/cgi-bin/carddisp.pl?gene={gene_name}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:87.0) Gecko/20100101 Firefox/87.0'
    }
    
    response = requests.get(url, headers=headers)
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        # Finding localization information
        localization_section = soup.find('div', class_='gc-locations')
        localization = localization_section.get_text(strip=True, separator=', ') if localization_section else "Localization not found"

        # Finding confidence information
        confidence_section = soup.find('div', class_='gc-confidence')
        confidence = confidence_section.get_text(strip=True, separator=', ') if confidence_section else "Confidence not found"

        return {
            'localization': localization,
            'confidence': confidence,
        }
    else:
        print("Error fetching the page.")
        return None

gene_info = scrape_genecard("ZC2HC1A")
print(gene_info)
