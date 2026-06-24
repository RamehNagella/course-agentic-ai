from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
import yfinance as yf



load_dotenv()

llm = ChatGroq(model="qwen/qwen3-32b", temperature = 0)

@tool 
def get_stock_price(ticker: str)-> str:
  """
  Get the current stock price for a given ticker symbol
  """
  stock = yf.Ticker(ticker)
  price = stock.info.get("currentPrice")
  return price

@tool
def get_market_valuation_of_private_company(compnay_name:str)-> str:
  """Return the market valuation of a private company in billion USD.This 
  is a placeholder function 
  """
  #In a real implementation, you would use an API response to get this information.
  # For demonstration purposes, we will return fixed value.
  compnay_valuations = {
    "SpaceX":137.0, # Example valuation in billion USD
    "Stripe":95.0, # Example valuation in billion USD
    "Airbnb":100.0, # Example valuation in billion USD
  }
  return compnay_valuations.get(compnay_name, 0.0) # Example valuation in USD

agent = create_agent(
    model=llm,
    tools=[get_stock_price, get_market_valuation_of_private_company],
    system_prompt="You are a finance agent"
)

result = agent.invoke(
    {"messages": [
        {
            "role": "user", 
            "content": (
                # "What is the valuation of SpaceX?"
                # "What is the stock price of Tesla?"
                "compare tesl stock price and Spacex stock price? and give me in table format?"
            )
        }
      ]
    }
)

print(result["messages"][-1].content)


# Summary: 

# 1. @tool decorator — turning functions into agent tools

# @tool wraps a normal Python function so the agent can call it
# The docstring is critical — the agent reads it to decide when to use the tool
# Type hints (str, float) tell the agent what input to pass


# 2. Two types of tools in one agent

# get_stock_price → calls a real external API (Yahoo Finance)
# get_market_valuation_of_private_company → uses hardcoded/mock data
# Agents can mix real and dummy tools — useful for prototyping


# 3. Agent decides which tool to use — you don't

# You just ask "What is the valuation of SpaceX?"
# The agent figures out SpaceX is private → calls get_market_valuation_of_private_company
# If you asked about Tesla, it would call get_stock_price instead
# This reasoning + tool selection is the core of what makes it an "agent"


# 4. system_prompt sets the agent's role/persona
# pythonsystem_prompt="You are a finance agent"

# Shapes how the agent responds, what tone it uses, and what it focuses on
# Short here, but in production you'd make it more detailed


# 5. messages format — how you talk to the agent
# python{"role": "user", "content": "What is the valuation of SpaceX?"}

# Standard chat format (same as OpenAI/Groq API)
# role can be "user", "assistant", or "system"
# Multi-turn conversations = just append more messages to the list


# 6. There is a bug in your code — spot it as a learner
# python# ❌ Wrong — yf.ticker() should be yf.Ticker() (capital T)
# stock = yf.ticker(ticker)

# # ✅ Correct
# stock = yf.Ticker(ticker)
# This is a common mistake — yfinance is case-sensitive.

# 7. Agent returns a list of messages — extract the last one
# pythonresult["messages"][-1].content

# The result contains the full conversation history (user → tool call → tool result → final answer)
# [-1] gets the final AI response
# Good habit: always use [-1] to get the answer


# 8. LLM is just the brain — tools are the hands
# pythonllm = ChatGroq(model="qwen/qwen3-32b", temperature=0)

# temperature=0 → deterministic, no creativity — good for factual finance tasks
# The LLM reasons; the tools act
# You can swap any LLM (OpenAI, Gemini, etc.) without changing your tools


# What to try next as a learner

# Add a 3rd tool like get_news(ticker) using SerpAPI (you already know this!)
# Ask multi-part questions: "Compare Tesla stock price vs SpaceX valuation"
# Add verbose=True to create_agent to see the agent's reasoning steps