from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

#parameters for _Get_Single_Diary_Entry_
class _Get_Single_Diary_Entry_params(BaseModel):
    #TODO: add parameters
    temp: Union[str,None]="",

# Retrieve a single diary entry from the system.
def _Get_Single_Diary_Entry_run(params: _Get_Single_Diary_Entry_params):
    #TODO: add code
    return "hello world"