from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model="qwen/qwen3-32b", temperature=0)
# llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

@tool
def get_customer_info_tool(customer_name: str)->str:
  """
  Fetches customer information based on a given customer name.
  This is a placeholder function that simulates retreiving ustomer data.
  In a real implementation, this would query a database or external API.
  """
  # Simulated customer data   
  customers = {

    "Krishna": {
      "email": "krishna_001@abc.com",
      "credit_card": "4111-1111-1111-1111",   # Visa test card ✓ Luhn valid
      "name": "Krishna",
      "loyalty_status": "Gold"
      },
      "Alice": {
        "email": "alice_002@abc.com",
        "credit_card": "5500-0000-0000-0004",   # Mastercard test card ✓ Luhn valid
        "name": "Alice",
        "loyalty_status": "Silver"
      },
      "Bob": {
          "email": "bob2009@xyz.com",
          "credit_card": "6011-1111-1111-1117",   # Discover test card ✓ Luhn valid
          "name": "Bob",
          "loyalty_status": "Bronze"
      },
  }
  
  return customers.get(customer_name, "Customer not found.")


agent = create_agent(

  system_prompt="""You are a customer service assistant.
  You have access to the get_customer_info_tool which provides customer information based on the customer's name.
  When a user asks for information about a customer, use the get_customer_info_tool to retrieve the data.

  """,
  model=llm,
  tools=[get_customer_info_tool]
)

result = agent.invoke({
  "messages":[{
    "role":"user",
    "content":"Give me information about customer Krishna"
  }]
})

print(result["messages"][-1].content)

# Here is the information for customer **Krishna**:

# - **Email**: krishna_001@abc.com  
# - **Credit Card**: 4111-1111-1111-1111 (last 4 digits: 1111)  
# - **Loyalty Status**: Gold  

# Let me know if you need further details!

# print(result)
pythonresult_1 = {
  'messages': [

    # ── 1. HumanMessage ──────────────────────────────────────────
    {
      'type': 'HumanMessage',
      'content': 'Give me information about customer Krishna',
      'additional_kwargs': {},
      'response_metadata': {},
      'id': '23894e31-ac65-4bbe-b551-bdda078f426e'
    },

    # ── 2. AIMessage (tool call decision) ────────────────────────
    {
      'type': 'AIMessage',
      'content': '',
      'additional_kwargs': {
        'reasoning_content': 'We need to use the get_customer_info_tool.',
        'tool_calls': [
          {
            'id': 'fc_7057a0b7-d693-419c-a902-e0d821c6874c',
            'function': {
              'arguments': '{"customer_name":"Krishna"}',
              'name': 'get_customer_info_tool'
            },
            'type': 'function'
          }
        ]
      },
      'response_metadata': {
        'token_usage': {
          'completion_tokens': 38,
          'prompt_tokens': 215,
          'total_tokens': 253,
          'completion_time': 0.038964592,
          'completion_tokens_details': {
            'reasoning_tokens': 11
          },
          'prompt_time': 0.010430007,
          'prompt_tokens_details': None,
          'queue_time': 0.31176021,
          'total_time': 0.049394599
        },
        'model_name': 'openai/gpt-oss-20b',
        'system_fingerprint': 'fp_92d51d08e5',
        'service_tier': 'on_demand',
        'finish_reason': 'tool_calls',
        'logprobs': None,
        'model_provider': 'groq'
      },
      'id': 'lc_run--019efed1-9718-7650-ba41-46f823c4d089-0',
      'tool_calls': [
        {
          'name': 'get_customer_info_tool',
          'args': {'customer_name': 'Krishna'},
          'id': 'fc_7057a0b7-d693-419c-a902-e0d821c6874c',
          'type': 'tool_call'
        }
      ],
      'invalid_tool_calls': [],
      'usage_metadata': {
        'input_tokens': 215,
        'output_tokens': 38,
        'total_tokens': 253,
        'output_token_details': {
          'reasoning': 11
        }
      }
    },

    # ── 3. ToolMessage (tool result) ──────────────────────────────
    {
      'type': 'ToolMessage',
      'content': '{"email": "krishna_001@abc.com", "credit_card": "4111-1111-1111-1111", "name": "Krishna", "loyalty_status": "Gold"}',
      'name': 'get_customer_info_tool',
      'id': 'd22c839e-a391-4267-a3e7-77f09f1f3e8b',
      'tool_call_id': 'fc_7057a0b7-d693-419c-a902-e0d821c6874c'
    },

    # ── 4. AIMessage (final response to user) ────────────────────
    {
      'type': 'AIMessage',
      'content': (
        "Here's the information we have on Krishna:\n\n"
        "- **Name:** Krishna\n"
        "- **Email:** krishna_001@abc.com\n"
        "- **Credit Card:** 4111-1111-1111-1111\n"
        "- **Loyalty Status:** Gold\n\n"
        "Let me know if you need anything else!"
      ),
      'additional_kwargs': {
        'reasoning_content': 'We have retrieved customer info. We should respond with that info.'
      },
      'response_metadata': {
        'token_usage': {
          'completion_tokens': 86,
          'prompt_tokens': 291,
          'total_tokens': 377,
          'completion_time': 0.090634577,
          'completion_tokens_details': {
            'reasoning_tokens': 14
          },
          'prompt_time': 0.021231188,
          'prompt_tokens_details': None,
          'queue_time': 0.281601692,
          'total_time': 0.111865765
        },
        'model_name': 'openai/gpt-oss-20b',
        'system_fingerprint': 'fp_f102a3179c',
        'service_tier': 'on_demand',
        'finish_reason': 'stop',
        'logprobs': None,
        'model_provider': 'groq'
      },
      'id': 'lc_run--019efed1-9c64-73d1-83c6-4dac674e7db2-0',
      'tool_calls': [],
      'invalid_tool_calls': [],
      'usage_metadata': {
        'input_tokens': 291,
        'output_tokens': 86,
        'total_tokens': 377,
        'output_token_details': {
          'reasoning': 14
        }
      }
    }

  ]
}
# The 4 messages in order are:

# HumanMessage — user's question
# AIMessage — LLM decides to call the tool (finish_reason: 'tool_calls')
# ToolMessage — tool returns the customer data
# AIMessage — LLM formats and returns the final answer to user (finish_reason: 'stop')