from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel
import openai
import os

openai.api_key = os.environ["OPENAI_API_KEY"]

#parameters for _Generate_Insights_
class _Generate_Insights_params(BaseModel):
    #TODO: add parameters
    temp: Union[str,None]="",

# Uses deep learning to generate insights from the diary entries.
def _Generate_Insights_run(params: _Generate_Insights_params):
    #TODO: add code
    return "hello world"