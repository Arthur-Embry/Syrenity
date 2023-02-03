from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel

#parameters for _Input_Parameters_
class _Input_Parameters_params(BaseModel):
    #TODO: add parameters
    temp: Union[str,None]="",

# Allows the user to input parameters (mass, velocity, etc.) to calculate the drop time.
def _Input_Parameters_run(params: _Input_Parameters_params):
    #TODO: add code
    return "hello world"