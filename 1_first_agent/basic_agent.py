from dotenv import load_dotenv
import os

from langchain.agents import create_agent
from langchain_community.utilities import SerpAPIWrapper
from langchain_groq import ChatGroq
from langchain.tools import tool

load_dotenv()

# llm = ChatGroq(model="qwen/qwen3-32b", temperature = 0)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature = 0)


# Fetch SerpApi key 
serpapi_key = os.getenv("SERPAPI_API_KEY")
# print(serpapi_key)

serp = SerpAPIWrapper(
    serpapi_api_key = serpapi_key,
    params={
        "tbm":"nws",    # Search in Google News 
        "tbs":"qdr:d",  #Past day(24 hours)
    },
)

@tool
def search_news(query: str) -> str:
    """
    Search last-24h Google News via SerpAPI.
    Returns news results with URLs.
    """
    return serp.run(query)

agent = create_agent(
    model=llm,
    tools=[search_news],
    system_prompt="You are a news reporter who reports news using a simple language"
    "in 3 lines along with date of news"
)

result = agent.invoke(
    {"messages": [
        {
            "role": "user", 
            "content": (
                "Tell me the most latest breaking political news from USA "
                "along with the web url of news "
            )
        }
      ]
    }
)

print(result["messages"][-1].content)

# SerpAPIkey is used as a tool, which allows user to search for the news
# In the system_prompt we give instructions to llm to work according to situation
