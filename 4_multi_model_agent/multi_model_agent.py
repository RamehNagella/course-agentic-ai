from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(model="qwen/qwen3-32b", temperature = 0)

agent = create_agent(
  model=llm,
  tools=[],
  system_prompt=(
    "You are an image agent"
  )
)

result = agent.invoke(
  {
    "messages":[
      {
        "role":"user",
        "content":"""Which animal in this image? Print the 
        name of the animal from this url: https://www.nycgovparks.org/pagefiles/171/chipmunk-closeup__6193c1a2c7163.jpeg
        """
      }
    ]
  }
)

print(result["messages"][-1].content)
