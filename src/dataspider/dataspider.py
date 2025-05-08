from typing import Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urlparse, parse_qs

class DataSpider:
    """
    A generic scraper for extracting data from any webpage with a specified table structure.
    """

    def __init__(self, full_url: str):
        """
        Initialize the scraper with the full URL.

        Args:
            full_url (str): The full URL of the webpage to scrape.
        """
        parsed_url = urlparse(full_url)
        self.base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        self.params = parse_qs(parsed_url.query)

    def extract_table_data(self, table_class: str) -> Optional[pd.DataFrame]:
        """
        Extracts data from a table with the specified class on the webpage.

        Args:
            table_class (str): The CSS class of the table to extract data from.

        Returns:
            Optional[pd.DataFrame]: A pandas DataFrame containing the extracted data,
                                    or None if the table could not be found or scraped.
        """
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "Cache-Control": "no-cache",  # Prevent caching
                "Pragma": "no-cache"         # HTTP 1.0 backward compatibility
            }
            response = requests.get(self.base_url, headers=headers, params=self.params, timeout=10)
            response.raise_for_status()

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the table containing the data
            data_table = soup.find("table", class_=table_class)
            if not data_table:
                print("No data table found on the page.")
                return None

            # Extract rows and convert them into key-value pairs
            table_data = []
            for row in data_table.find_all("tr"):
                cells = row.find_all("td")
                if len(cells) % 2 == 0:  # Ensure pairs of key-value
                    for i in range(0, len(cells), 2):
                        key = cells[i].get_text(strip=True)
                        value = cells[i + 1].get_text(strip=True)
                        table_data.append([key, value])

            # Convert the extracted data into a pandas DataFrame
            if table_data:
                df = pd.DataFrame(table_data, columns=["Attribute", "Value"])
                return df
            else:
                print("No data found in the table.")
                return None

        except requests.RequestException as e:
            print(f"Error fetching the URL: {e}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None