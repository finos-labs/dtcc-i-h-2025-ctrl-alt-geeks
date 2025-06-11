import pandas as pd
import yfinance as yf
from pypfopt import EfficientFrontier, risk_models, expected_returns
from pypfopt.exceptions import OptimizationError

class PortfolioConstructionAgent:
    def __init__(self, client_profile: dict):
        """
        Initializes the agent with the client's structured profile.
        :param client_profile: A dictionary containing riskProfile, constraints, etc.
        """
        self.profile = client_profile
        self.asset_universe = []

    # --- Tool 1: Asset Universe Selection ---
    def _select_asset_universe(self):
        """Selects a pool of assets based on the client's risk profile and constraints."""
        print(f"Selecting asset universe for a '{self.profile['riskProfile']}' profile...")
        
        # Base asset classes
        universe = {
            "US Equity": "VTI",          # Total US Stock Market
            "Intl Equity": "VXUS",       # Total International Stock Market
            "US Bonds": "AGG",           # Aggregate US Bond Market
            "High-Yield Bonds": "JNK",   # Riskier bonds
            "Real Estate": "VNQ",        # US Real Estate
            "Growth Tech": "QQQ"         # Nasdaq 100
        }

        # Tailor the universe based on risk profile
        if self.profile['riskProfile'] == 'Conservative':
            self.asset_universe = [universe["US Equity"], universe["Intl Equity"], universe["US Bonds"]]
        elif self.profile['riskProfile'] == 'Moderate':
            self.asset_universe = [universe["US Equity"], universe["Intl Equity"], universe["US Bonds"], universe["Real Estate"]]
        elif self.profile['riskProfile'] == 'Aggressive Growth':
            self.asset_universe = [universe["US Equity"], universe["Intl Equity"], universe["High-Yield Bonds"], universe["Growth Tech"]]
        else: # Default to a balanced mix
            self.asset_universe = [universe["US Equity"], universe["Intl Equity"], universe["US Bonds"]]
        
        # Handle constraints like ESG
        if "ESG-focused" in self.profile.get("constraints", []):
            print("Applying ESG constraint: Swapping VTI for ESGV")
            if "VTI" in self.asset_universe:
                self.asset_universe[self.asset_universe.index("VTI")] = "ESGV" # ESG Aware US Equity ETF
        
        print(f"Selected Tickers: {self.asset_universe}")

    # --- Tool 2: Optimization Engine ---
    def _optimize_portfolio(self):
        """
        Fetches data and runs the optimization based on the selected objective.
        """
        if not self.asset_universe:
            return None, "Asset universe is empty."

        try:
            print("Fetching data for optimization...")
            # Fetch 5 years of historical data
            # NEW, FIXED LINE
            # NEW, FIXED LINE
            prices = yf.download(self.asset_universe, period="5y")['Close'].dropna()

            # Calculate expected returns and sample covariance matrix
            # mu is the annualized sample return, S is the sample covariance matrix
            mu = expected_returns.mean_historical_return(prices)
            S = risk_models.sample_cov(prices)
            
            # Initialize the optimizer
            ef = EfficientFrontier(mu, S)
            
            # Set the optimization objective based on the risk profile
            objective_rationale = ""
            if self.profile['riskProfile'] == 'Conservative':
                ef.min_volatility()
                objective_rationale = "Optimized for minimum volatility to prioritize capital preservation."
            else: # For Moderate and Aggressive, we aim for the best risk-adjusted return
                ef.max_sharpe()
                objective_rationale = "Optimized for the highest Sharpe Ratio (best risk-adjusted return)."

            # Get the raw weights and clean them (removes tiny weights)
            weights = ef.clean_weights()
            
            # Format the output
            holdings = [{"ticker": ticker, "percentage": weight} for ticker, weight in weights.items() if weight > 0]
            
            return holdings, objective_rationale

        except (ValueError, OptimizationError) as e:
            return None, f"Could not optimize for the given assets. Error: {e}"
        except Exception as e:
            return None, f"An unexpected error occurred during optimization: {e}"

    # --- Main Agentic Function ---
    def run(self):
        """
        Executes the full portfolio construction workflow.
        """
        self._select_asset_universe()
        holdings, rationale = self._optimize_portfolio()
        
        if not holdings:
            return {"error": rationale}

        # Calculate the overall asset allocation from the holdings
        # This part could be more sophisticated by mapping tickers to asset classes
        asset_allocation = {
            "Equity": sum(h['percentage'] for h in holdings if h['ticker'] in ["VTI", "VXUS", "QQQ", "ESGV"]),
            "Bonds": sum(h['percentage'] for h in holdings if h['ticker'] in ["AGG", "JNK"]),
            "Real Estate": sum(h['percentage'] for h in holdings if h['ticker'] == "VNQ")
        }
        
        portfolio_name = f"{self.profile['clientId']}_{self.profile['riskProfile'].replace(' ', '_')}_V1"

        return {
            "portfolioName": portfolio_name,
            "assetAllocation": {k: f"{v:.2%}" for k, v in asset_allocation.items() if v > 0},
            "holdings": holdings,
            "rationale": rationale
        }

# --- Example of how to use the agent ---
if __name__ == "__main__":
    import json

    # --- Scenario 1: A moderate client ---
    moderate_client_profile = {
        "clientId": "C-12345",
        "riskProfile": "Moderate",
        "constraints": []
    }
    
    print("--- Running for Moderate Client ---")
    construction_agent_mod = PortfolioConstructionAgent(moderate_client_profile)
    moderate_portfolio = construction_agent_mod.run()
    print("\nGenerated Portfolio:")
    print(json.dumps(moderate_portfolio, indent=2))
    print("-" * 40)

    # --- Scenario 2: An aggressive growth client with an ESG preference ---
    aggressive_esg_client_profile = {
        "clientId": "C-67890",
        "riskProfile": "Aggressive Growth",
        "constraints": ["ESG-focused"]
    }
    
    print("\n--- Running for Aggressive ESG Client ---")
    construction_agent_agg = PortfolioConstructionAgent(aggressive_esg_client_profile)
    aggressive_portfolio = construction_agent_agg.run()
    print("\nGenerated Portfolio:")
    print(json.dumps(aggressive_portfolio, indent=2))
    portfolios = {
        "moderate_client_portfolio": moderate_portfolio,
        "aggressive_esg_client_portfolio": aggressive_portfolio
    }
    with open("constructed_portfolios.json", "w", encoding="utf-8") as f:
        json.dump(portfolios, f, indent=2)