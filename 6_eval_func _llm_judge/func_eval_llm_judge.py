import json

from langsmith import Client, evaluate, traceable
from inventory_agent import run 
from langchain.tools import tool
from utils import cosine_similarity
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os
load_dotenv()

judge = ChatGroq(model="openai/gpt-oss-20b")

# print("langsmith_key: ", os.getenv("LANGSMITH_API_KEY"))

@traceable
def target(inputs: dict)->dict:
  question = inputs["question"]
  answer = run(question)
  print(">>",question, answer)
  return {"answer": answer}

client = Client()

dataset_name = "inventorydata_llm_judge"   #test_suite (table which shows comparison between actual and reference)

if not client.has_dataset(dataset_name = dataset_name):
  client.create_dataset(dataset_name=dataset_name)

  client.create_examples(
    dataset_name = dataset_name,
    examples = [
      {
        'inputs':{"question": "What is the stock status of iPhone 15?"},
        'outputs':{"answer":"The iPhone 15 is currently in stock with 2 units available."}
      },
      {
        "inputs": {"question": "Is AirPods Pro available?"},
        "outputs": {"answer": "The AirPods Pro is currently out of stock. There are 0 available items."},
      },
      {
        "inputs": {"question": "How many iPhone 15 units are available?"},
        "outputs": {"answer": "The iPhone 15 is currently in stock with 2 units available."},
      },
      {
        "inputs": {"question": "Do you have Samsung Galaxy S23?"},
        "outputs": {"answer": "The product is not available in our inventory"},
      },
      {
        "inputs": {"question": "Can you tell me the recipe of Vada Pav?"},
        "outputs": {"answer": "Sorry, I can’t assist with that"},
      }
    ]
  )

JUDG_PROMPT = """You are a helpful and precise assistant for 
  the correctness of the answer.

  Question: {question}

  Expected Answer:{expected}

  Actual Answer: {actual}

  Please compare the actual answer with the expected answer and
  give a score between 0 and 1 based on the correctness.

  Retrun ONLY valid JSON like:
  {{"score": <number>}}.
"""

def llm_judge(example, run):
  print("e.g.", example,"\n run: ", run)
  question= example.inputs["question"]
  expected = example.outputs["answer"]
  actual = run.outputs["answer"]
  # print('e', expected, actual)
  msg = JUDG_PROMPT.format(question=question, expected=expected, actual=actual)
  resp = judge.invoke(msg).content
  
  data = json.loads(resp)
  score = float(data["score"])

  print("llm judgement data: ", data)

  return {
    "key": "llm_judge",
    "score":score,
  }

evaluate(
  target,
  client=client,
  data=dataset_name,
  evaluators=[llm_judge],
  experiment_prefix="inventory_agent_evaluation_llm_judge"
)



# /*  Output:

# 0it [00:00, ?it/s]TOOL CALLED for:Samsung Galaxy S23
# >> Do you have Samsung Galaxy S23? The product is not available in our inventory.
# e.g. dataset_id=UUID('f073a69b-84ec-4163-8727-b837e58dd1d7') inputs={'question': 'Do you have Samsung Galaxy S23?'} outputs={'answer': 'The product is not available in our inventory'} metadata={'dataset_split': ['base']} id=UUID('273328b8-289f-4ecc-877c-8cf78fb71b4b') created_at=datetime.datetime(2026, 6, 25, 10, 30, 7, 562259, tzinfo=TzInfo(0)) modified_at=datetime.datetime(2026, 6, 25, 10, 30, 7, 562259, tzinfo=TzInfo(0)) source_run_id=None attachments={} 
#  run:  id=UUID('019efe73-fb32-7502-b4c7-3f94e66fcba6') name='target' start_time=datetime.datetime(2026, 6, 25, 11, 4, 34, 354913, tzinfo=datetime.timezone.utc) run_type='chain' end_time=datetime.datetime(2026, 6, 25, 11, 4, 35, 547225, tzinfo=datetime.timezone.utc) extra={'metadata': {'revision_id': '3b72584-dirty', '__ls_runner': 'py_sdk_evaluate', 'num_repetitions': 1, 'example_version': '2026-06-25T10:30:07.562259+00:00', 'ls_method': 'traceable'}, 'runtime': {'sdk': 'langsmith-py', 'sdk_version': '0.9.1', 'library': 'langsmith', 'platform': 'Linux-6.17.0-35-generic-x86_64-with-glibc2.39', 'runtime': 'python', 'py_implementation': 'CPython', 'runtime_version': '3.12.3', 'langchain_version': '1.2.15', 'langchain_core_version': '1.3.0'}} error=None serialized=None events=[] inputs={'inputs': {'question': 'Do you have Samsung Galaxy S23?'}} outputs={'answer': 'The product is not available in our inventory.'} reference_example_id=UUID('273328b8-289f-4ecc-877c-8cf78fb71b4b') parent_run_id=None tags=[] attachments={} parent_run=None parent_dotted_order=None child_runs=[RunTree(id=019efe73-fb3c-7941-8e00-b518fc94dc1d, name='LangGraph', run_type='chain', dotted_order='20260625T110434354913Z019efe73-fb32-7502-b4c7-3f94e66fcba6.20260625T110434364061Z019efe73-fb3c-7941-8e00-b518fc94dc1d')] session_name='inventory_agent_evaluation_llm_judge-ced0323c' session_id=None ls_client=Client (API URL: https://api.smith.langchain.com) dotted_order='20260625T110434354913Z019efe73-fb32-7502-b4c7-3f94e66fcba6' trace_id=UUID('019efe73-fb32-7502-b4c7-3f94e66fcba6') dangerously_allow_filesystem=False replicas=[]
# llm judgement data:  {'score': 0.99}

