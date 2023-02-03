from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel

#parameters for _Calculate_Drop_Time_
class _Calculate_Drop_Time_params(BaseModel):
    #TODO: add parameters
    temp: Union[str,None]="",

# Calculates the time it will take for an object to drop given certain parameters. 
def _Calculate_Drop_Time_run(params: _Calculate_Drop_Time_params):
    #TODO: add code
    return "hello world"