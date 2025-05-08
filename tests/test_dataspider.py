from dataspider.dataspider import DataSpider

def test_extract_table_data():
    full_url = "https://finviz.com/quote.ashx?t=AAPL&ty=c&p=d&b=1"
    table_class = "snapshot-table2"
    scraper = DataSpider(full_url)
    df = scraper.extract_table_data(table_class)
    assert df is not None
    assert not df.empty
    assert "Attribute" in df.columns
    assert "Value" in df.columns
