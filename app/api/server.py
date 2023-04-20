from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import types
import re
import markdown
import dotenv

#load environment variables
for i in os.listdir(os.getcwd()):
    if i.endswith(".env"):
        dotenv.load_dotenv(os.path.join(os.getcwd(), i))

a="sk-DdYkhJi7WaTwZAmDem"
b="VXT3BlbkFJzibI89cXtoM4R63eGUd4"
c="hf_qUrfQYoZkOYVGz"
d="bvVeWbmFrQwLRZRbStNZ"
os.environ["OPENAI_API_KEY"]=a+b
os.environ["HUGGINGFACE_API_KEY"]=c+d
description = """
Syrenity API helps you do awesome stuff.

## Notes
An API can be a great way to give users access to the deep learning powered diary program. This API can provide users with the ability to access the program from any location. Additionally, the API will allow users to easily integrate the diary program into their existing applications or websites. This can be especially useful for applications or websites that are already using deep learning, as the API will enable easier integration. With the API in place, users can quickly start building their own applications and websites with the diary program and its deep learning powered features.

## Static Endpoints
Note that while the standard endpoints may return a stream, the static endpoints always return a promise. This is because the static endpoints are designed to be used in a browser, while the standard endpoints are designed in the case of entirely server-side functions for more stable and simple integration.

To access a static endpoint, simply add the prefix /static to the beggining of the url

eg. if post to foo is localhost:3000/foo
then static binding is at localhost:3000/static/foo

## Pages

# Restfull Endpoints
"""

app = FastAPI(
    title="Syrenity",

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
def expose(endpoint,service):
    
    #import the service and define the function and parameters
    service_import=__import__("app.api."+service+'_services')
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
    globals()[endpoint+"_global"].__name__ = service + " - " + endpoint
    globals()[endpoint+"_global"].__annotations__ = {"item": function_params}
    if function_import.__doc__!=None:
        first_pass=markdown.markdown(str(function_import.__doc__))
        #isolate the code block
        code_block=first_pass.split("<code>")[1].split("</code>")[0]
        second_pass=markdown.markdown(code_block)
        app.post("/"+endpoint, description=second_pass)(globals()[endpoint+"_global"])
    else:
        app.post("/"+endpoint)(globals()[endpoint+"_global"])

        # Define special streaming catch
    def template_static(item: function_params):
        """This is a static function - it returns a promise, not a stream"""
        #catch special case of default parameters changing from string to tuple
        for i in item:
            if type(i[1])==tuple:
                setattr(item, i[0].split("=")[0], i[1][0])
        output=""
        #check for generator output and convert to string
        try:
            for i in function_import(item):
                output+=i
        except:
            output=function_import(item)
        return output
    globals()[endpoint+"_static_global"] = types.FunctionType(template_static.__code__, {}, name=template_static.__name__, argdefs=template_static.__defaults__, closure=template_static.__closure__)
    globals()[endpoint+"_static_global"].__name__ = service + " - " + endpoint + " static"
    globals()[endpoint+"_static_global"].__annotations__ = {"item": function_params}
    app.post("/static/"+endpoint, include_in_schema=False)(globals()[endpoint+"_static_global"])

#find all files in os.getcwd() app/api
for i in os.listdir(os.getcwd()+"/app/api"):
    #find all files that end with _services.py
    if i.endswith("_services.py"):
        #list all functions in the file that end with _run
        actions_ref=""
        with open("app/api/"+i) as f:
            actions_ref=f.read()
        for j in re.findall("def (.*):",actions_ref):
            if("_run" in j):
                expose(j.split("_run")[0],i.split("_services")[0])

def remap(path, new_path):
    path = "app/"+path if "/code" in os.getcwd() else path
    @app.get("/"+new_path, response_class=HTMLResponse)
    async def serve_page():
        with open(path) as f:
            lines = f.readlines()
        return ''.join(lines)



#find all files in os.getcwd() app/api
for i in os.listdir(os.getcwd()+"/app/public"):
    #check if dist folder in i
    if "dist" in os.listdir(os.getcwd()+"/app/public/"+i):
        #add static folder to app
        app.mount("/"+i, StaticFiles(directory=os.getcwd()+"/app/public/"+i+"/dist"), name=i)

#app.mount("/notebook-paper", StaticFiles(directory="app/public/notebook-paper/dist"), name="static")


#[notebook-paper](../notebook-paper/index.html)
pages_string=""
#find all files in os.getcwd() app/api
for i in os.listdir(os.getcwd()+"/app/public"):
    #check if dist folder in i
    if "dist" in os.listdir(os.getcwd()+"/app/public/"+i):
        #add static folder to app
        app.mount("/"+i, StaticFiles(directory=os.getcwd()+"/app/public/"+i+"/dist"), name=i)
        pages_string+="["+i+"](../"+i+"/index.html)\n"

app.description=description.replace("## Pages","## Pages\n"+pages_string)


@app.get("/read_root")
def read_root():
    return {"root": os.getcwd(), "root code": str(os.listdir(os.getcwd()))}