# 1it [00:02,  2.33s/it]>> Can you tell me the recipe of Vada Pav? Sorry, I can't assist with that.
# e.g. dataset_id=UUID('f073a69b-84ec-4163-8727-b837e58dd1d7') inputs={'question': 'Can you tell me the recipe of Vada Pav?'} outputs={'answer': 'Sorry, I can’t assist with that'} metadata={'dataset_split': ['base']} id=UUID('51e3142a-18ec-4b4e-b3c9-593346c7a9a7') created_at=datetime.datetime(2026, 6, 25, 10, 30, 7, 562259, tzinfo=TzInfo(0)) modified_at=datetime.datetime(2026, 6, 25, 10, 30, 7, 562259, tzinfo=TzInfo(0)) source_run_id=None attachments={} 
#  run:  id=UUID('019efe74-0452-72c0-b115-2f0b92bf63c4') name='target' start_time=datetime.datetime(2026, 6, 25, 11, 4, 36, 690904, tzinfo=datetime.timezone.utc) run_type='chain' end_time=datetime.datetime(2026, 6, 25, 11, 4, 37, 132438, tzinfo=datetime.timezone.utc) extra={'metadata': {'revision_id': '3b72584-dirty', '__ls_runner': 'py_sdk_evaluate', 'num_repetitions': 1, 'example_version': '2026-06-25T10:30:07.562259+00:00', 'ls_method': 'traceable'}, 'runtime': {'sdk': 'langsmith-py', 'sdk_version': '0.9.1', 'library': 'langsmith', 'platform': 'Linux-6.17.0-35-generic-x86_64-with-glibc2.39', 'runtime': 'python', 'py_implementation': 'CPython', 'runtime_version': '3.12.3', 'langchain_version': '1.2.15', 'langchain_core_version': '1.3.0'}} error=None serialized=None events=[] inputs={'inputs': {'question': 'Can you tell me the recipe of Vada Pav?'}} outputs={'answer': "Sorry, I can't assist with that."} reference_example_id=UUID('51e3142a-18ec-4b4e-b3c9-593346c7a9a7') parent_run_id=None tags=[] attachments={} parent_run=None parent_dotted_order=None child_runs=[RunTree(id=019efe74-0456-7d63-acc9-3fb1cff32a6e, name='LangGraph', run_type='chain', dotted_order='20260625T110436690904Z019efe74-0452-72c0-b115-2f0b92bf63c4.20260625T110436694096Z019efe74-0456-7d63-acc9-3fb1cff32a6e')] session_name='inventory_agent_evaluation_llm_judge-ced0323c' session_id=None ls_client=Client (API URL: https://api.smith.langchain.com) dotted_order='20260625T110436690904Z019efe74-0452-72c0-b115-2f0b92bf63c4' trace_id=UUID('019efe74-0452-72c0-b115-2f0b92bf63c4') dangerously_allow_filesystem=False replicas=[]
# llm judgement data:  {'score': 0.9}

