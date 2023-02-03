import openai
# Import the required module for text 
# to speech conversion
from gtts import gTTS
import Whisper
from playsound import playsound
# This module is imported so that we can 
# play the converted audio
import os
import Record
# Set your secret API key
openai.api_key="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"


def play_audio(text):
    # The text that you want to convert to audio
    mytext = text
    
    # Language in which you want to convert
    language = 'en'
    
    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed
    myobj = gTTS(text=mytext, lang=language, slow=False)
    
    # Saving the converted audio in a mp3 file named
    # welcome 
    myobj.save("cache.mp3")

    playsound("cache.mp3")

    #delete the file
    os.remove("cache.mp3")


#create a prompt and prompt active given a topic
def create_prompt(topic):
    prompt="The following conversation is between a supportive, well spoken and intelligent person (person A), and person B, where person B is asked about their "+topic
    prompt_active="The conversation continues, and person B is asked about their "+topic
    #create a global variable for the prompt and prompt active using the topic string
    globals()[topic+"_prompt"]=prompt
    globals()[topic+"_prompt_active"]=prompt_active
#create real prompts for each topic
for i in ("name","age","location","hobbies","favourite food","favourite colour","favourite animal","favourite sport","favourite movie","height","weight","eye colour","favourite music","favourite book"):
    create_prompt(i)
    

def converse(query_map):
    feedback=0
    text_log=[]
    while True:
        if feedback < len(query_map) and query_map[feedback]!=0:
            #print(query_map[feedback])
            text_log.append(query_map[feedback])
        feedback+=1
        print("AI: ",end="")
        text_log.append("Person A: ")
        prompt=""
        for i in text_log:
            prompt+=i
        #TODO generate ai response
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.9,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["Person A:", "Person B:"]
        )
        print(response["choices"][0]["text"].strip()+"\n",end="")
        play_audio(response["choices"][0]["text"].strip())
        text_log.append(response["choices"][0]["text"].strip()+"\n")
        print("Human: ",end="")
        text_log.append("Person B: ")
        a = Record.Recorder()
        a.listen()
        user_input = Whisper.analysis("user_cache.wav")
        print(user_input['transcription'])
        #user_input=input()
        text_log.append(user_input['transcription'].strip()+"\n")

query_map=[name_prompt,0,age_prompt_active,location_prompt_active]
converse(query_map)