import os
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from ecommbot.ingest import ingestdata

# ✅ Set your FREE Gemini API Key (from makersuite)
os.environ["GOOGLE_API_KEY"] = "AIzaSyANb7rTgq8DNLr-DQsKJ09AFqbDr0IGErw"

def generation(vstore):
    retriever = vstore.as_retriever(search_kwargs={"k": 3})

    PRODUCT_BOT_TEMPLATE = """
    Your ecommercebot is an expert in product recommendations and customer queries.
    It analyzes product titles and reviews to provide accurate and helpful responses.
    Stay relevant to the product context and be concise.

    CONTEXT:
    {context}

    QUESTION: {question}

    YOUR ANSWER:
    """

    prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

    # ✅ Use correct free model with extra param for compatibility
    llm = ChatGoogleGenerativeAI(
        model="gemini-pro", 
        convert_system_message_to_human=True  # important for free use
    )

    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

if __name__ == '__main__':
    vstore = ingestdata("done")
    chain = generation(vstore)
    print(chain.invoke("can you tell me the best bluetooth buds?"))
