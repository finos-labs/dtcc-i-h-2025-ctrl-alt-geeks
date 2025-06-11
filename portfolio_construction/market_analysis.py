import os
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta
import yfinance as yf # <-- Import yfinance
import pandas as pd

# Load API keys from the .env file
load_dotenv()

class MarketResearchAgent:
    def __init__(self):
        # We no longer need Alpha Vantage for sectors, but keep it for other potential tools
        self.alpha_vantage_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        self.fred_key = os.getenv("FRED_API_KEY")
        self.news_api_key = os.getenv("NEWS_API_KEY")

    # --- REVISED Tool 1: Get Sector Performance via ETFs ---
    def _get_sector_performance(self):
        """
        Calculates recent performance of the 11 GICS sectors by tracking their main ETFs.
        This is the new, reliable method.
        """
        print("Fetching sector performance via ETFs...")
        SECTOR_ETFS = {
            'Information Technology': 'XLK',
            'Health Care': 'XLV',
            'Financials': 'XLF',
            'Communication Services': 'XLC',
            'Consumer Discretionary': 'XLY',
            'Consumer Staples': 'XLP',
            'Industrials': 'XLI',
            'Utilities': 'XLU',
            'Real Estate': 'XLRE',
            'Materials': 'XLB',
            'Energy': 'XLE'
        }
        
        try:
            # We will calculate performance over the last month (approx 22 trading days)
            # yfinance is very flexible here, we'll use '1mo' period
            tickers = list(SECTOR_ETFS.values())
            data = yf.download(tickers, period="1mo", progress=False)['Adj Close']

            if data.empty:
                print("Warning: yfinance returned no data for sector ETFs.")
                return {}, {}

            # Calculate percentage change from the first day to the last
            performance = ((data.iloc[-1] / data.iloc[0]) - 1) * 100
            
            # Map the performance back to sector names
            sector_performance = {
                sector: performance[ticker] for sector, ticker in SECTOR_ETFS.items()
            }
            
            # Sort the sectors by performance
            sorted_sectors = sorted(sector_performance.items(), key=lambda item: item[1], reverse=True)
            
            top_performing = {s: f"{p:.2f}%" for s, p in sorted_sectors[:3]}
            underperforming = {s: f"{p:.2f}%" for s, p in sorted_sectors[-3:]}
            
            return top_performing, underperforming
        except Exception as e:
            print(f"Error fetching sector performance via yfinance: {e}")
            return {}, {}

    # --- Other tools remain the same as they use reliable APIs ---
    def _get_interest_rate_trend(self):
        """Fetches the Federal Funds Rate to determine interest rate trend."""
        # ... (This function remains unchanged)
        try:
            url = f"https://api.stlouisfed.org/fred/series/observations?series_id=FEDFUNDS&api_key={self.fred_key}&file_type=json&limit=2&sort_order=desc"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()['observations']
            latest = float(data[0]['value']); previous = float(data[1]['value'])
            if latest > previous: return "Rising"
            if latest < previous: return "Falling"
            return "Holding Steady"
        except Exception as e:
            print(f"Error fetching interest rate data: {e}")
            return "Unknown"

    def _get_market_news_sentiment(self):
        """Fetches recent financial news to gauge market sentiment."""
        # ... (This function remains unchanged)
        try:
            yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
            url = (f"https://newsapi.org/v2/everything?q=market+economy+inflation+stocks"
                   f"&from={yesterday}&language=en"
                   f"&sources=bloomberg,the-wall-street-journal,reuters"
                   f"&apiKey={self.news_api_key}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            articles = response.json().get('articles', []); score = 0
            positive = ['optimism', 'growth', 'rally', 'upbeat', 'strong', 'gains']
            negative = ['fear', 'recession', 'downturn', 'volatile', 'slump', 'losses', 'crisis']
            for article in articles[:15]:
                title = article.get('title', '').lower()
                score += sum(1 for word in positive if word in title)
                score -= sum(1 for word in negative if word in title)
            if score > 2: return "Positive"
            if score < -2: return "Negative"
            return "Neutral"
        except Exception as e:
            print(f"Error fetching market news: {e}")
            return "Unknown"

    # --- Main Agentic Function ---
    def run(self):
        """Executes all tools and synthesizes the findings into a structured 'Market Conditions Brief'."""
        print("MarketResearchAgent: Starting analysis...")
        
        top_sectors, bottom_sectors = self._get_sector_performance()
        interest_trend = self._get_interest_rate_trend()
        news_sentiment = self._get_market_news_sentiment()
        
        outlook = "Neutral"
        if news_sentiment == "Positive" and interest_trend != "Rising":
            outlook = "Bullish"
        elif news_sentiment == "Negative" or interest_trend == "Rising":
            outlook = "Bearish"
        
        print("MarketResearchAgent: Analysis complete.")

        market_brief = {
            "timestamp": datetime.now().isoformat(),
            "marketOutlook": outlook,
            "interestRateTrend": interest_trend,
            "marketSentiment": news_sentiment,
            "topPerformingSectors_1mo": top_sectors,
            "underperformingSectors_1mo": bottom_sectors,
            "summary": (
                f"The general market outlook is {outlook.lower()}, driven by a {news_sentiment.lower()} news sentiment "
                f"and interest rates that are {interest_trend.lower()}. "
                f"Over the past month, top performing sectors include {', '.join(top_sectors.keys())}."
            )
        }
        return market_brief

if __name__ == "__main__":
    agent = MarketResearchAgent()
    brief = agent.run()
    
    import json
    print("\n--- Market Conditions Brief ---")
    print(json.dumps(brief, indent=2))

    # Save the brief to a JSON file
    with open("market_conditions_brief.json", "w", encoding="utf-8") as f:
        json.dump(brief, f, indent=2)