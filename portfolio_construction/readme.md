# GenAI Portfolio Maker: End-to-End Workflow

## Overview

This project provides an end-to-end workflow for generating a GenAI-powered financial portfolio and client report. The workflow integrates multiple modules to automate the process of client profiling, market research, portfolio construction, portfolio analysis, and report generation.

## Workflow Steps

1. **Client Profiling**  
   Uses `ClientProfiler` to analyze client conversation text and generate a personalized investment profile.

2. **Market Research**  
   Uses `MarketAnalysis` to analyze current market conditions and trends.

3. **Portfolio Construction**  
   Uses `PortfolioConstruction` to build a tailored investment portfolio based on the client profile and market research.

4. **Portfolio Analysis**  
   Uses `PortfolioAnalysis` to assess the constructed portfolio's risk, return, and other metrics.

5. **Reporting and Customization**  
   Uses `ReportingAndCustomization` to generate a professional, client-friendly report in Markdown format.

## Features

- **API and CLI Support:**  
  - Run the workflow as a script for batch processing.
  - Exposes a FastAPI endpoint (`/generate_portfolio_report`) for on-demand report generation.

- **Modular Agents:**  
  Each step is handled by a dedicated agent class, making the workflow extensible and maintainable.

- **Customizable Reports:**  
  Reports can be tailored for different audiences, formats, and tones.
