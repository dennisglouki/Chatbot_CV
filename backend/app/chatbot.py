import faiss
import json
from google import genai
import pathlib
from app.prompt import SYSTEM_PROMPT
import numpy as np


class Bot:
    def __init__(self):
        self.client = genai.Client()

        data_folder = pathlib.Path(__file__).resolve().parent.parent / "data"

        self.index = faiss.read_index(
            str(data_folder / "cv.index")
        )

        with open(data_folder / "chunks.json") as f:
            self.chunks = json.load(f)

    def prepare_query(self, query):
        return f"task: search result | query: {query}"


    def embed_query(self, query):
        prepared_query = self.prepare_query(query)
        result = self.client.models.embed_content(
            model='gemini-embedding-2',
            contents=prepared_query,
        )
        embedding = result.embeddings[0].values

        return np.asarray(
            embedding,
            dtype=np.float32,
        )

    def search(self,query, k=3):
        query_embedding = self.embed_query(query)

        scores, indices = self.index.search(
            np.array([query_embedding]),
            k
        )

        return [
            self.chunks[i]
            for i in indices[0]
        ]

    def create_prompt(self, question,context):
        cont = ''
        for num, i in enumerate(context):
            cont += f'''Context {num+1}
            Source file: {i['source']}
            Page in Source: {i['page_nr']}
            Text of context: {i['text']}\n'''


        return f"""
    CONTEXT:
    {cont}

    USER QUESTION:
    {question}
    """


    def execute_bot(self, question):
        context = self.search(question)
        prompt = self.create_prompt(question, context)

        response = self.client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
            config={
                "system_instruction": SYSTEM_PROMPT,
            },
        )

        return response.text


