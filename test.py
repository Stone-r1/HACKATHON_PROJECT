from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv('API_KEY'))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="i'll give you one complicated word, you return one synonym of that word and three distraction words.also make words moderately rare and complicated for college student. return just words nothing more first being synonym others distraction. word is 'compartmentalize'",
)

print(response.text)

