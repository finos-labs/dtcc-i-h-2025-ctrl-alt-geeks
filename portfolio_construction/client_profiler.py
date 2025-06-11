import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import sent_tokenize
import re

class ClientProfilerAgent:
    def __init__(self):
        """Initializes the agent by loading the NLTK sentiment analyzer."""
        self.sentiment_analyzer = SentimentIntensityAnalyzer()
        
    # --- Tool 1: Sentiment Analysis for Risk Tolerance ---
    def _get_sentiment_score(self, text: str) -> float:
        """
        Analyzes the text and returns a compound sentiment score.
        Score ranges from -1 (very negative/fearful) to +1 (very positive/aggressive).
        """
        return self.sentiment_analyzer.polarity_scores(text)['compound']

    # --- Tool 2: Keyword and Pattern Extraction (using NLTK and Regex) ---
    def _extract_details(self, text: str) -> dict:
        """Extracts goals, constraints, and investment horizon from the text."""
        goals = []
        constraints = []
        horizon = None

        # Define our keyword dictionaries
        goal_keywords = ['retire', 'retirement', 'college', 'house', 'education', 'legacy']
        constraint_keywords = ['no', 'avoid', 'without', 'hate', "don't want"]
        esg_keywords = ['esg', 'green', 'sustainable', 'ethical', 'clean energy']
        # A simple list of financial nouns to look for after a negative keyword
        avoidance_targets = ['oil', 'tobacco', 'gambling', 'crypto', 'volatile stocks', 'tech stocks']
        
        # Use NLTK to break the text into sentences for more accurate context
        sentences = sent_tokenize(text)
        
        for sentence in sentences:
            sent_lower = sentence.lower()
            
            # Goal extraction
            if any(keyword in sent_lower for keyword in goal_keywords):
                goals.append(sentence.strip())
            
            # ESG Constraint extraction
            if any(keyword in sent_lower for keyword in esg_keywords):
                constraints.append("ESG-focused")

            # Negative Constraint extraction (simpler approach without POS tagging)
            if any(keyword in sent_lower for keyword in constraint_keywords):
                for target in avoidance_targets:
                    if target in sent_lower:
                        constraints.append(f"Avoid {target.capitalize()}")

        # Investment Horizon using regex (the most reliable method for this)
        # Find patterns like "15 years" or "ten years"
        match = re.search(r'(\d{1,2})\s+years', text, re.IGNORECASE)
        if match:
            horizon = int(match.group(1))
        
        return {
            "goals": list(set(goals)), # Use set to remove duplicates
            "constraints": list(set(constraints)),
            "investmentHorizon": horizon
        }
        
    # --- Synthesizing the Profile ---
    def run(self, client_id: str, conversation_text: str):
        """
        Processes the client conversation to generate a structured profile.
        """
        print(f"Profiling client {client_id}...")
        
        # 1. Analyze sentiment for risk appetite
        sentiment_score = self._get_sentiment_score(conversation_text)
        
        # 2. Map sentiment score (-1 to +1) to a risk score (1 to 10)
        risk_score = round(((sentiment_score + 1) / 2) * 9 + 1, 1)

        # 3. Map numeric risk score to a qualitative profile
        if risk_score <= 3.0:
            risk_profile = "Conservative"
        elif risk_score <= 6.0:
            risk_profile = "Moderate"
        elif risk_score <= 8.5:
            risk_profile = "Aggressive Growth"
        else:
            risk_profile = "Very Aggressive"

        # 4. Extract specific goals and constraints
        details = self._extract_details(conversation_text)

        # 5. Assemble the final structured output
        profile = {
            "clientId": client_id,
            "riskScore": risk_score,
            "riskProfile": risk_profile,
            "sentimentAnalysis": f"{sentiment_score:.2f} (from -1 to 1)",
            "goals": details["goals"],
            "constraints": details["constraints"],
            "investmentHorizon": details["investmentHorizon"]
        }
        
        return profile


# --- Example of how to use the agent ---
if __name__ == "__main__":
    import json

    agent = ClientProfilerAgent()

    # --- Scenario 1: A Cautious, Conservative Client ---
    conservative_text = """
    Honestly, I'm very nervous about the market right now. My main goal is just to make sure my
    nest egg is safe for my retirement in about 10 years. I've worked hard for this money and
    I really can't afford to lose a significant portion of it. I'd rather have slow, steady
    growth than take any big risks. I definitely don't want any part of volatile tech stocks.
    """
    
    conservative_profile = agent.run("C-001", conservative_text)
    print("\n--- Conservative Client Profile ---")
    print(json.dumps(conservative_profile, indent=2))

    with open("conservative_profile.json", "w", encoding="utf-8") as f:
        json.dump(conservative_profile, f, indent=2)

    # --- Scenario 2: A Confident, Aggressive Client with an ESG preference ---
    aggressive_text = """
    I'm young and I'm looking for aggressive growth. I have a long time horizon, maybe 20 years
    before I'll need this money for retirement. I'm comfortable with volatility and want to maximize my returns.
    I'm particularly interested in sustainable investing and clean energy sectors. I believe that's the future.
    Let's aim high! I'd love to build a strong legacy.
    """
    
    aggressive_profile = agent.run("C-002", aggressive_text)
    print("\n--- Aggressive ESG Client Profile ---")
    print(json.dumps(aggressive_profile, indent=2))

    with open("aggressive_profile.json", "w", encoding="utf-8") as f:
        json.dump(aggressive_profile, f, indent=2)
