from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel,RunnableLambda

short_prompt = ChatPromptTemplate.from_template(
    "Explain about {topic} in 50 words "
)

detailed_prompt = ChatPromptTemplate.from_template(
    "Explain about {topic} in 250 words "
)

model = init_chat_model("mistral-small-2506")

parser = StrOutputParser()

chain = RunnableParallel({
    "short" : RunnableLambda(lambda x : x['short']) |  short_prompt | model | parser,
    "detailed" : RunnableLambda(lambda x : x['detailed']) | detailed_prompt | model | parser
})

result = chain.invoke({
   "short" : {"topic" : "virat kohli"},
   "detailed" : {"topic" : "rohit sharma"}
})

print(f"short : {result['short']}")
print()
print(f"detailed : {result['detailed']}")
