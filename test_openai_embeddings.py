import os
from dotenv import load_dotenv
from openai import OpenAI


# 1. Load environment variables from .env
load_dotenv()

# 2. Create OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://api.euron.one/api/v1/euri"
)

# 3. Prepare sample sentences
sentences = [
    "Django is a Python web framework.",
    "Django helps developers build web applications.",
    "PostgreSQL is a relational database."
]

# 4. Generate embeddings
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=sentences
)

# 5. Extract embedding vectors
embeddings = [
    item.embedding for item in response.data
]

# 6. Display results
print("Number of sentences:", len(sentences))

print("Number of embeddings:", len(embeddings))

print("Dimensions of first embedding:", len(embeddings[0]))

print("\nFirst embedding:")
print(embeddings[0])

print("\nAPI tokens used:", response.usage.total_tokens)
