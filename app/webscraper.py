import requests
from bs4 import BeautifulSoup
import numpy as np 
import pandas as pd

def scrape_and_store():
  # Code to scrape the website
  data = []
  for i in range(9):
      url = "https://researchops.web.illinois.edu/?page=" + str(i)
      response = requests.get(url)
      if response.status_code == 200:
          soup = BeautifulSoup(response.content, 'html.parser')  
          table_rows = soup.find_all('tr') 

          for row in table_rows:
              columns = row.find_all('td')
              row_data = [column.text.strip() for column in columns]
              if row_data:  
                  data.append(row_data)

  df = pd.DataFrame(data, columns=["Description", "Research Area", "Timing", "Deadline"]).fillna("Unknown")
  # Remove duplicates and rows with missing values
  df = df.drop_duplicates()
  return df