from tabulate import tabulate  # Import tabulate for better table visualization
from dataspider.dataspider import DataSpider

if __name__ == "__main__":
    # Provide the full URL
    full_url = "https://finviz.com/quote.ashx?t=AAPL&ty=c&p=d&b=1"
    table_class = "snapshot-table2"

    scraper = DataSpider(full_url)
    df = scraper.extract_table_data(table_class)
    if df is not None:
        # Display the DataFrame as a table with borders
        print(tabulate(df, headers='keys', tablefmt='grid'))

        # Save the DataFrame to a CSV file
        csv_file = "scraped_data.csv"
        df.to_csv(csv_file, index=False)
        print(f"Data saved to {csv_file}")
    else:
        print("Failed to scrape data.")