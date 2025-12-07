from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

model=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

messages=[
    SystemMessage(content="You are helpful assistant"),
    HumanMessage(content="tell me about langchain")
]
response=AIMessage(model.invoke(messages).content)
messages.append(response)
print(messages)