# 2it [00:03,  1.74s/it]TOOL CALLED for:iPhone 15
# >> How many iPhone 15 units are available? The iPhone 15 is in stock with 2 units available.
# e.g. dataset_id=UUID('f073a69b-84ec-4163-8727-b837e58dd1d7') inputs={'question': 'How many iPhone 15 units are available?'} outputs={'answer': 'The iPhone 15 is currently in stock with 2 units available.'} metadata={'dataset_split': ['base']} id=UUID('7c5e3bc9-9778-43d8-ab9a-f547bf48cdc0') created_at=datetime.datetime(2026, 6, 25, 10, 30, 7, 562259, tzinfo=TzInfo(0)) modified_at=datetime.datetime(2026, 6, 25, 10, 30, 7, 562259, tzinfo=TzInfo(0)) source_run_id=None attachments={} 
#  run:  id=UUID('019efe74-0980-7e23-9ab7-6304c3846757') name='target' start_time=datetime.datetime(2026, 6, 25, 11, 4, 38, 16321, tzinfo=datetime.timezone.utc) run_type='chain' end_time=datetime.datetime(2026, 6, 25, 11, 4, 40, 258954, tzinfo=datetime.timezone.utc) extra={'metadata': {'revision_id': '3b72584-dirty', '__ls_runner': 'py_sdk_evaluate', 'num_repetitions': 1, 'example_version': '2026-06-25T10:30:07.562259+00:00', 'ls_method': 'traceable'}, 'runtime': {'sdk': 'langsmith-py', 'sdk_version': '0.9.1', 'library': 'langsmith', 'platform': 'Linux-6.17.0-35-generic-x86_64-with-glibc2.39', 'runtime': 'python', 'py_implementation': 'CPython', 'runtime_version': '3.12.3', 'langchain_version': '1.2.15', 'langchain_core_version': '1.3.0'}} error=None serialized=None events=[] inputs={'inputs': {'question': 'How many iPhone 15 units are available?'}} outputs={'answer': 'The iPhone 15 is in stock with 2 units available.'} reference_example_id=UUID('7c5e3bc9-9778-43d8-ab9a-f547bf48cdc0') parent_run_id=None tags=[] attachments={} parent_run=None parent_dotted_order=None child_runs=[RunTree(id=019efe74-0982-7fd1-8b35-42191d4d7181, name='LangGraph', run_type='chain', dotted_order='20260625T110438016321Z019efe74-0980-7e23-9ab7-6304c3846757.20260625T110438018270Z019efe74-0982-7fd1-8b35-42191d4d7181')] session_name='inventory_agent_evaluation_llm_judge-ced0323c' session_id=None ls_client=Client (API URL: https://api.smith.langchain.com) dotted_order='20260625T110438016321Z019efe74-0980-7e23-9ab7-6304c3846757' trace_id=UUID('019efe74-0980-7e23-9ab7-6304c3846757') dangerously_allow_filesystem=False replicas=[]
# llm judgement data:  {'score': 0.97}

# 3it [00:06,  2.34s/it]TOOL CALLED for:AirPods Pro
# >> Is AirPods Pro available? The product "AirPods Pro" is currently **Out of Stock**. Available items: 0.
# e.g. dataset_id=UUID('f073a69b-84ec-4163-8727-b837e58dd1d7') inputs={'question': 'Is AirPods Pro available?'} outputs={'answer': 'The AirPods Pro is currently out of stock. There are 0 available items.'} metadata={'dataset_split': ['base']} id=UUID('de12d603-13be-49de-ac77-2fa5b192eef5') created_at=datetime.datetime(2026, 6, 25, 10, 30, 7, 562259, tzinfo=TzInfo(0)) modified_at=datetime.datetime(2026, 6, 25, 10, 30, 7, 562259, tzinfo=TzInfo(0)) source_run_id=None attachments={} 
#  run:  id=UUID('019efe74-1563-7b50-b8b8-8b023d41b873') name='target' start_time=datetime.datetime(2026, 6, 25, 11, 4, 41, 59563, tzinfo=datetime.timezone.utc) run_type='chain' end_time=datetime.datetime(2026, 6, 25, 11, 4, 43, 216208, tzinfo=datetime.timezone.utc) extra={'metadata': {'revision_id': '3b72584-dirty', '__ls_runner': 'py_sdk_evaluate', 'num_repetitions': 1, 'example_version': '2026-06-25T10:30:07.562259+00:00', 'ls_method': 'traceable'}, 'runtime': {'sdk': 'langsmith-py', 'sdk_version': '0.9.1', 'library': 'langsmith', 'platform': 'Linux-6.17.0-35-generic-x86_64-with-glibc2.39', 'runtime': 'python', 'py_implementation': 'CPython', 'runtime_version': '3.12.3', 'langchain_version': '1.2.15', 'langchain_core_version': '1.3.0'}} error=None serialized=None events=[] inputs={'inputs': {'question': 'Is AirPods Pro available?'}} outputs={'answer': 'The product "AirPods Pro" is currently **Out of Stock**. Available items: 0.'} reference_example_id=UUID('de12d603-13be-49de-ac77-2fa5b192eef5') parent_run_id=None tags=[] attachments={} parent_run=None parent_dotted_order=None child_runs=[RunTree(id=019efe74-1564-71a1-92b6-6469cb971050, name='LangGraph', run_type='chain', dotted_order='20260625T110441059563Z019efe74-1563-7b50-b8b8-8b023d41b873.20260625T110441060346Z019efe74-1564-71a1-92b6-6469cb971050')] session_name='inventory_agent_evaluation_llm_judge-ced0323c' session_id=None ls_client=Client (API URL: https://api.smith.langchain.com) dotted_order='20260625T110441059563Z019efe74-1563-7b50-b8b8-8b023d41b873' trace_id=UUID('019efe74-1563-7b50-b8b8-8b023d41b873') dangerously_allow_filesystem=False replicas=[]
# llm judgement data:  {'score': 0.98}

