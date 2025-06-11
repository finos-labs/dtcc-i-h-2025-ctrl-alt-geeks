import pandas as pd
import numpy as np
import yfinance as yf
import quantstats as qs  # <-- Import quantstats
from datetime import datetime, timedelta

class PortfolioAnalysisAgent:
    def __init__(self, portfolio: dict, investment_horizon_years=10, initial_capital=100000):
        """
        Initializes the agent with a portfolio.
        :param portfolio: A dictionary from the construction agent, e.g., {"holdings": [{"ticker": "VTI", "percentage": 0.6}]}
        :param investment_horizon_years: The number of years for backtesting and simulation.
        :param initial_capital: The starting capital for Monte Carlo simulation.
        """
        # --- MODIFIED: Handle the new portfolio structure ---
        # The input is the full dictionary from the previous agent
        self.portfolio_input = portfolio
        
        # We create a simple ticker:weight dictionary for internal use
        self.portfolio_weights_dict = {
            item['ticker']: item['percentage'] for item in self.portfolio_input.get('holdings', [])
        }
        
        if not self.portfolio_weights_dict:
            raise ValueError("Portfolio holdings are empty or malformed.")

        if not np.isclose(sum(self.portfolio_weights_dict.values()), 1.0):
            raise ValueError("Portfolio weights must sum to 1.0")
            
        self.tickers = list(self.portfolio_weights_dict.keys())
        self.weights = np.array(list(self.portfolio_weights_dict.values()))
        self.horizon_years = investment_horizon_years
        self.initial_capital = initial_capital
        self.historical_data = None

    # --- Tool 1: Data Fetching (Unchanged) ---
    def _fetch_historical_data(self):
        """Fetches historical close prices using yfinance."""
        print("Fetching historical data...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.horizon_years * 365)
        try:
            # Using 'Close' is the modern standard for yfinance
            data = yf.download(self.tickers, start=start_date, end=end_date)['Close']
            self.historical_data = data.dropna()
            print("Data fetched successfully.")
        except Exception as e:
            print(f"Error fetching data: {e}")
            self.historical_data = pd.DataFrame()

    # --- REVISED Tool 2: Backtesting & Risk Metric Calculation with quantstats ---
    def _calculate_performance_metrics(self):
        """Calculates key risk and return metrics using quantstats."""
        if self.historical_data.empty: return {}
        print("Calculating performance metrics...")
        
        asset_returns = self.historical_data.pct_change().dropna()
        portfolio_returns = asset_returns.dot(self.weights)
        
        # quantstats functions return floats directly, not Series, which is convenient.
        # We assume a risk-free rate of 0 for simplicity.
        sharpe = qs.stats.sharpe(portfolio_returns, rf=0)
        sortino = qs.stats.sortino(portfolio_returns, rf=0)
        # quantstats max_drawdown is positive. We make it negative to match financial conventions.
        max_drawdown = qs.stats.max_drawdown(portfolio_returns) * -1
        cagr = qs.stats.cagr(portfolio_returns)
        volatility = qs.stats.volatility(portfolio_returns, annualize=True)

        return {
            "cagr": f"{cagr:.2%}",
            "max_drawdown": f"{max_drawdown:.2%}",
            "sharpe_ratio": f"{sharpe:.2f}",
            "sortino_ratio": f"{sortino:.2f}",
            "annual_volatility": f"{volatility:.2%}"
        }

    # --- Tool 3: Monte Carlo Simulation (Unchanged) ---
    def _run_monte_carlo_simulation(self, num_simulations=1000):
        """Runs a Monte Carlo simulation to forecast potential future outcomes."""
        if self.historical_data.empty: return {}
        print("Running Monte Carlo simulation...")
        
        asset_returns = self.historical_data.pct_change().dropna()
        portfolio_returns = asset_returns.dot(self.weights)
        mean_return = portfolio_returns.mean()
        std_dev = portfolio_returns.std()
        
        num_trading_days = 252 * self.horizon_years
        simulation_results = np.zeros((num_simulations, num_trading_days + 1))
        simulation_results[:, 0] = self.initial_capital

        for i in range(num_simulations):
            random_returns = np.random.normal(mean_return, std_dev, num_trading_days)
            for t in range(1, num_trading_days + 1):
                simulation_results[i, t] = simulation_results[i, t-1] * (1 + random_returns[t-1])
        
        final_values = simulation_results[:, -1]
        return {
            "num_simulations": num_simulations, "horizon_years": self.horizon_years,
            "10th_percentile_outcome": f"${np.percentile(final_values, 10):,.2f}",
            "50th_percentile_outcome (Median)": f"${np.percentile(final_values, 50):,.2f}",
            "90th_percentile_outcome": f"${np.percentile(final_values, 90):,.2f}",
        }

    # --- Main Agentic Function (Unchanged) ---
    def run(self):
        """Executes the full analysis workflow."""
        self._fetch_historical_data()
        if self.historical_data.empty or len(self.historical_data) < 252:
            print("Not enough historical data to perform analysis.")
            return {"error": "Could not retrieve sufficient historical data for the given tickers."}

        backtest_results = self._calculate_performance_metrics()
        monte_carlo_forecast = self._run_monte_carlo_simulation()
        analysis_report = {
            "portfolio": self.portfolio_weights_dict, # Use the simple dict for the report
            "analysis_period_years": self.horizon_years,
            "backtest_results": backtest_results,
            "monte_carlo_forecast": monte_carlo_forecast,
            "risk_warnings": self._generate_warnings(backtest_results)
        }
        return analysis_report

    def _generate_warnings(self, backtest_results):
        warnings = []
        # Use .get() to avoid errors if a key is missing
        max_drawdown_str = backtest_results.get('max_drawdown', '0%')
        volatility_str = backtest_results.get('annual_volatility', '0%')

        if float(max_drawdown_str.strip('%')) < -30.0:
            warnings.append("High Max Drawdown: This portfolio has historically experienced significant drops.")
        if float(volatility_str.strip('%')) > 20.0:
            warnings.append("High Volatility: Portfolio value is expected to fluctuate significantly.")
        return warnings


# --- Example of how to use the agent ---
if __name__ == "__main__":
    import json
    
    # --- MOCK DATA from the PortfolioConstructionAgent ---
    # Note the structure with the 'holdings' key
    sample_portfolio = {
        "portfolioName": "C-12345_Moderate_V1",
        "assetAllocation": {"Equity": "80.00%", "Bonds": "20.00%"},
        "holdings": [
            {"ticker": "VTI", "percentage": 0.6},
            {"ticker": "AGG", "percentage": 0.4}
        ],
        "rationale": "Optimized for a moderate profile."
    }

    # Create and run the analysis agent
    analysis_agent = PortfolioAnalysisAgent(
        portfolio=sample_portfolio,
        investment_horizon_years=10,
        initial_capital=250000
    )
    report = analysis_agent.run()
    
    # Pretty-print the final report
    print("\n--- Portfolio Analysis Report ---")
    print(json.dumps(report, indent=2))
    
    # Save the report to a JSON file
    with open("portfolio_analysis_report.json", "w") as f:
        json.dump(report, f, indent=2)