import subprocess
import pandas as pd
import re

def fastafromgene(file_path):
    # File containing gene names to read through
    df = pd.read_excel(file_path)

    # fasta_seqs = []
    # uni_id = []
    localizations = []  # New list to store localization data

    for index, uniprot_query in enumerate(df['Protein.Group']):
        uniprot_query = "Q5FYB0"
        # Query Uniprot for subcellular location data
        command = f'curl -H "Accept: text/plain; format=flatfile" "https://rest.uniprot.org/uniprotkb/{uniprot_query}"'
        uniprot_response = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        uniprot_data = uniprot_response.stdout.decode()

        with open('/Users/barriab/Desktop/uniprot_data_single_query_imp.txt', 'w') as output_file:
                output_file.write(f"UniProt Entry for {uniprot_query}:\n")
                output_file.write(uniprot_data)
        
        
        # Use regex to capture lines between "SUBCELLULAR LOCATION" and "ALTERNATIVE PRODUCTS"
        location_match = re.search(r'CC\s+-!-\s+SUBCELLULAR LOCATION:(.*?)CC\s+-!-\s+ALTERNATIVE PRODUCTS:', 
                                   uniprot_data, 
                                   re.DOTALL)

        if location_match:
            # Clean and save the matched localization section
            localization_section = location_match.group(1).strip()
            localization_section = re.sub(r'CC\s+', '', localization_section)  # Remove 'CC' prefixes from each line
        else:
            localization_section = 'N/A'

        # Append the extracted localization information
        localizations.append(localization_section)

    # Add the new 'localization' column to the DataFrame
    df['localization'] = localizations
    # Save the modified DataFrame back to the Excel file
    df.to_excel('/Users/barriab/Desktop/2875_subcellular_localisation_final.xlsx', index=False)


if __name__ == "__main__":
    file_path = '/Users/barriab/Desktop/2875_subcellular_localisation.xlsx'
    fastafromgene(file_path)