# 4it [00:09,  2.53s/it]TOOL CALLED for:iPhone 15
# >> What is the stock status of iPhone 15? The iPhone 15 is in stock with 2 available items.
# e.g. dataset_id=UUID('f073a69b-84ec-4163-8727-b837e58dd1d7') inputs={'question': 'What is the stock status of iPhone 15?'} outputs={'answer': 'The iPhone 15 is currently in stock with 2 units available.'} metadata={'dataset_split': ['base']} id=UUID('e5f233f8-e17e-4ee4-8247-112c8bc0760a') created_at=datetime.datetime(2026, 6, 25, 10, 30, 7, 562259, tzinfo=TzInfo(0)) modified_at=datetime.datetime(2026, 6, 25, 10, 30, 7, 562259, tzinfo=TzInfo(0)) source_run_id=None attachments={} 
#  run:  id=UUID('019efe74-2075-7df2-bad2-e579b174e1b7') name='target' start_time=datetime.datetime(2026, 6, 25, 11, 4, 43, 893745, tzinfo=datetime.timezone.utc) run_type='chain' end_time=datetime.datetime(2026, 6, 25, 11, 4, 46, 266320, tzinfo=datetime.timezone.utc) extra={'metadata': {'revision_id': '3b72584-dirty', '__ls_runner': 'py_sdk_evaluate', 'num_repetitions': 1, 'example_version': '2026-06-25T10:30:07.562259+00:00', 'ls_method': 'traceable'}, 'runtime': {'sdk': 'langsmith-py', 'sdk_version': '0.9.1', 'library': 'langsmith', 'platform': 'Linux-6.17.0-35-generic-x86_64-with-glibc2.39', 'runtime': 'python', 'py_implementation': 'CPython', 'runtime_version': '3.12.3', 'langchain_version': '1.2.15', 'langchain_core_version': '1.3.0'}} error=None serialized=None events=[] inputs={'inputs': {'question': 'What is the stock status of iPhone 15?'}} outputs={'answer': 'The iPhone 15 is in stock with 2 available items.'} reference_example_id=UUID('e5f233f8-e17e-4ee4-8247-112c8bc0760a') parent_run_id=None tags=[] attachments={} parent_run=None parent_dotted_order=None child_runs=[RunTree(id=019efe74-2077-7fc1-8971-606611e0ddfa, name='LangGraph', run_type='chain', dotted_order='20260625T110443893745Z019efe74-2075-7df2-bad2-e579b174e1b7.20260625T110443895756Z019efe74-2077-7fc1-8971-606611e0ddfa')] session_name='inventory_agent_evaluation_llm_judge-ced0323c' session_id=None ls_client=Client (API URL: https://api.smith.langchain.com) dotted_order='20260625T110443893745Z019efe74-2075-7df2-bad2-e579b174e1b7' trace_id=UUID('019efe74-2075-7df2-bad2-e579b174e1b7') dangerously_allow_filesystem=False replicas=[]
# llm judgement data:  {'score': 0.9}
# */
