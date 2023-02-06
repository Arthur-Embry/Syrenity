from fastapi.responses import StreamingResponse
from typing import Union, List
from pydantic import BaseModel
import openai
import os
import requests

openai.api_key = os.environ["OPENAI_API_KEY"]

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
headers = {"Authorization": "Bearer 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"}

class entry_classification_params(BaseModel):
    chat_history: Union[List[str],None]=[""],
    classifications: Union[List[str],None]=["trauma", "coping", "psychology"],

def entry_classification_run(params: entry_classification_params):
    """
    ## Description
    classifies an input into a category for relevant actions
    """
    
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    logs=""
    for i in params.chat_history:
        logs += i+"\n"
    output = query({
        "inputs": logs,
        "parameters": {"candidate_labels": params.classifications},
    })

    return output

class interjection_clasification_params(BaseModel):
    chat_history: Union[List[str],None]="",
    input: Union[str,None]="",
    response: Union[str,None]=""

def interjection_clasification_run(params: interjection_clasification_params):
    """
    ## Description
    classifies a response into a category for relevant actions
    """
    #TODO: add code
    return "hello world"

