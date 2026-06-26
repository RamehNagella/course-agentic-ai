from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()

llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)
# llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)

@tool
def inventory_tool(product_name:str)->str:
  """Check inventory availability for a given product name."""
  print(f"TOOL CALLED for:{product_name}")
  inventory ={
    "iPhone 15": "In Stock: Available Itms = 2",
    "AirPods Pro": "Out of Stock: Available Items = 0",
    "MacBook Air M3": "In Stock: Available Items = 5"
  }
  return inventory.get(product_name, "Product not found in inventory.")

agent = create_agent(
  model=llm,
  tools=[inventory_tool],
  system_prompt="""
  You are an inventory assistant.

  - If a question is out of scope which is not related to inventory then just say 
  "sorry, I can't assist with that." No need to say anything else.

  When a user asks about a product, use the inventory_tool to fetch the inventory data.

  - Always call the inventory_tool with full product name.
  - inventory_tool will reuturn a dictionary which you need to parse to extract stock
  status, inventory items etc.

  - Respond with clear, concise information including:
    1.The stock status (e.g. "In Stock", "Out of stock")
    2.The number of available items(if applicable)
  - IF the product is not found, say: "The product is not available in our inventory."

  Never guess or hallucinate information. Do not respond unless the inventory_tool is called.

  Keep your response short and informative.

  """
)

def run(question: str)->str:
  result = agent.invoke({"messages": [HumanMessage(content=question)]})
  return result["messages"][-1].content

if __name__ == "__main__":
  # question = "Do you have any airpods pro in stock?"
  # question = "I want to travel to moon, how much will it cost?"
  # question = "What is the inventory status of iphone 15?"
  question = "What are available phones in samsung company?"
  print(run(question))



# 1. What is HumanMessage()?
# HumanMessage is a message wrapper that tells the LLM who is speaking. LangChain uses a structured message system to represent a conversation:
# ClassRepresentsExampleHumanMessageUser's input"Do you have iPhone 15?"AIMessageLLM's response"Yes, it is in stock."SystemMessageSystem instructions"You are an inventory assistant."ToolMessageTool's output{"iPhone 15": "In Stock"}
# So when you write:
# python{"messages": [HumanMessage(content=question)]}
# You are telling the agent — "this message is coming from the human/user".

# 2. Why is it used in THIS agent?
# Your agent uses LangGraph-style message passing (which create_react_agent follows internally). It expects input in this format:
# python# ✅ Correct — agent understands who is speaking
# agent.invoke({"messages": [HumanMessage(content="Do you have iPhone 15?")]})

# # ❌ Wrong — agent won't know the role of this message
# agent.invoke({"messages": ["Do you have iPhone 15?"]})
# The agent internally builds a conversation like this:
# HumanMessage  → "Do you have iPhone 15?"
# AIMessage     → "Let me check..." (calls inventory_tool)
# ToolMessage   → "In Stock: Available Items = 2"
# AIMessage     → "iPhone 15 is In Stock with 2 items available."
# Each step needs proper role labels — that's why HumanMessage is necessary.

# 3. When should you use HumanMessage?
# SituationUse it?Sending user input to an agent✅ YesBuilding multi-turn conversations✅ YesPassing history of chat to LLM✅ YesSimple llm.invoke("some text")❌ Not needed
# Multi-turn example (where it really shines):
# pythonmessages = [
#     HumanMessage(content="Do you have iPhone 15?"),
#     AIMessage(content="Yes, iPhone 15 is In Stock with 2 items."),
#     HumanMessage(content="What about AirPods Pro?"),  # follow-up
# ]
# agent.invoke({"messages": messages})

# 4. What should you learn from this agent as a beginner?
# Here are the key concepts this single file teaches you:
# ① Tool Creation with @tool
# python@tool
# def inventory_tool(product_name: str) -> str:
#     """Check inventory availability."""  # ← LLM reads this docstring to decide when to call
# The docstring is critical — the LLM uses it to decide when to call the tool.
# ② Agent = LLM + Tools + Loop
# User Input → LLM decides → calls tool → gets result → LLM responds
# The agent automatically loops until it has enough info to answer.
# ③ System Prompt controls behavior

# Your system prompt defines:

# What the agent can/cannot do
# How it should respond
# Guardrails ("Never guess or hallucinate")

# ④ Message structure

# HumanMessage → AIMessage → ToolMessage → AIMessage is the core flow of every agent.
# ⑤ result["messages"][-1].content
# pythonreturn result["messages"][-1].content
# The agent returns ALL messages in the conversation history. You take [-1] (last one) because that's the final answer from the LLM.
# */