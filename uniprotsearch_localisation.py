import subprocess
import pandas as pd
import re

def subcellularlocalisations(file_path):
    df = pd.read_excel(file_path)
    UniProt_Annotations = []
    GO_Annotations = []

    for index, uniprot_query in enumerate(df['Protein.Group']):
        command = f'curl -H "Accept: text/plain; format=flatfile" "https://rest.uniprot.org/uniprotkb/{uniprot_query}"'
        uniprot_response = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        uniprot_data = uniprot_response.stdout.decode()

        # UniProt Annotations
        location_match = re.search(r'CC\s+-!-\s+SUBCELLULAR LOCATION:(.*?)CC\s+-!-\s+ALTERNATIVE PRODUCTS:', 
                                   uniprot_data, 
                                   re.DOTALL)
        if location_match:
            localization_section = location_match.group(1).strip()
            localization_section = re.sub(r'CC\s+', '', localization_section)  # Remove 'CC' prefixes
        else:
            localization_section = 'N/A'
        UniProt_Annotations.append(localization_section)

        # GO annotations
        go_matches = re.findall(r'DR\s+GO;\s+(GO:\d+);\s+([CFP]):(.*?);\s+(\w+):(\w+)\.', uniprot_data)
        if go_matches:
            go_descriptions = [desc.strip() for _, _, desc, _, _ in go_matches] # Get only the descriptions
            go_annotations_text = "; ".join(go_descriptions)  # Join descriptions with a semicolon
        else:
            go_annotations_text = 'N/A'
        GO_Annotations.append(go_annotations_text)

    # Add new columns to the DataFrame
    df['UniProt_Annotations'] = UniProt_Annotations
    df['GO_Annotations'] = GO_Annotations

    df.to_excel('2875_subcellular_localisation_withannotations.xlsx', index=False)

if __name__ == "__main__":
    file_path = '2875_subcellular_localisation.xlsx'
    subcellularlocalisations(file_path)
