"""
GenAI Portfolio Maker: End-to-End Workflow

This script integrates all agents in the following order:
1. ClientProfilerAgent
2. MarketResearchAgent
3. PortfolioConstructionAgent
4. PortfolioAnalysisAgent
5. ReportingAndCustomizationAgent

It demonstrates a full pipeline for generating a GenAI-powered financial portfolio and report.
"""
import json
import os
from portfolio_construction.client_profiler import ClientProfilerAgent
from portfolio_construction.market_analysis import MarketResearchAgent
from portfolio_construction.portfolio_construction import PortfolioConstructionAgent
from portfolio_construction.portfolio_analysis import PortfolioAnalysisAgent
from portfolio_construction.reporting_customization import ReportingAndCustomizationAgent
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import uvicorn
from fastmcp import FastMCP


# --- 1. Client Profiling ---
def run_client_profiling(client_id, conversation_text):
    profiler = ClientProfilerAgent()
    profile = profiler.run(client_id, conversation_text)
    with open(f"{client_id}_profile.json", "w", encoding="utf-8") as f:
        json.dump(profile, f, indent=2)
    print(f"[1] Client profile saved: {client_id}_profile.json")
    return profile

# --- 2. Market Research ---
def run_market_research():
    market_agent = MarketResearchAgent()
    market_brief = market_agent.run()
    with open("market_conditions_brief.json", "w", encoding="utf-8") as f:
        json.dump(market_brief, f, indent=2)
    print("[2] Market conditions brief saved: market_conditions_brief.json")
    return market_brief

# --- 3. Portfolio Construction ---
def run_portfolio_construction(profile):
    constructor = PortfolioConstructionAgent(profile)
    portfolio = constructor.run()
    with open(f"constructed_portfolio_{profile['clientId']}.json", "w", encoding="utf-8") as f:
        json.dump(portfolio, f, indent=2)
    print(f"[3] Constructed portfolio saved: constructed_portfolio_{profile['clientId']}.json")
    return portfolio

# --- 4. Portfolio Analysis ---
def run_portfolio_analysis(portfolio, profile):
    horizon = profile.get("investmentHorizon", 10) or 10
    initial_capital = 100000  # Default; could be customized
    analysis_agent = PortfolioAnalysisAgent(portfolio, investment_horizon_years=horizon, initial_capital=initial_capital)
    analysis = analysis_agent.run()
    with open(f"portfolio_analysis_{profile['clientId']}.json", "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)
    print(f"[4] Portfolio analysis saved: portfolio_analysis_{profile['clientId']}.json")
    return analysis

# --- 5. Report Generation ---
def run_report_generation(profile, portfolio, analysis, customization_options):
    reporting_agent = ReportingAndCustomizationAgent()
    report = reporting_agent.generate_report(profile, portfolio, analysis, customization_options)
    report_filename = f"client_report_{profile['clientId']}.md"
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"[5] Client report saved: {report_filename}")
    return report_filename

app = FastAPI(title="GenAI Portfolio Maker API")

@app.get("/generate_portfolio_report")
def generate_portfolio_report(
    message: str = Query(..., description="Client's conversation text for profiling")
):
    """Generates a financial portfolio report based on client input conversation text and a given client id.
    This endpoint profiles the client, conducts market research, constructs a portfolio,
    analyzes the portfolio, and generates a report.
    """
    client_id = "C-001"
    try:
        # 1. Profile the client
        profile = run_client_profiling(client_id, message)

        # 2. Get market research (optional for construction, but useful for reporting)
        market_brief = run_market_research()

        # 3. Construct a portfolio
        portfolio = run_portfolio_construction(profile)

        # 4. Analyze the portfolio
        analysis = run_portfolio_analysis(portfolio, profile)

        # 5. Generate a report (for client)
        customization_options = {
            "target_audience": "client",
            "report_format": "markdown",
            "tone": "professional and encouraging",
        }
        report_file = run_report_generation(profile, portfolio, analysis, customization_options)

        # Read the generated report and return its content
        with open(report_file, "r", encoding="utf-8") as f:
            report_content = f.read()

        return {
            "client_report": report_content
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# --- MAIN WORKFLOW ---
if __name__ == "__main__":
    # --- Example client conversation (could be replaced with user input or file read) ---
    client_id = "C-001"
    conversation_text = """
    Honestly, I'm very nervous about the market right now. My main goal is just to make sure my
    nest egg is safe for my retirement in about 10 years. I've worked hard for this money and
    I really can't afford to lose a significant portion of it. I'd rather have slow, steady
    growth than take any big risks. I definitely don't want any part of volatile tech stocks.

    I want the portfolio to be diversified, with different holdings that can provide
    stability. I also want to avoid any investments that are too complex or hard to understand.
    I just want something straightforward that I can trust to grow my money safely over the
    next decade. I preferably want multiple asset classes, like bonds and some stable
    dividend-paying stocks, but nothing too aggressive.
    """
    client_id2 = "C-002"

    conversation_text2 = """

    I'm looking to invest for my child's education, which is about 15 years away. I want to
    ensure that the money grows steadily without too much risk. I don't mind some exposure to
    equities, but I want to avoid anything too volatile. My main goal is to have a solid
    portfolio that can weather market fluctuations and provide a good return over the long term.
    """
    client_id3 = "C-003"

    conversation_text3  = """
    I'm a young professional with a high risk tolerance. I want to maximize my returns over the
    next 20 years. I'm comfortable with volatility and want to invest in high-growth sectors,
    especially in technology and renewable energy. I also care about ESG factors and want to
    ensure my investments align with my values. I'm looking for a portfolio that can deliver
    aggressive growth while also considering sustainability.

    I want my portfolio to be as diversified as possible, with a mix of high-growth stocks,
    some international exposure, and maybe even some alternative investments like cryptocurrencies
    or real estate. I believe in the potential of emerging markets and want to include some
    investments there as well. I also want to ensure that my portfolio is adaptable to changing
    market conditions, so I can take advantage of new opportunities as they arise.
    I want to avoid any investments that are too conservative or slow-growing, as I'm looking
    for significant capital appreciation over the long term.
    I also want to ensure that my portfolio is adaptable to changing market conditions, so I can
    take advantage of new opportunities as they arise.
    """

    # 1. Profile the client
    profile = run_client_profiling(client_id3, conversation_text3)

    # 2. Get market research (optional for construction, but useful for reporting)
    market_brief = run_market_research()

    # 3. Construct a portfolio
    portfolio = run_portfolio_construction(profile)

    # 4. Analyze the portfolio
    analysis = run_portfolio_analysis(portfolio, profile)

    # 5. Generate a report (for client)
    customization_options = {
        "target_audience": "client",
        "report_format": "markdown",
        "tone": "professional and encouraging",
        # Optionally, you could add market_brief to the prompt for more context
    }
    report_file = run_report_generation(profile, portfolio, analysis, customization_options)

    print("\nWorkflow complete! Open the generated report for review.")
    # To run the API: uncomment the following line
    # uvicorn.run("genai_portfolio_workflow:app", host="0.0.0.0", port=8000, reload=True)
