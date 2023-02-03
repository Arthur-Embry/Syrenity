from fastapi.responses import StreamingResponse
from typing import Union
from pydantic import BaseModel

#parameters for _Retrieve_Previous_Results_
class _Retrieve_Previous_Results_params(BaseModel):
    #TODO: add parameters
    temp: Union[str,None]="",

# Retrieves any previous results stored in the system.
def _Retrieve_Previous_Results_run(params: _Retrieve_Previous_Results_params):
    #TODO: add code
    return "hello world"