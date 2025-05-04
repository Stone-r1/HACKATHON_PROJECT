import os
import random
from dotenv import load_dotenv
from google import genai


class WordExplorer:
    def __init__(self, word_count = 10):
        load_dotenv()
        self.API_KEY = os.getenv('API_KEY')
        self.client = genai.Client(api_key = self.API_KEY)
        self.word_count = word_count
        self.words = self.loadWords()


    def loadWords(self):
        with open("words.txt", 'r') as file:
            return [line.strip() for line in file if line.strip()]


    def chooseRandomWords(self):
        return random.sample(self.words, self.word_count)


    def buildPrompt(self, word_list): # good prompt :D
        return f""" 
        Given a list of ten words, the task is to generate, for each word, a group of four words that follow a specific pattern. Each group must contain exactly one word that is a synonym of the original word from the list. The remaining three words in the group should be unrelated to both the original word and its synonym. These unrelated words should be randomly chosen but remain within a vocabulary level appropriate for college students—challenging, but not obscure. The four words in each group should be presented in a clean and uniform format: capitalized, But not written just in caps, separated by single spaces, and with no punctuation or extra explanation. The result should be a simple, readable list of ten lines, each line containing four words that meet these criteria.
The words are: {'; '.join(word_list)}.
"""


    def queryModel(self, prompt):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return response.text


    def parseResponse(self, response):
        result = {}
        for line in response.strip().split('\n'):
            words = line.strip().split()
            if len(words) == 5:
                key = (words[0], words[1])
                value = words[2:]
                result[key] = value
        return result


    def run(self):
        selected_words = self.chooseRandomWords()
        prompt = self.buildPrompt(selected_words)
        response = self.queryModel(prompt)
        result = self.parseResponse(response)
        print(result)


if __name__ == "__main__":
    explorer = WordExplorer(10)
    explorer.run()
