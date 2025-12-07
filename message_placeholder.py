from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pprint import pprint
l=[]
with open("temp.txt","r") as f:
    l=f.read().split("\n")

chats=ChatPromptTemplate(
    [
        ('system','hi'),
        MessagesPlaceholder(variable_name='chat_history'),
        ('human','{query}')
        
        
    ]
    )

prompt=chats.invoke({'chat_history':l,'query':'where is my slip'})
pprint(prompt)
    