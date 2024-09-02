import pandas as pd
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import re
import yfinance as yf

class StockNewsScraper:
    def __init__(self, tickers):
        self.tickers = tickers

    def get_news(self):
        finviz_url = 'https://finviz.com/quote.ashx?t='
        news_tables = {}
        parsed_data = []

        for ticker in self.tickers:
            url = finviz_url + ticker
            req = Request(url, headers={'user-agent': 'google'})
            response = urlopen(req)
            html = BeautifulSoup(response, 'html.parser')
            news_table = html.find('table', {'id': 'news-table'})
            news_tables[ticker] = news_table

        for ticker, news_table in news_tables.items():
            for rows in news_table.findAll('tr'):
                title = rows.a.text.strip()
                date_time_data = rows.td.text.strip().split(' ')
                if len(date_time_data) == 1:
                    time = date_time_data[0]
                else:
                    date = date_time_data[0]
                    time = date_time_data[1]
                parsed_data.append([ticker, date, time, title])

        df = pd.DataFrame(parsed_data, columns=['Ticker', 'Date', 'Time', 'Headline'])
        return df

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df['Headline'] = df['Headline'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s]', '', x.lower()))

        # Let Pandas infer the date format and handle errors by converting invalid dates to NaT
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Drop rows with NaT in 'Date' column
        df.dropna(subset=['Date'], inplace=True)

        return df

    def fetch_stock_data(self, start_date: str, end_date: str) -> pd.DataFrame:
        all_data = pd.DataFrame()
        for ticker in self.tickers:
            stock = yf.Ticker(ticker)
            stock_data = stock.history(start=start_date, end=end_date)
            stock_data['Ticker'] = ticker
            stock_data.reset_index(inplace=True)
            all_data = pd.concat([all_data, stock_data[['Date', 'Ticker', 'Close']]], ignore_index=True)
        return all_data

    def merge_news_with_stock(self, news_df: pd.DataFrame, stock_df: pd.DataFrame) -> pd.DataFrame:
        news_df['Date'] = pd.to_datetime(news_df['Date'])
        stock_df['Date'] = pd.to_datetime(stock_df['Date'])
        stock_df['Date'] = stock_df['Date'].dt.tz_localize(None)

        grouped_news_df = news_df.groupby(['Ticker', 'Date'])['Headline'].apply(lambda x: ' , '.join(x)).reset_index()
        merged_df = pd.merge(grouped_news_df, stock_df, how='left', on=['Date', 'Ticker'])

        stock_df_shifted = stock_df.copy()
        stock_df_shifted['Date'] = stock_df_shifted['Date'] + pd.Timedelta(days=1)

        merged_df = pd.merge(merged_df, stock_df_shifted[['Date', 'Ticker', 'Close']],
                             how='left', on=['Date', 'Ticker'], suffixes=('', '_prev_day'))

        merged_df['Price_Change'] = merged_df['Close'] - merged_df['Close_prev_day']
        merged_df['Label'] = merged_df['Price_Change'].apply(lambda x: 1 if x > 0 else -1)
        merged_df.drop(columns=['Close_prev_day'], inplace=True)

        return merged_df
