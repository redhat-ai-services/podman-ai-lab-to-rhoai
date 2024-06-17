from langchain_openai import ChatOpenAI
from langchain.vectorstores import ElasticsearchStore
from elasticsearch import Elasticsearch
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains import LLMChain
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.memory import ConversationBufferWindowMemory
import streamlit as st
import requests
import time
import json
import os 
import re

#####################################
## GET ENVIRONMENT VARIABLES 
#####################################
model_service = os.getenv("MODEL_ENDPOINT")
elasticsearch_url = os.getenv("ELASTIC_URL")
elasticsearch_pass = os.getenv("ELASTIC_PASS")
print("--- MODEL SERVICE --- ", model_service)
print("--- ELASTICSEARCH URL --- ", elasticsearch_url)

model_service = f"{model_service}/v1"

@st.cache_resource(show_spinner=False)
def checking_model_service():
    start = time.time()
    print("Checking Model Service Availability...")
    ready = False
    while not ready:
        try:
            request_cpp = requests.get(f'{model_service}/models')
            request_ollama = requests.get(f'{model_service[:-2]}api/tags')
            if request_cpp.status_code == 200:
                server = "Llamacpp_Python"
                ready = True
            elif request_ollama.status_code == 200:
                server = "Ollama"
                ready = True        
        except:
            pass
        time.sleep(1)
    print(f"{server} Model Service Available")
    print(f"{time.time()-start} seconds")
    return server 

def get_models():
    try:
        response = requests.get(f"{model_service[:-2]}api/tags")
        return [i["name"].split(":")[0] for i in  
            json.loads(response.content)["models"]]
    except:
        return None

st.title("💬 From Podman AI Lab to OpenShift AI - Chat with RHOAI documentation")  
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", 
                                     "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

@st.cache_resource()
def memory():
    memory = ConversationBufferWindowMemory(return_messages=True,k=10)
    return memory

model_name = "" 

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are world class technical advisor."),
    MessagesPlaceholder(variable_name="history"),
    ("user", "{input}")
])

#####################################
## RAG CODE ADDED 
#####################################
llm = ChatOpenAI(
        api_key="sk-no-key-required",
        openai_api_base=model_service,
        streaming=True,
        callbacks=[StreamlitCallbackHandler(st.empty(),
                                            expand_new_thoughts=True,
                                            collapse_completed_thoughts=True)])

es = Elasticsearch(
    elasticsearch_url,
    basic_auth=("elastic", elasticsearch_pass),
    verify_certs=False
)

embeddings = HuggingFaceEmbeddings()

db = ElasticsearchStore.from_documents(
    [],
    embeddings,
    index_name="rhoai-docs",
    es_connection=es,
)

template="""<s>[INST] <<SYS>>
You are a helpful, respectful and honest assistant.
You will be given a question you need to answer, and a context to provide you with information. You must answer the question based as much as possible on this context.
Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.

If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.
<</SYS>>

Question: {question}
Context: {context} [/INST]
"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

chain = RetrievalQA.from_chain_type(llm,
                                retriever=db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 4, "score_threshold": 0.2 }),
                                chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
                                return_source_documents=True)
#####################################
## END RAG CODE ADDED 
#####################################

#####################################
## UPDATES TO RESPONSE IN MESSAGE 
#####################################
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    print(prompt)
    response = chain.invoke(prompt)
    print(response)

    def extract_links(text):
        """Extract all URLs from a text string."""
        link_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        return link_pattern.findall(text)

    # Displaying the Results (Modified)
    if response["source_documents"]:
        links = []
        for doc in response["source_documents"]:
            links.extend(extract_links(doc.metadata["source"]))

        # Concatenate links and the main result
        link_text = ""
        if links:
            link_text = "\n\n**Relevant Links:**\n" + "\n".join([f"- {link}" for link in links])

        # Combine the result and link text
        combined_message = response["result"] + link_text
        st.chat_message("assistant").markdown(combined_message)
        st.session_state.messages.append({"role": "assistant", "content": combined_message})

    else:
        # If no source documents, just display the result
        st.chat_message("assistant").markdown(response["result"])
        st.session_state.messages.append({"role": "assistant", "content": response["result"]})

    st.rerun()