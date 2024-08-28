"""
title: MLX Pipeline
author: justinh-rahb
date: 2024-05-27
version: 1.1
license: MIT
description: A pipeline for generating text using Apple MLX Framework.
requirements: requests, mlx-lm, huggingface-hub
environment_variables: MLX_HOST, MLX_PORT, MLX_MODEL, MLX_STOP, MLX_SUBPROCESS, HUGGINGFACE_TOKEN
"""
import tweepy
#M744QevSvcx*NK)
import requests
import json
from typing import List, Union, Generator, Iterator
from pydantic import BaseModel
from schemas import OpenAIChatMessage
from blueprints.function_calling_blueprint import Pipeline as FunctionCallingBlueprint
import requests
import os


class Pipeline:
    class Valves(BaseModel):
        # List target pipeline ids (models) that this filter will be connected to.
        # If you want to connect this filter to all pipelines, you can set pipelines to ["*"]
        pipelines: List[str] = ["*"]

        # Assign a priority level to the filter pipeline.
        # The priority level determines the order in which the filter pipelines are executed.
        # The lower the number, the higher the priority.
        priority: int = 0

        pass

    def __init__(self):
        # Optionally, you can set the id and name of the pipeline.
        # Best practice is to not specify the id so that it can be automatically inferred from the filename, so that users can install multiple versions of the same pipeline.
        # The identifier must be unique across all pipelines.
        # The identifier must be an alphanumeric string that can include underscores or hyphens. It cannot contain spaces, special characters, slashes, or backslashes.
        #self.id = "chatbot_pipeline"

        self.name = "Chatbot Pipeline"
        self.valves = self.Valves(**{"pipelines": ["*"]})

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
            data = ''
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
            print(jsonArray)

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


            return (tweetText+"tweetText") if tweetText else "No information found"
