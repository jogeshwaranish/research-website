import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_and_store():
    # Initialize a list to store the data
    data = []
    
    # Loop through the pages
    for i in range(9):
        url = "https://researchops.web.illinois.edu/?page=" + str(i)
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            table_rows = soup.find_all('tr')
            
            # Extract data from each row
            for row in table_rows:
                columns = row.find_all('td')
                row_data = [column.text.strip() for column in columns]
                
                # Extract the hyperlink, if available
                link_tag = row.find('a')  # Find the first <a> tag in the row
                link = link_tag['href'] if link_tag and 'href' in link_tag.attrs else "No Link"
                
                if row_data:  # If the row contains data
                    row_data.append(link)  # Add the link to the row data
                    data.append(row_data)
    
    # Create a DataFrame and include the link as a new column
    df = pd.DataFrame(data, columns=["Description", "Research Area", "Timing", "Deadline", "Link"]).fillna("Unknown")
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    return df
