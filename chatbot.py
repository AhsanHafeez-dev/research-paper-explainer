from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate,load_prompt

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
chatHistory=[
    SystemMessage("You are an ai assistant")
]
while(True):
    user_input=input("You : ")
    chatHistory.append(HumanMessage(user_input))
    if(user_input=="exit"):
        break
    result=model.invoke(chatHistory)
    chatHistory.append(AIMessage(result.content))
    print(f"AI : {result.content}")

print(chatHistory)    