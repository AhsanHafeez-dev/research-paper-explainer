# from langchain_google_genai import ChatGoogleGenerativeAI
# from dotenv import load_dotenv
# import streamlit as st
# from langchain_core.prompts import PromptTemplate,load_prompt

# load_dotenv()
# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# st.header('Reasearch Tool')

# paper_input = st.selectbox( "Select Research Paper Name", ["Attention Is All You Need", "BERT: Pre-training of Deep Bidirectional Transformers", "GPT-3: Language Models are Few-Shot Learners", "Diffusion Models Beat GANs on Image Synthesis"] )

# style_input = st.selectbox( "Select Explanation Style", ["Beginner-Friendly", "Technical", "Code-Oriented", "Mathematical"] ) 

# length_input = st.selectbox( "Select Explanation Length", ["Short (1-2 paragraphs)", "Medium (3-5 paragraphs)", "Long (detailed explanation)"] )

# template = load_prompt('template.json')



# if st.button('Summarize'):
#     chain = template | model
#     result = chain.invoke({
#         'paper_input':paper_input,
#         'style_input':style_input,
#         'length_input':length_input
#     })
#     st.write(result.content)

import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage
import uuid
import PyPDF2
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#*********************************** utility functions ********************************************************************************************************

def generate_thread_id():
    thread_id= uuid.uuid4()
    return thread_id

def extract_text_from_file(file):
    """Reads text content from uploaded file, supporting PDF and TXT."""
    text = ""
    if file.name.lower().endswith(".pdf"):
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    elif file.name.lower().endswith((".jpg", ".jpeg", ".png")):
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
    elif file.name.lower().endswith(".txt"):
        text = file.read().decode("utf-8", errors="ignore")
    else:
        text = "Unsupported file format. Please upload a .pdf or .txt file."
    return text

def reset_chat():
    thread_id= generate_thread_id()
    st.session_state["thread_id"]= thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"]= []

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config= {"configurable": {"thread_id": thread_id}}).values["messages"]

#*********************************** session setup *************************************************************************************************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if "file" not in st.session_state:
    st.session_state["file"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"]= generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"]= []

add_thread(st.session_state["thread_id"])

# st.session_state -> dict -> 
CONFIG = {'configurable': {'thread_id': st.session_state["thread_id"]}}

#************************************ Sidebar UI ***************************************************************************************************************

st.sidebar.title("Lang Graph Chatbot")

if st.sidebar.button("New Chat"):
    reset_chat()
    
uploaded_file= st.sidebar.file_uploader("Upload your file")
if uploaded_file:
    st.session_state["file"]= uploaded_file
    st.sidebar.success("File uploaded successfully")
        
st.sidebar.header("My conversations")

for thread_id in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread_id)):
        st.session_state["thread_id"]= thread_id
        messages= load_conversation(thread_id)

        temp_messages= []

        for message in messages:
            if isinstance(message, HumanMessage):
                role= "user"
            else:
                role= "assistant"
            temp_messages.append({"role": role, "content": message.content})

        st.session_state["message_history"]= temp_messages

#************************************ loading the conversation history ******************************************************************************************
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

#{'role': 'user', 'content': 'Hi'}
#{'role': 'assistant', 'content': 'Hi=ello'}

#************************************ Taking input *************************************************************************************************************

user_input = st.chat_input('Type here')

if user_input:

    # first add the message to message_history
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

     # Prepare input for LLM
    if st.session_state.get("file"):
        file_obj = st.session_state["file"]
        file_obj.seek(0)  # ensure pointer is at start
        file_text = extract_text_from_file(file_obj)
        
        user_prompt = (
            f"The user uploaded the following document:\n\n"
            f"{file_text}\n\n"
            f"Now answer the user's question based on this document:\n{user_input}"
        )
        st.session_state["file"]= []
    else:
        user_prompt = user_input
    
    # first add the message to message_history
    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_prompt)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )

    st.session_state['message_history'].append({'role': 'assistant', 'content': ai_message})
