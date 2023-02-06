from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

#parameters for _Delete_Diary_Entry_
class _Delete_Diary_Entry_params(BaseModel):
    #TODO: add parameters
    temp: Union[str,None]="",

# Allows user to delete an existing diary entry.
def _Delete_Diary_Entry_run(params: _Delete_Diary_Entry_params):
    #TODO: add code
    return "hello world"