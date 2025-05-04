import os
import json
from dotenv import load_dotenv
from google import genai


class WordExplorer:
    def __init__(self, word_file):
        load_dotenv()
        self.API_KEY = os.getenv('API_KEY')
        self.client = genai.Client(api_key=self.API_KEY)
        self.word_file = word_file
        self.words = self.loadWords()


    def loadWords(self):
        try:
            with open(self.word_file, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            print(f"Error: The file {self.word_file} was not found.")
            return []


    def buildPrompt(self, word_list):
        return f""" 
        Please provide a simple definition for each of the following words. 
        Keep the definitions clear, concise, and free of any additional symbols or formatting:
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
        lines = response.strip().split('\n')
        for line in lines:
            if line.strip():
                try:
                    word, definition = line.split(":", 1)
                    result[word.strip()] = definition.strip()
                except ValueError:
                    continue
        return result


    def saveDefinitions(self, definitions, filename="wordDefinition.json"):
        try:
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(definitions, file, ensure_ascii=False, indent=4)
            print(f"Definitions saved to {filename}")
        except Exception as e:
            print(f"Error saving definitions: {e}")


    def run(self):
        if not self.words:
            return
        prompt = self.buildPrompt(self.words)
        response = self.queryModel(prompt)
        result = self.parseResponse(response)
        self.saveDefinitions(result)


if __name__ == "__main__":
    word_file = ".temp.txt"
    explorer = WordExplorer(word_file)
    explorer.run()

