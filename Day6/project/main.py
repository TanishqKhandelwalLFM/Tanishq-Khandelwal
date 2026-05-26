from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import TextLoader
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_chroma import Chroma
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.messages import AIMessage,SystemMessage,HumanMessage

load_dotenv()

embedding_model = MistralAIEmbeddings(
    model="mistral-embed",
)

vector_store = Chroma(
    persist_directory = 'chroma-db',
    embedding_function = embedding_model
)

retriever = vector_store.as_retriever(
    search_type = 'mmr',
    search_kwargs = {
        'k' : 4,
        'fetch_k' : 10,
        'lambda_mult' : 0.5
    }
)


history = [
    
]

model = init_chat_model(model='mistral-small-2506')

prompt = ChatPromptTemplate.from_messages([
    ("system" , 
    '''
        You are a syllabus assistant.

        Use only the given context to answer the question , if the answer is not present in the context , say : "I could not find answer is not present in the pdf"

        Your task is to answer questions using only the retrieved syllabus context provided by the retrieval system.

        Rules:
        - Use retrieved information as the source of truth.
        - Do not generate information that is not present in the retrieved content.
        - Keep explanations clear and concise.
        - Explain topics in student-friendly language.
        - Organize responses properly when multiple topics are present.
        - If information is missing, clearly state that the available context is insufficient.
        - Avoid unrelated details.
        - Stay focused on syllabus topics, units, descriptions, and academic content only.
    
    '''
    ),
    (
        "human",
        '''
            history : {history}
            context : {context}
            question : {question}
        '''
    )
])


print("-------- RAG ENGINE ACTIVATED -------")
print()

print("press 0 to exit")
print()
while True: 
    query = input("you : ")

    if query == '0':
        break


    docs = retriever.invoke(query)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    final_prompt = prompt.invoke(
        {
            "context" : context,
            "question" : query,
            "history" : history
        }
    )

    res = model.invoke(final_prompt)

    print()
    print()
    print(f"bot : {res.content}")
    history.append(HumanMessage(content=query))
    history.append(AIMessage(content=res.content))
    print()
    print()
