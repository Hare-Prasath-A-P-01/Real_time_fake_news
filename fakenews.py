from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq 
import streamlit as st 
import base64



class My_Agent():
    
    def Fake_news_Agent(self,news):
        
        Fake_Agent = Agent(
            name="FakenewsAgent",
            tools= [DuckDuckGo()],
            model = Groq(id="deepseek-r1-distill-llama-70b"),
            instructions=[
            "You are a fake news detector.",
            "Always analyze multiple sources before deciding.",
            "Provide sources for transparency.",
            "Respond only with 'FAKE' or 'REAL' followed by a brief explanation."
            "Dont access private information based on the government policy",],
            show_tool_calls=False,
            markdown=True
            )

        # return Fake_Agent.print_response(f"Check whether this is real or fake:{news}")
        
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
        
        # return News_agent.print_response(f"Generate news based on: {news_title}")
        
#------------------------------------------------------------------------------
obj = My_Agent()

# text_detect = input("Enter a news for detect:")

# obj.Fake_news_Agent(text_detect)

# news = input("Enter a news to fetch:")
# obj.news_generator(news)
#-------------------------------------------------------------------------------


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
option = st.sidebar.radio(label="Select an Option",options=["Real Time Fake News Detection","Real Time News Search"])



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
    
    
set_sidebar_bg("back.png")
        
if option == "Real Time Fake News Detection":
    st.title("Fake News Detection")
    user_input = st.text_input("Enter the news text:")
    if st.button("Detect"):
        with st.spinner("Analyzing...🕵️"):
            result = obj.Fake_news_Agent(user_input)
        st.markdown(f"### Result: {result.content}")


elif option == "Real Time News Search":
    st.title("Real News Search")
    user_input = st.text_input("Enter topic:")
    if st.button("Search"):
        with st.spinner("Fetching latest news...🔍"):
            result = obj.news_generator(user_input)
        st.markdown(f"### Search Result: {result.content}")
        
