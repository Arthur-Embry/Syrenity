from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel

#parameters for _Output_Result_
class _Output_Result_params(BaseModel):
    #TODO: add parameters
    temp: Union[str,None]="",

# Displays the calculated drop time. 
def _Output_Result_run(params: _Output_Result_params):
    #TODO: add code
    return "hello world"