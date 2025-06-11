import asyncio
import json
from browser_use import Agent, BrowserProfile
from langchain_google_genai import ChatGoogleGenerativeAI

from dotenv import load_dotenv
load_dotenv()

browser = BrowserProfile(
    user_data_dir=r'C:\Users\Lenovo\AppData\Local\Chromium\User Data',
)

async def main():
    agent = Agent(
        task="""Go to www.linkedin.com, Search for the posts where some users have posted about their recent promotions 
                or new jobs at a company in India.You can Search for phrases like 'I am happy to announce that I am joining ' or 
                'I am happy to share that I am starting a new position as '. Go to that user's profile and Collect the names and 
                details of these users in a JSON like this 
                {
                    "name": "John Doe",
                    "job_title": "Software Engineer",
                    "company": "Tech Company",
                    "location": "India",
                }.
                Stop when you have got 3 users in a json that match the criteria.""",
        llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-05-20", temperature=0.0),
        browser_profile=browser
    )
    result = await agent.run()
    with open("result.json", "w", encoding="utf-8") as f:
        try:
            json.dump(result.extracted_content(), f, ensure_ascii=False, indent=2)
        except TypeError:
            # If result is not serializable, save as string
            f.write(str(result))
    return result.extracted_content()

def run_agent():
    return asyncio.run(main())

if __name__ == "__main__":
    run_agent()