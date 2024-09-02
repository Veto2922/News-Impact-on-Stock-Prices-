import streamlit as st
import pandas as pd
from models.web_scraping import StockNewsScraper

st.title("Stock News and Price Data")

tickers_input = st.text_input("Enter stock tickers separated by commas (e.g., DELL , AMZN , META , NVDA , AAPL, GOOGL:)")

if tickers_input:
    tickers = [ticker.strip().upper() for ticker in tickers_input.split(',')]
    
    # Instantiate the scraper object
    scraper = StockNewsScraper(tickers)
    
    # Fetch and clean news data
    df = scraper.get_news()
    df = scraper.clean_data(df)
    
    # Fetch stock data and merge with news
    stock_data = scraper.fetch_stock_data(df['Date'].min().strftime('%Y-%m-%d'), df['Date'].max().strftime('%Y-%m-%d'))
    final_df = scraper.merge_news_with_stock(df, stock_data)
    final_df.dropna(inplace=True)

    st.dataframe(final_df)
    
    # Allow user to download the final DataFrame
    file_name = st.text_input("Name your CSV file (without '.csv'):") + ".csv"
    csv = final_df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name=file_name,
        mime='text/csv',
    )
