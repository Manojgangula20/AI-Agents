from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai

import os
from dotenv import load_dotenv
load_dotenv()
openai.api_key =os.getenv('OPENAI_API_KEY') 


## web search agent
web_search_agent=Agent(
    name = 'Web Search Agent',
    role = 'Search the web for the information',
    model = Groq(id='llama-3.3-70b-versatile',),
    tools = [DuckDuckGo()],
    instructions = ["Always include sources"],
    show_tools_calls=True,
    markdown=True,
)

## financial agent
finance_agent=Agent(
    name = 'Financial Agent',
    role = 'Analyze financial data and provide insights',
    model = Groq(id='llama-3.3-70b-versatile'),
    tools=[
        YFinanceTools(stock_price=True,analyst_recommendations=True,stock_fundamentals=True,
                      company_news=True),
        ], # add web search agent as a tool to access internet
    instructions=["Provide detailed analysis of the stock market using tables"],
    show_tools_calls=True,
    markdown=True,
)


# run the agent with a query
multi_ai_agent=Agent(
    model=Groq(id='llama-3.1-70b-versatile'),
    team=[web_search_agent,finance_agent],
    instructions=["Always include sources","Use table to display the data"],  
    show_tools_calls=True,
    markdown=True,
)

multi_ai_agent.print_response("Summarize analyst recommendation and share the latest news for NVDA",stream=True)
