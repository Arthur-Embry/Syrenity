from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import types

description = """
Syrenity API helps you do awesome stuff.

## Notes

 file

## Notes
The program to calculate the time for an object to drop can be a useful tool for those who need to measure the amount of time it takes for an object to fall from a certain height. This could be used for a variety of applications, such as scientific experiments, engineering projects, or even for recreational activities. Additionally, having an API to access this program would make it much easier to use, allowing users to quickly and easily access the program from any device.

## Pages

[transformer-chatbot](../transformer-chatbot/index.html)


# Restfull Endpoints
"""

app = FastAPI(
    title="Syrenity",
    description=description,
)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#exposure template
#exposure template
def expose(endpoint,service):
    
    #import the service and define the function and parameters
    service_import=__import__("app.api."+service+'_services')### if "/code" in os.getcwd() else __import__("api."+service+'_services')
    print(service_import.__dict__['api'].__dict__[service+'_services'].__dict__[endpoint+'_run'])
    function_import=service_import.__dict__['api'].__dict__[service+'_services'].__dict__[endpoint+'_run']
    function_params=service_import.__dict__['api'].__dict__[service+'_services'].__dict__[endpoint+'_params']

    # Decorate it with your decorator and then pass it to FastAPI
    def template(item: function_params):
        #catch special case of default parameters changing from string to tuple
        for i in item:
            if type(i[1])==tuple:
                setattr(item, i[0].split("=")[0], i[1][0])

        return function_import(item)

        
    globals()[endpoint+"_global"] = types.FunctionType(template.__code__, {}, name=template.__name__, argdefs=template.__defaults__, closure=template.__closure__)
    globals()[endpoint+"_global"].__name__ = endpoint
    globals()[endpoint+"_global"].__annotations__ = {"item": function_params}
    app.post("/"+endpoint)(globals()[endpoint+"_global"])

def remap(path, new_path):
    path = "app/"+path if "/code" in os.getcwd() else path
    @app.get("/"+new_path, response_class=HTMLResponse)
    async def serve_page():
        with open(path) as f:
            lines = f.readlines()
        return ''.join(lines)



expose("_Calculate_Drop_Time","_Calculate_Drop_Time")
expose("_Input_Parameters","_Input_Parameters")
expose("_Output_Result","_Output_Result")
expose("_Save_Result","_Save_Result")
expose("_Retrieve_Previous_Results","_Retrieve_Previous_Results")


app.mount("/transformer-chatbot", StaticFiles(directory="app/public/transformer-chatbot/dist"), name="static")

#ping