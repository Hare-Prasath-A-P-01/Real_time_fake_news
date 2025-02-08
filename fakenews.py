from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq 
import streamlit as st 
from PIL import Image
import pytesseract
import base64
from gtts import gTTS
import tempfile
import os
import subprocess
import whisper
import wave
import av 
import numpy as np
import os

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

# Test if FFmpeg works
# os.system("ffmpeg -version")


import json
from typing import Any, Optional

from phi.tools import Toolkit
from phi.utils.log import logger
from duckduckgo_search import DDGS




class My_Agent():
    
    def Fake_news_Agent(self,news):
        
        Fake_Agent = Agent(
            name="FakenewsAgent",
            tools= [DuckDuckGo()],
            # model = Groq(id="deepseek-r1-distill-llama-70b")
            model = OpenAIChat(id="gpt-4o"),
            
            instructions=[
            "You are a fake news detector.",
            "Always analyze multiple sources before deciding.",
            "Provide sources for transparency.",
            "Respond only with 'FAKE' or 'REAL' followed by a brief explanation."
            "Dont access private information based on the government policy",],
            show_tool_calls=False,
            markdown=True
            )

      
        
        response =  Fake_Agent.run(f"Generate news based on: {news}")
        return response
        
    def news_generator(self,news_title):
        
        News_agent = Agent(
            name="News_Agent",
            tools=[DuckDuckGo()],
            model = Groq(id="deepseek-r1-distill-llama-70b"),
            instructions=[
                "You are a real-time news generator that fetches the latest and most relevant information from multiple sources.",
                "Always perform a comprehensive search across various sources before providing an answer.",
                "Include the source URLs in your responses to ensure transparency and credibility.",
                "Continuously collect and update news in real time."
            ],
            show_tool_calls=False,
            markdown=True
            )
        
        response = News_agent.run(f"Generate news based on: {news_title}")
        
        return response
        
        
        
#------------------------------------------------------------------------------
obj = My_Agent()



#-------------------------------------streamlit app---------------------------------------
st.set_page_config(
    page_title="Fare AI🤖",
    layout="wide"
)



def set_body_background(img_path):
    
    with open(img_path,'rb') as img_file:
        
        encoded_file = base64.b64encode(img_file.read()).decode()
        
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_file}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
        

set_body_background("1.png")

st.sidebar.title("More Options")
option = st.sidebar.radio(label="Select an Option",options=["Real Time Fake News Detection","Real Time News Search","Upload image to detect","Audio_Input"])



def set_sidebar_bg(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(
        f"""
        <style>
        [data-testid="stSidebar"] {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
    
def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename



    
set_sidebar_bg("back.png")
        
if option == "Real Time Fake News Detection":
    st.title("Fake News Detection")
    user_input = st.text_input("Enter the news text:")
    if st.button("Detect"):
        with st.spinner("Analyzing...🕵️"):
            result = obj.Fake_news_Agent(user_input)
            output_file = text_to_speech(result.content)
        st.markdown(f"### Result: {result.content}")
        st.audio(output_file,format="audio/wav")


elif option == "Real Time News Search":
    st.title("Real News Search")
    user_input = st.text_input("Enter topic:")
    if st.button("Search"):
        with st.spinner("Fetching latest news...🔍"):
            result = obj.news_generator(user_input)
            output_file = text_to_speech(result.content)
        st.markdown(f"### Search Result: {result.content}")
        st.audio(output_file,format="audio/wav")



    
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def recText(filename):
    text = pytesseract.image_to_string(Image.open(filename))
    return text
    
if option == "Upload image to detect":
    st.title("Image to detect")
    uploaded_file = st.file_uploader("Upload an image containing text", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        text = recText(uploaded_file)
        if st.button("Detect"):
            st.image(uploaded_file)
            with st.spinner("Analyzing the image to...🕵️"):
                result = obj.Fake_news_Agent(text)
                output_file = text_to_speech(result.content)
            st.markdown(f"### Result: {result.content}")
            st.audio(output_file,format="audio/wav")
            
if option == "Audio_Input":
    st.title("Speech Recognition ")
    
    @st.cache_resource
    def load_model():
        return whisper.load_model("base")
    
    model = load_model()
    
    uploaded_file = st.file_uploader("Upload an audio file", type=['mp3', 'wav'])
    
    if uploaded_file is not None:
        st.audio(uploaded_file, format="audio/mp3")
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(uploaded_file.read())
            temp_audio_path = temp_audio.name
        
        st.info("Transcribing Audio...")
        result = model.transcribe(temp_audio_path)
        
        
        res = None
        
        if st.button("Detect"):
            with st.spinner("Loading..🔃"):
                res = obj.Fake_news_Agent(result['text'])
                output_file = text_to_speech(res.content)
            st.markdown(f"### Result: {res.content}")
            st.audio(output_file, format="audio/wav")   
                
if st.sidebar.button("Logout"):
    
    st.markdown('<meta http-equiv="refresh" content="0;URL=http://127.0.0.1:5500/index.html">', unsafe_allow_html=True)
        
