import os
import random
from dotenv import load_dotenv
from google import genai


class WordExplorer:
    def __init__(self, filepath: str, word_count: int = 10):
        load_dotenv()
        self.api_key = os.getenv('API_KEY')
        self.client = genai.Client(api_key=self.api_key)
        self.filepath = filepath
        self.word_count = word_count
        self.words = self.load_words()


    def load_words(self):
        with open(self.filepath, 'r') as file:
            return [line.strip() for line in file if line.strip()]


    def choose_random_words(self):
        return random.sample(self.words, self.word_count)


    def build_prompt(self, word_list): # good prompt :D
        return f""" 
        Given a list of ten words, the task is to generate, for each word, a group of four words that follow a specific pattern. Each group must contain exactly one word that is a synonym of the original word from the list. The remaining three words in the group should be unrelated to both the original word and its synonym. These unrelated words should be randomly chosen but remain within a vocabulary level appropriate for college students—challenging, but not obscure. The four words in each group should be presented in a clean and uniform format: capitalized, But not written just in caps, separated by single spaces, and with no punctuation or extra explanation. The result should be a simple, readable list of ten lines, each line containing four words that meet these criteria.
The words are: {'; '.join(word_list)}.
"""


    def query_model(self, prompt: str):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text


    def run(self):
        selected_words = self.choose_random_words()
        prompt = self.build_prompt(selected_words)
        response = self.query_model(prompt)
        print("Selected words:", selected_words)
        print("\nGemini response:\n")
        print(response)


if __name__ == "__main__":
    explorer = WordExplorer("words.txt", word_count=10)
    explorer.run()
