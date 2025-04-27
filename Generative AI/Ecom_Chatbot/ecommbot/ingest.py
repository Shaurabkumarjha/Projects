from langchain_astradb import AstraDBVectorStore
from dotenv import load_dotenv
import os
from ecommbot.data_converter import dataconveter
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")

# ✅ Using sentence-transformers for embeddings instead of OpenAI
embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

def ingestdata(status):
    vstore = AstraDBVectorStore(
        embedding=embedding,
        collection_name="chatbotecomm",
        api_endpoint=ASTRA_DB_API_ENDPOINT,
        token=ASTRA_DB_APPLICATION_TOKEN,
        namespace=ASTRA_DB_KEYSPACE,
    )

    if status is None:
        docs = dataconveter()
        inserted_ids = vstore.add_documents(docs)
        return vstore, inserted_ids
    else:
        return vstore

if __name__ == '__main__':
    vstore_result = ingestdata(None)

    if isinstance(vstore_result, tuple):
        vstore, inserted_ids = vstore_result
        print(f"\nInserted {len(inserted_ids)} documents.")
    else:
        vstore = vstore_result

    results = vstore.similarity_search("can you tell me the low budget sound basshead.")
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")
