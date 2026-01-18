from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import ElasticsearchStore
from elasticsearch import Elasticsearch
from langchain_community.embeddings import HuggingFaceEmbeddings
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
# Try to load from .env file first, then fall back to environment variables
def load_env_vars():
    env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value
        print("✅ Loaded environment variables from .env file")
    else:
        print("⚠️  No .env file found, using system environment variables")

# Load environment variables
load_env_vars()

model_service = os.getenv("MODEL_ENDPOINT")
elasticsearch_url = os.getenv("ELASTIC_URL")
elasticsearch_pass = os.getenv("ELASTIC_PASS")
print("--- MODEL SERVICE --- ", model_service)
print("--- ELASTICSEARCH URL --- ", elasticsearch_url)

# Initialize Elasticsearch connection early
es = None

# Check if Elasticsearch is configured
if elasticsearch_url:
    try:
        if elasticsearch_pass and elasticsearch_pass != "your_elastic_password_here" and elasticsearch_pass != "no_password_needed":
            # With authentication
            es = Elasticsearch(
                hosts=[elasticsearch_url],
                basic_auth=("elastic", elasticsearch_pass),
                verify_certs=False
            )
            print(f"Elasticsearch connected to: {elasticsearch_url} with authentication")
        else:
            # Without authentication (local development)
            es = Elasticsearch(
                hosts=[elasticsearch_url],
                verify_certs=False
            )
            print(f"Elasticsearch connected to: {elasticsearch_url} without authentication")
        
        # Test the connection - use HTTP request instead of client methods
        try:
            import requests
            # Test via HTTP request
            response = requests.get(f"{elasticsearch_url}/_cluster/health", timeout=5)
            if response.status_code == 200:
                health_data = response.json()
                if health_data.get('status') in ['green', 'yellow']:
                    print("✅ Elasticsearch connection successful (HTTP health check)!")
                else:
                    print(f"⚠️ Elasticsearch status: {health_data.get('status')}")
            else:
                print(f"⚠️ Elasticsearch HTTP status: {response.status_code}")
        except Exception as e:
            print(f"⚠️ Elasticsearch connection test warning: {e}")
            # Continue anyway - the client might still work
    except Exception as e:
        print(f"❌ Elasticsearch connection error: {e}")
        es = None
else:
    print("Elasticsearch not configured - running in local mode only")

# Handle different model service formats
if model_service:
    if model_service.endswith('/v1'):
        # Already has /v1
        pass
    elif model_service.endswith('/'):
        # Ends with slash, add v1
        model_service = f"{model_service}v1"
    else:
        # No slash, add /v1
        model_service = f"{model_service}/v1"
else:
    # Default to localhost:8000 if not set
    model_service = "http://localhost:8000/v1"
    print("No MODEL_ENDPOINT set, using default: http://localhost:8000/v1")

@st.cache_resource(show_spinner=False)
def checking_model_service():
    start = time.time()
    print("Checking Model Service Availability...")
    ready = False
    max_attempts = 30  # Wait up to 30 seconds
    attempts = 0
    
    while not ready and attempts < max_attempts:
        try:
            # Try OpenAI-compatible endpoint
            request_openai = requests.get(f'{model_service}/models', timeout=5)
            if request_openai.status_code == 200:
                server = "OpenAI_Compatible"
                ready = True
                break
            
            # Try Ollama endpoint
            base_url = model_service.replace('/v1', '')
            request_ollama = requests.get(f'{base_url}/api/tags', timeout=5)
            if request_ollama.status_code == 200:
                server = "Ollama"
                ready = True
                break
                
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempts + 1}: Connection failed - {e}")
        except Exception as e:
            print(f"Attempt {attempts + 1}: Unexpected error - {e}")
        
        attempts += 1
        time.sleep(1)
    
    if ready:
        print(f"{server} Model Service Available")
        print(f"{time.time()-start} seconds")
        return server
    else:
        print("Model service not available after 30 seconds")
        return None 

def get_models():
    try:
        response = requests.get(f"{model_service[:-2]}api/tags")
        return [i["name"] for i in json.loads(response.content)["models"]]
    except:
        return None

def get_default_model():
    """Get the first available model or use a fallback"""
    models = get_models()
    if models and len(models) > 0:
        return models[0]  # Return the first available model
    return "qwen2.5:0.5b"  # Fallback model name

# Get the default model early so it can be used in the UI
default_model = get_default_model()

