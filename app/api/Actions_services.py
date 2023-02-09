from fastapi.responses import StreamingResponse
from typing import Union, List
from pydantic import BaseModel
import openai
import os
import backoff

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def completions_with_backoff(**kwargs):
    return openai.Completion.create(**kwargs)


#set env variable of api key
openai.api_key = os.environ["OPENAI_API_KEY"]


class connect_live_agent_params(BaseModel):
    pass

def connect_live_agent_run(params: connect_live_agent_params):
    """
    ## Description
    swaps the chatbot for a live agent
    """
    #TODO: add code
    return "hello world"

class response_params(BaseModel):
    chat_log: Union[List[str],None]=[""]
    current_user: Union[str,None]="User 1:"
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 250
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0

def response_run(params: response_params):
    """
    ## Description
    responds to a message with GPT response
    """
    prompt = ""
    for i in params.chat_log:
        prompt += i+"\n"
    gpt_iter = completions_with_backoff(
        model="text-davinci-003",
        prompt="""The following is a conversation with an assistant. The assistant is helpful, creative, clever, and very friendly.
        \n"""+prompt+params.current_user,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["User 1:", "User 2:"],
        stream=True
    )
    def iterfile():
        for i in gpt_iter:
            yield str(i.choices[0].text)

    return StreamingResponse(iterfile(), media_type="text/plain")


class guide_message_params(BaseModel):
    guidance: Union[str,None]=""
    chat_log: Union[List[str],None]=[""]
    current_user: Union[str,None]="User 1:"
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 250
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0

def guide_message_run(params: guide_message_params):
    """
    ## Description
    responds to a message with GPT response
    """
    prompt = ""
    for i in params.chat_log:
        prompt += i+"\n"
    gpt_iter = completions_with_backoff(
        model=params.engine,
        prompt="""The following is a conversation with an assistant. The assistant is helpful, creative, clever, and very friendly.
        \n"""+prompt+"\nresponse subject: "+params.guidance+"\n"+params.current_user,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["User 1:", "User 2:"],
        stream=True
    )
    def iterfile():
        for i in gpt_iter:
            yield str(i.choices[0].text)

    return StreamingResponse(iterfile(), media_type="text/plain")

class cache_data_params(BaseModel):
    chat_history: Union[List[str],None]=""
    input: Union[str,None]=""

def cache_data_run(params: cache_data_params):
    """
    ## Description
    caches the data for future use
    """
    #TODO: add code
    return "hello world"

class extract_info_params(BaseModel):
    context: Union[str,None]="",
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 250
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0

def extract_info_run(params: extract_info_params):
    """
    ## Description
    extracts information from the user
    """
    gpt_iter = completions_with_backoff(
        model=params.engine,
        prompt=params.context+"\nGiven the above, extract a few key notes relevant to a therapist, and use dashes for each note:",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stream=True
    )
    def iterfile():
        for i in gpt_iter:
            yield str(i.choices[0].text)
    return StreamingResponse(iterfile(), media_type="text/plain")
    

class biased_extract_params(BaseModel):
    bias: Union[str,None]="",
    context: Union[str,None]="",
    engine: Union[str,None]="text-davinci-003",
    temperature: Union[float,None] = 0.9
    max_tokens: Union[int,None] = 250
    top_p: Union[float,None] = 1
    frequency_penalty: Union[float,None] = 0
    presence_penalty: Union[float,None] = 0

def biased_extract_run(params: extract_info_params):
    """
    ## Description
    extracts information from the user
    """
    gpt_iter = completions_with_backoff(
        model=params.engine,
        prompt=params.context+"\nGiven the above, extract \""+params.bias+"\" information and note it with a - in front:",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stream=True
    )
    def iterfile():
        for i in gpt_iter:
            yield str(i.choices[0].text)
    return StreamingResponse(iterfile(), media_type="text/plain")