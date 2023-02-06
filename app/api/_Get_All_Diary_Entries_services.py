from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

#parameters for _Get_All_Diary_Entries_
class _Get_All_Diary_Entries_params(BaseModel):
    #TODO: add parameters
    temp: Union[str,None]="",

# Retrieve all diary entries stored in the system.
def _Get_All_Diary_Entries_run(params: _Get_All_Diary_Entries_params):
    #TODO: add code
    return "hello world"