from phi.agent import Agent
from phi.tools.duckduckgo import DuckDuckGo
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq 
import streamlit as st 



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

        return Fake_Agent.print_response(f"Check whether this is real or fake:{news}")
        
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
        
        return News_agent.print_response(f"Generate news based on: {news_title}")
        

obj = My_Agent()

text_detect = input("Enter a news for detect:")

obj.Fake_news_Agent(text_detect)

news = input("Enter a news to fetch:")
obj.news_generator(news)

