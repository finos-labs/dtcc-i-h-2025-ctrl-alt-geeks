import os, json
import google.generativeai as genai
from IPython.display import display, Markdown
from dotenv import load_dotenv  # NEW: Import the load_dotenv function

# --- Configuration ---

# NEW: Load environment variables from the .env file
# This should be at the top of your script, before you access any variables.
load_dotenv()

try:
    # MODIFIED: The code now primarily relies on the .env file or a system environment variable.
    GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        # MODIFIED: Updated error message to be more specific.
        raise ValueError("GOOGLE_API_KEY not found. Please create a .env file with the key or set it as an environment variable.")

    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    print(f"Error configuring Gemini: {e}")
    print("Please ensure you have a valid Gemini API key configured in your .env file.")
    # Exit or handle the lack of API key appropriately
    exit()


class ReportingAndCustomizationAgent:
    """
    An agent that generates customized financial reports using the Gemini model.

    This agent synthesizes information from client profiling, portfolio construction,
    and analysis to create reports tailored to different audiences (e.g., client, advisor)
    and formats.
    """

    def __init__(self, model_name='gemini-1.5-flash-latest'):
        """
        Initializes the agent and the generative model.

        Args:
            model_name (str): The name of the Gemini model to use.
        """
        try:
            self.model = genai.GenerativeModel(model_name)
            print(f"ReportingAndCustomizationAgent initialized with model: {model_name}")
        except Exception as e:
            print(f"Error initializing generative model: {e}")
            self.model = None

    def _create_prompt(self, client_profile, constructed_portfolio, portfolio_analysis, customization_options):
        """
        Builds a detailed, structured prompt for the Gemini model.
        """
        # Unpack customization options with defaults
        target_audience = customization_options.get('target_audience', 'client')
        report_format = customization_options.get('report_format', 'markdown')
        tone = customization_options.get('tone', 'professional and encouraging')

        # Start building the prompt with role-playing and clear instructions
        prompt = f"""
        **Role:** You are a highly skilled financial analyst and communication expert. Your task is to generate a personalized financial portfolio report.

        **Objective:** Synthesize the provided client data, portfolio composition, and performance analysis into a clear, concise, and customized report.

        **Customization Guidelines:**
        - **Target Audience:** {target_audience}
        - **Report Format:** {report_format}
        - **Tone:** {tone}

        **Instructions based on Target Audience:**
        - If the audience is the 'client', use simple, easy-to-understand language. Avoid jargon. Focus on how the portfolio aligns with their personal goals. Be reassuring but realistic.
        - If the audience is a 'financial_advisor', you can use technical terms (like Sharpe Ratio, VaR). Focus on performance metrics, risk analysis, and potential rebalancing opportunities.

        **Input Data:**

        --- CLIENT PROFILE (from ClientProfilerAgent) ---
        {client_profile}

        --- CONSTRUCTED PORTFOLIO (from PortfolioConstructionAgent) ---
        {constructed_portfolio}

        --- PORTFOLIO ANALYSIS (from PortfolioAnalysisAgent) ---
        {portfolio_analysis}

        --- REQUIRED OUTPUT ---
        Based on all the above information and guidelines, please generate the report now.
        Ensure the structure is logical and easy to follow. For a markdown report, use headings, bullet points, and bold text to improve readability.
        Start with a summary, then detail the portfolio, analyze its performance in relation to the client's goals, and conclude with next steps or recommendations.
        """
        return prompt.strip()

    def generate_report(self, client_profile, constructed_portfolio, portfolio_analysis, customization_options):
        """
        Generates the report by calling the Gemini API.

        Args:
            client_profile (dict): Output from ClientProfilerAgent.
            constructed_portfolio (dict): Output from PortfolioConstructionAgent.
            portfolio_analysis (dict): Output from PortfolioAnalysisAgent.
            customization_options (dict): Options to tailor the report.

        Returns:
            str: The generated report as a string.
        """
        if not self.model:
            return "Error: Generative model is not initialized. Cannot generate report."

        try:
            prompt = self._create_prompt(
                client_profile,
                constructed_portfolio,
                portfolio_analysis,
                customization_options
            )

            print("\n--- Generating Report... ---")
            response = self.model.generate_content(prompt)

            return response.text

        except Exception as e:
            return f"An error occurred while generating the report: {e}"

# --- Main Execution Block (To demonstrate the agent) ---
if __name__ == "__main__":
    with open("conservative_profile.json", "r", encoding="utf-8") as f:
        mock_client_profile = json.load(f)

    with open("constructed_portfolios.json", "r", encoding="utf-8") as f:
        constructed_portfolios = json.load(f)
        mock_constructed_portfolio = constructed_portfolios["moderate_client_portfolio"]

    with open("portfolio_analysis_report.json", "r", encoding="utf-8") as f:
        mock_portfolio_analysis = json.load(f)


    # 2. INSTANTIATE THE AGENT
    reporting_agent = ReportingAndCustomizationAgent()

    # 3. GENERATE DIFFERENT TYPES OF REPORTS

    # --- Use Case 1: Standard report for the Client ---
    print("\n" + "="*50)
    print("1: Generating a standard report for the client...")
    print("="*50)
    client_report_options = {
        "target_audience": "client",
        "report_format": "markdown",
        "tone": "professional and encouraging"
    }
    client_report = reporting_agent.generate_report(
        mock_client_profile,
        mock_constructed_portfolio,
        mock_portfolio_analysis,
        client_report_options
    )
    print("\n--- Client Report (Markdown) ---\n")
    print(client_report)
    with open("client_report.md", "w", encoding="utf-8") as f:
        f.write(client_report)


    # --- Use Case 2: Technical report for a Financial Advisor ---
    print("\n" + "="*50)
    print("2: Generating a technical summary for a financial advisor...")
    print("="*50)
    advisor_report_options = {
        "target_audience": "financial_advisor",
        "report_format": "markdown",
        "tone": "analytical and direct"
    }
    advisor_report = reporting_agent.generate_report(
        mock_client_profile,
        mock_constructed_portfolio,
        mock_portfolio_analysis,
        advisor_report_options
    )
    print("\n--- Advisor Report (Markdown) ---\n")
    print(advisor_report)
    with open("advisor_report.md", "w", encoding="utf-8") as f:
        f.write(advisor_report)