st.title("💬 From Podman AI Lab to OpenShift AI - Chat with RHOAI documentation")  

# Show configuration info
with st.expander("🔧 Configuration Info", expanded=False):
    st.write(f"**Model Service:** {model_service}")
    st.write(f"**Active Model:** {default_model}")
    st.write(f"**Elasticsearch:** {elasticsearch_url or 'Not configured'}")
    
    if not model_service or "localhost:8000" in model_service:
        st.info("💡 **Tip**: To use a local model service, make sure you have one running on http://localhost:8000")
        st.write("**Options to get a model service running:**")
        st.write("1. **Podman AI Lab**: Start a model service in VS Code")
        st.write("2. **Ollama**: Run `ollama serve` and download a model")
        st.write("3. **Custom service**: Point to your own endpoint")
    
    if not elasticsearch_url:
        st.info("🔍 **Elasticsearch Setup**: To enable RAG capabilities, you need Elasticsearch running")
        st.write("**Quick setup options:**")
        st.write("1. **Local with Podman/Docker**: Run `./setup_elasticsearch_local.sh`")
        st.write("2. **Cloud service**: Use Elastic Cloud or AWS OpenSearch")
        st.write("3. **OpenShift**: Deploy using the provided YAML files")
    elif es:
        st.success("✅ **Elasticsearch**: Connected and ready for RAG!")
    else:
        st.warning("⚠️ **Elasticsearch**: Configured but connection failed")

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
print(f"Using model: {default_model}")

llm = ChatOpenAI(
        api_key="sk-no-key-required",
        openai_api_base=model_service,
        model=default_model,  # Use the detected model
        streaming=True,
        callbacks=[StreamlitCallbackHandler(st.empty(),
                                            expand_new_thoughts=True,
                                            collapse_completed_thoughts=True)])

embeddings = HuggingFaceEmbeddings()

# Create ElasticsearchStore only if Elasticsearch is available
if es:
    try:
        # Try to create index with explicit dimensions
        db = ElasticsearchStore.from_documents(
            [],
            embeddings,
            index_name="rhoai-docs",
            es_connection=es,
            dims_length=768,  # Specify embedding dimensions
        )
        print("ElasticsearchStore created successfully")
    except Exception as e:
        print(f"⚠️ ElasticsearchStore creation failed: {e}")
        # Try alternative approach - create empty store
        try:
            db = ElasticsearchStore(
                index_name="rhoai-docs",
                es_connection=es,
                embedding=embeddings,
            )
            print("ElasticsearchStore created with alternative method")
        except Exception as e2:
            print(f"⚠️ Alternative method also failed: {e2}")
            print("Falling back to local mode only")
            db = None
else:
    print("ElasticsearchStore not created - running in local mode only")
    db = None

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

# Create chain only if Elasticsearch is available
if db:
    chain = RetrievalQA.from_chain_type(llm,
                                    retriever=db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"k": 4, "score_threshold": 0.2 }),
                                    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
                                    return_source_documents=True)
    print("RAG chain created successfully")
else:
    # Create a simple LLM chain for local mode
    chain = LLMChain(llm=llm, prompt=prompt)
    print("Simple LLM chain created for local mode")
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
    
    # Handle different chain types
    try:
        if db:
            # RAG mode
            response = chain.invoke({"query": prompt})
            print(response)
        else:
            # Local mode - simple LLM response
            # Get conversation history from session state
            history = st.session_state.messages[:-1]  # Exclude the current user message
            response = chain.invoke({"input": prompt, "history": history})
            print(response)
            # Convert to RAG-like format for consistency
            response = {"result": response["text"], "source_documents": []}
    except Exception as e:
        error_msg = f"Error connecting to model service: {str(e)}"
        if "Connection error" in str(e):
            error_msg = "❌ **Connection Error**: Unable to connect to the AI model service. Please ensure:\n\n" \
                       "1. Podman AI Lab is running\n" \
                       "2. A model service is started on the configured endpoint\n" \
                       "3. Check your MODEL_ENDPOINT environment variable\n\n" \
                       "**Current endpoint**: " + (model_service or "Not configured")
        elif "Missing some input keys" in str(e):
            error_msg = "❌ **Configuration Error**: " + str(e)
        else:
            error_msg = "❌ **Unexpected Error**: " + str(e)
        
        st.error(error_msg)
        response = {"result": error_msg, "source_documents": []}

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