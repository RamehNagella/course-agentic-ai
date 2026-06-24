from dotenv import load_dotenv

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.tools import tool



load_dotenv()

llm = ChatGroq(model="qwen/qwen3-32b", temperature = 0)


agent = create_agent(
    model=llm,
    tools=[],
    system_prompt="""
    You are an advanced reasoning assistant.
    List out all the steps you carry to reason with numbers
    If you're using any formula, it should not be in Latex but plain formulas
    """
)

result = agent.invoke(
    {"messages": [
        {
            "role": "user", 
            "content": "How much time will it take for a chetah to travel from New Delhi to Mumbai?"
        }
      ]
    }
)

print(result["messages"][-1].content)
