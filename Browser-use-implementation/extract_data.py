from google import genai
from pydantic import BaseModel
import json


class User(BaseModel):
    name: str
    job_title: str
    company: str
    location: str


with open("result.json", "r", encoding="utf-8") as f:
    result_json_str = f.read()

client = genai.Client(api_key="AIzaSyCBMAXDOi-MjJfaTBZ4YLqH7OvAocS1Dd4")
response = client.models.generate_content(
    model="gemini-2.5-flash-preview-05-20",
    contents="""Read the following extract and return a JSON with type User." 
    Extract:"""+result_json_str,
    config={
        "response_mime_type": "application/json",
        "response_schema": list[User],
    },
)
print(response.text)
prospects : list[User] = response.parsed

try:
    with open("prospects.json", "w", encoding="utf-8") as f:
        f.write(response.text)
except TypeError as e:
    print(f"Error writing to file: {e}")
