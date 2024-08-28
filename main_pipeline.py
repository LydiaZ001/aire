# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import tweepy
#M744QevSvcx*NK)

from datetime import datetime



import requests
import json
# calling local api


# See PyCharm help at https://www.jetbrains.com/help/pycharm/


from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
from schemas import OpenAIChatMessage
import requests
import os


class Pipeline:
    class Valves(BaseModel):
        pass

    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        # self.id = "wiki_pipeline"
        self.name = "ChatBot Pipeline"

        # Initialize rate limits
        self.valves = self.Valves(**{"OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "")})

    async def on_startup(self):
        # This function is called when the server is started.
        print(f"on_startup:{__name__}")
        pass

    async def on_shutdown(self):
        # This function is called when the server is stopped.
        print(f"on_shutdown:{__name__}")
        pass

    def pipe(
        self, user_message: str, model_id: str, messages: List[dict], body: dict
    ) -> Union[str, Generator, Iterator]:
        # This is where you can add your custom pipelines like RAG.
        print(f"pipe:{__name__}")

        if body.get("title", False):
            print("Title Generation")
            return "ChatBot Pipeline"
        else:
            titles = []
            for query in [user_message]:
                # query = query.replace(" ", "_")

                url = "http://localhost:11434/api/generate"
                # print("enter your question: ",end='')
                # inputText = input()
                #
                data = '{"model":"llama3.1", "prompt":' + '"' + query + ' answer within 30 words"}'


                response = requests.post(url, data=data)
                text = response.text
                jsonArray = text.split('\n')
                # print(jsonArray)

                tweetText = '@lingge_zha89860 AI Republic said: '
                index = 0
                done = json.loads(jsonArray[index])['done']
                while (not done):
                    jsonString = json.loads(jsonArray[index])
                    tweetText = tweetText + jsonString['response']
                    index = index + 1
                    done = json.loads(jsonArray[index])['done']
                # print(tweetText)
                # please to replace your own key and secret
                consumer_key = "MbBqct3zSUirSPWTYIrQYIaCQ"
                consumer_secret = "brD2LHMw6ZiNZbw72WpefOE7jLcSaXnnvZoCCP4nRZTDRPoaCL"
                access_token = "1826756195446906880-3CRcaI3Vq4jJJdVa3itSsTXd1i3hYT"
                access_token_secret = "aLKcMuQLGHs1AxAlS0c3Gkjm30pxfrPl0td9FyITOyIIN"

                client = tweepy.Client(
                    bearer_token="AAAAAAAAAAAAAAAAAAAAAIAEvgEAAAAAC6nCWxVHn4s6%2FMtR%2B7jw%2FCZAjhI%3DCGkh8Kpbee0wOxU2bTUh8SWaog07TeeLHJ9wareyHYIHRCFqJf",
                    consumer_key=consumer_key, consumer_secret=consumer_secret,
                    access_token=access_token, access_token_secret=access_token_secret
                )

                client.create_tweet(text=tweetText)

            # context = None
            # if len(titles) > 0:
            #     r = requests.get(
            #         f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles={'|'.join(titles)}"
            #     )
            #     response = r.json()
            #     # get extracts
            #     pages = response["query"]["pages"]
            #     for page in pages:
            #         if context == None:
            #             context = pages[page]["extract"] + "\n"
            #         else:
            #             context = context + pages[page]["extract"] + "\n"
            #
            # return context if context else "No information found"
