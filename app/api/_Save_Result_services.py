from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel

#parameters for _Save_Result_
class _Save_Result_params(BaseModel):
    #TODO: add parameters
    temp: Union[str,None]="",

# Allows the user to save the result for future use. 
def _Save_Result_run(params: _Save_Result_params):
    #TODO: add code
    return "hello world"