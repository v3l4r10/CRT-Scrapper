import argparse
import requests
from bs4 import BeautifulSoup

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Scrape and check domains from crt.sh")
parser.add_argument("--domain", "-d", required=True, help="Domain to search for")
parser.add_argument("-o", "--output", help="Save output to a file")
args = parser.parse_args()

# Construct the URL based on the provided domain
base_url = f"https://crt.sh/?q={args.domain}"

# Send an HTTP GET request
response = requests.get(base_url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <td> elements in the 6th column (index 5)
td_elements = soup.select('tr td:nth-of-type(6)')

# Extract all domains from the <td> elements
all_domains = []

for td in td_elements:
    # Find all <br> tags and replace them with newline characters
    td_text = str(td).replace('<br/>', '\n')
    
    # Parse the modified HTML using BeautifulSoup
    modified_td = BeautifulSoup(td_text, 'html.parser')
    
    # Extract domains from the modified HTML
    domain_list = [domain.strip() for domain in modified_td.stripped_strings]
    
    all_domains.extend(domain_list)

# Print or save the output based on the -o argument
if args.output:
    with open(args.output, "w") as file:
        for domain in all_domains:
            file.write(domain + "\n")
else:
    for domain in all_domains:
        print(domain)

