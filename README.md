Reads xlsx with the following headings:
Protein.Group	Protein.Names	Genes	First.Protein.Description	log2FC
i.e. P58397	ATS12_HUMAN	ADAMTS12	A disintegrin and metalloproteinase with thrombospondin motifs 12	10

Install drivers:
/usr/bin/python3 -m pip install selenium  
/usr/bin/python3 -m pip install selenium webdriver-manager "urllib3<2"
/usr/bin/python3 -m pip install beautifulsoup4

uniprotandjensen.py = final file

localisationtest.py = initial file
  uses uniprot_query code, searches the UniProt, then searches the Subcellular Location on this page (uses regex)
  
uniprot_data_single_query_imp.txt
  example output after searching by uniprot number

fetchinggenecard.py
  trying to scrape genecard - couldn't
