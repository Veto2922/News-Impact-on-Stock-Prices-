# Analyzing News Impact on Stock Prices and Sentiment Classification

## Project Overview

This project explores the impact of news sentiment on stock prices through a comprehensive analysis of news headlines and historical stock data. It involves data collection, preprocessing, sentiment analysis, exploratory data analysis (EDA), and the development and evaluation of various machine learning and deep learning models.

For more info please visit the [Project Medium Article](https://medium.com/@abdelrahman.m2922/analyzing-news-impact-on-stock-prices-and-sentiment-classification-19b29d5fc670

## Table of Contents

1. [Web Scraping](#web-scraping)
2. [Stock Price Data Collection](#stock-price-data-collection)
3. [Text Preprocessing](#text-preprocessing)
4. [Sentiment Analysis and EDA](#sentiment-analysis-and-eda)
5. [Modeling](#modeling)

## Web Scraping

### Why Finviz?

Finviz was selected as the data source due to its comprehensive market data, including news headlines for various stock tickers. Its structured news table layout facilitates efficient data extraction.

### Data Collection

The `get_news` function scrapes recent news headlines for a list of stock tickers from Finviz. It performs the following steps:
1. Constructs the URL
2. Sends a request
3. Parses HTML content
4. Extracts data
5. Stores data in a DataFrame

```python
def get_news(tickers: list):
    # Function code
```

### Data Cleaning

The `clean_data` function preprocesses the scraped news data:
1. Removes special characters
2. Standardizes dates

```python
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Function code
```

### Results

The cleaned data includes columns for Ticker, Date, Time, and Headline. The data is saved to a CSV file for further analysis.

## Stock Price Data Collection

### Fetching Historical Stock Prices

The `fetch_stock_data` function retrieves historical stock prices using the yfinance library.

### Merging News with Stock Prices

The `merge_news_with_stock` function integrates news headlines with stock prices:
1. Converts dates
2. Groups news data
3. Merges DataFrames
4. Calculates price change
5. Assigns labels based on price change

### Results

The final DataFrame includes columns for Ticker, Date, Headline, Close, Price_Change, and Label. Some rows may have missing values due to weekends and holidays without stock prices.

## Text Preprocessing

The text preprocessing phase prepares the data for analysis and modeling:
1. Lowercasing
2. Removing punctuation and special characters
3. Tokenization
4. Removing stopwords
5. Lemmatization

## Sentiment Analysis and EDA

### Why VADER?

VADER (Valence Aware Dictionary and Sentiment Reasoner) is effective for analyzing short texts like news headlines due to its dictionary-based approach and ability to detect sentiment nuances.

### Sentiment Calculation

The `calculate_average_sentiment` function computes the average sentiment score for combined headlines.

### EDA

1. **Scatter Plot of Sentiment vs. Price Change**: No significant effect of sentiment on stock prices.
2. **Correlation Heatmap**: Very weak correlation between sentiment scores and price changes.
3. **Sentiment and Price Change Plots for Specific Tickers**: Varied impact across different companies (e.g., DELL, GOOGL, NFLX, ORCL, BABA).

### Final Insights

- No clear overall relationship between news sentiment and stock prices.
- Stronger correlation observed for companies with direct consumer interactions (e.g., Netflix, Google).

## Modeling

### Preprocessing

- Columns: Processed_Headline, Sentiment, Close, Price_Change, Label
- Train-Test Split: 80–20
- TFIDF Vectorization

### Models

1. **Baseline Model**: Logistic Regression
2. **Traditional Machine Learning Models**:
   - Naive Bayes
   - SVM
   - Random Forest
   - K-Nearest Neighbors (KNN)

   Random Forest was selected for hyperparameter tuning due to its balanced performance.

3. **Deep Learning Models**:
   - **Recurrent Neural Network (RNN)**: Limited performance due to small dataset size.
   - **DistilRoBERTa**: Transformer-based model fine-tuned for sentiment analysis.

### Results

- **Random Forest**: Balanced performance across metrics.
- **DistilRoBERTa**: Outperformed traditional models in recall and F1-score.
- **RNN**: Underperformed due to limited dataset size.

### Conclusion

- **Random Forest**: Recommended for general use due to balanced performance.
- **DistilRoBERTa**: Suitable for tasks requiring nuanced understanding of text.
- **RNN**: Limited by dataset size.

## Future Work

- Explore advanced sentiment analysis techniques using transformer models for improved accuracy.

## Installation

To run the code, clone the repository and install the required packages:

```bash
git clone https://github.com/Veto2922/News-Impact-on-Stock-Prices-.git
cd <repository-directory>
pip install -r requirements.txt
```

## Usage

Run the Streamlit application to interact with the data:

```bash
streamlit run app.py
```

```
