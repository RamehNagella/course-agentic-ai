# code for COSINE SIMILARITY
# In this code we will check two statements how similar to each other
# Before comparing two statments we will convert them into embedding vectors
# using sentance transformer

from sentence_transformers import SentenceTransformer
import numpy as np
import logging
from dotenv import load_dotenv
load_dotenv()

logging.getLogger("transformers").setLevel(logging.ERROR)

_model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_similarity(sentence1: str, sentence2: str) -> float:
  embeddings = _model.encode([sentence1, sentence2])
  a, b = embeddings[0], embeddings[1]
  similarity = np.dot(a,b)/(np.linalg.norm(a)* np.linalg.norm(b))
  return float(np.clip(similarity, 0.0,1.0))

if __name__ == "__main__":
  
  pairs = [
    ("The cat sat on the mat.","A feline rested on the rug."),
    ("The cat sat on the mat.", "The dog barked at the mailman."),
    ("Python is great.", "I love programming in Python.")
  ]

  for s1, s2 in pairs:
    sim = cosine_similarity(s1, s2)
    print(f"{sim:.4f} | \"{s1}\" vs \"{s2}\"")

# here why we doing this, bcoz for agentic evaluation we are
# using cosine similarity as a method to evaluate expected response
# and actual response and to compar them 