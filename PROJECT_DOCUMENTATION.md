# Project Documentation - Podman AI Lab to RHOAI

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Components](#components)
4. [Data Flow](#data-flow)
5. [Configuration](#configuration)
6. [Development Guide](#development-guide)
7. [Deployment Guide](#deployment-guide)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

## Project OverviewValueError: Missing some input keys: {'history'}

File "/Users/darioristic/Projects/ai Lab/podman-ai-lab-to-rhoai/components/app/chatbot_ui.py", line 161, in <module>
    response = chain.invoke({"input": prompt})
File "/Users/darioristic/Projects/ai Lab/podman-ai-lab-to-rhoai/venv/lib/python3.9/site-packages/langchain/chains/base.py", line 163, in invoke
    self._validate_inputs(inputs)
File "/Users/darioristic/Projects/ai Lab/podman-ai-lab-to-rhoai/venv/lib/python3.9/site-packages/langchain/chains/base.py", line 307, in _validate_inputs
    raise ValueError(msg)

The Podman AI Lab to RHOAI project demonstrates how to transition from local AI model development using Podman AI Lab to enterprise deployment on OpenShift AI (RHOAI). This project creates a Retrieval Augmented Generation (RAG) chatbot that combines local model development with enterprise-grade infrastructure.

### Key Features
- **Local Development**: Use Podman AI Lab for model testing and development
- **Enterprise Deployment**: Deploy on OpenShift AI with proper scaling and management
- **RAG Capabilities**: Integrate with Elasticsearch vector database for document retrieval
- **Containerized**: Fully containerized application for easy deployment
- **Multi-Platform**: Support for different model formats and serving runtimes

### Use Cases
- **Document Q&A**: Chat with company documents and knowledge bases
- **Model Evaluation**: Test models locally before enterprise deployment
- **RAG Development**: Develop and test RAG applications locally
- **Enterprise AI**: Scale AI applications in enterprise environments

## Architecture

### High-Level Architecture
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Podman AI Lab │    │   OpenShift AI   │    │   Elasticsearch │
│                 │    │                  │    │   Vector DB     │
│ • Model Download│    │ • Model Serving  │    │ • Document      │
│ • Local Testing │    │ • Inference      │    │   Storage       │
│ • Recipe Code   │    │ • Scaling        │    │ • Embeddings    │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RAG Chatbot Application                     │
│                                                                 │
│ • Streamlit UI                                                 │
│ • LangChain Integration                                        │
│ • Model Endpoint Connection                                    │
│ • Vector Database Query                                        │
└─────────────────────────────────────────────────────────────────┘
```

### Component Architecture
```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend Layer                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Streamlit UI  │  │   Chat History  │  │   User Input    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Application Layer                          │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   LangChain     │  │   RAG Pipeline  │  │   Response      │ │
│  │   Integration   │  │                 │  │   Generation    │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                       Service Layer                             │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐ │
│  │   Model        │  │   Vector        │  │   Document      │ │
│  │   Inference    │  │   Database      │  │   Storage       │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Components

### 1. Application Components (`components/app/`)

#### `chatbot_ui.py`
The main Streamlit application that provides the chatbot interface.

**Key Features:**
- Streamlit-based web interface
- Chat history management
- LangChain integration for RAG
- Environment variable configuration
- Error handling and logging

**Dependencies:**
- `streamlit`: Web interface framework
- `langchain`: RAG framework
- `langchain_openai`: OpenAI-compatible model integration
- `elasticsearch`: Vector database client
- `sentence_transformers`: Text embedding generation

#### `requirements.txt`
Python dependencies for the application.

#### `Containerfile`
Container image definition for deployment.

#### `deployment.yaml`
Kubernetes/OpenShift deployment configuration.

### 2. Model Serving Runtime (`components/custom-model-serving-runtime/`)

#### `llamacpp-runtime-custom.yaml`
Custom serving runtime configuration for GGUF models.

#### `Containerfile`
Runtime container definition.

#### `src/run.sh`
Runtime startup script.

### 3. Infrastructure Components

#### OpenShift AI (`components/openshift-ai/`)
- Operator deployment
- Data Science Cluster configuration
- Instance management

#### Elasticsearch (`components/elasticsearch/`)
- Vector database operator
- Cluster configuration
- Data ingestion notebooks

#### MinIO (`components/minio/`)
- S3-compatible storage
- Model artifact storage
- Bucket configuration

#### Service Mesh (`components/openshift-servicemesh/`)
- Istio-based service mesh
- Traffic management
- Security policies

#### Serverless (`components/openshift-serverless/`)
- Knative serving
- Auto-scaling
- Event-driven architecture

## Data Flow

### 1. Model Development Flow
```
1. Download Model (Podman AI Lab)
   ↓
2. Local Testing (Podman AI Lab)
   ↓
3. Code Development (VS Code)
   ↓
4. Container Build
   ↓
5. OpenShift Deployment
```

### 2. RAG Query Flow
```
1. User Input
   ↓
2. Query Processing
   ↓
3. Vector Search (Elasticsearch)
   ↓
4. Document Retrieval
   ↓
5. Context Assembly
   ↓
6. Model Inference
   ↓
7. Response Generation
   ↓
8. UI Display
```

### 3. Data Ingestion Flow
```
1. Document Upload
   ↓
2. Text Extraction
   ↓
3. Chunking
   ↓
4. Embedding Generation
   ↓
5. Vector Storage (Elasticsearch)
   ↓
6. Index Creation
```

## Configuration

### Environment Variables

#### Application Configuration
```bash
MODEL_ENDPOINT=http://localhost:8000/v1/chat/completions
ELASTIC_URL=http://localhost:9200
ELASTIC_PASS=your_password_here
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_RUN_ON_SAVE=true
```

#### Model Configuration
```yaml
model_name: mistral7b
serving_runtime: LlamaCPP
model_framework: any
model_server_size: Medium
```

#### Elasticsearch Configuration
```yaml
connection_string: http://elasticsearch:9200
index_name: documents
embedding_model: sentence-transformers/all-MiniLM-L6-v2
```

### Configuration Files

#### `deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: elastic-vectordb-chat
spec:
  replicas: 1
  selector:
    matchLabels:
      app: elastic-vectordb-chat
  template:
    metadata:
      labels:
        app: elastic-vectordb-chat
    spec:
      containers:
      - name: chatbot
        image: your-registry/elastic-vectordb-chat:latest
        ports:
        - containerPort: 8501
        env:
        - name: MODEL_ENDPOINT
          value: "your-model-endpoint"
        - name: ELASTIC_URL
          value: "your-elasticsearch-url"
        - name: ELASTIC_PASS
          value: "your-elasticsearch-password"
```

## Development Guide

### Local Development Setup

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd podman-ai-lab-to-rhoai
   ```

2. **Run Setup Script**
   ```bash
   # Linux/macOS
   chmod +x setup_local.sh
   ./setup_local.sh
   
   # Windows
   setup_local.bat
   ```

3. **Manual Setup (Alternative)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate     # Windows
   
   pip install -r components/app/requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Run Application**
   ```bash
   cd components/app
   streamlit run chatbot_ui.py --server.port 8501
   ```

### Development Workflow

1. **Code Changes**
   - Modify `chatbot_ui.py` for application logic
   - Update `requirements.txt` for dependencies
   - Modify `Containerfile` for container changes

2. **Testing**
   - Test locally with Streamlit
   - Validate model responses
   - Test RAG functionality

3. **Container Build**
   ```bash
   cd components/app
   podman build -t your-registry/elastic-vectordb-chat:latest .
   ```

4. **Deployment**
   ```bash
   oc apply -f deployment.yaml
   ```

## Deployment Guide

### Prerequisites
- OpenShift 4.12+ cluster
- Admin access to cluster
- OpenShift AI 2.9+
- Elasticsearch operator
- Service Mesh operator
- Serverless operator

### Deployment Steps

1. **Deploy OpenShift AI**
   ```bash
   oc apply -k ./components/openshift-ai/operator/overlays/fast
   oc apply -k ./components/openshift-ai/instance/overlays/fast
   ```

2. **Deploy Elasticsearch**
   ```bash
   oc apply -k ./components/elasticsearch/base/
   oc apply -f ./components/elasticsearch/cluster/instance.yaml
   ```

3. **Deploy MinIO**
   ```bash
   oc apply -k ./components/minio/base
   ```

4. **Deploy Service Mesh and Serverless**
   ```bash
   oc apply -k ./components/openshift-servicemesh/operator/overlays/stable
   oc apply -k ./components/openshift-serverless/operator/overlays/stable
   ```

5. **Enable Single Model Serving**
   ```bash
   oc apply -k ./components/model-server/components-serving
   ```

6. **Deploy Custom Runtime**
   - Upload `llamacpp-runtime-custom.yaml` in OpenShift AI
   - Configure model serving

7. **Deploy Application**
   ```bash
   oc new-project elastic-vectordb-chat
   oc apply -f ./components/app/deployment.yaml
   ```

### Deployment Verification

1. **Check Pod Status**
   ```bash
   oc get pods -n elastic-vectordb-chat
   ```

2. **Check Routes**
   ```bash
   oc get routes -n elastic-vectordb-chat
   ```

3. **Test Application**
   - Open application URL in browser
   - Test chatbot functionality
   - Verify model responses

## API Reference

### Model Inference API

#### Endpoint
```
POST /v1/chat/completions
```

#### Request Format
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a helpful assistant."
    },
    {
      "role": "user",
      "content": "Your question here"
    }
  ],
  "max_tokens": 100,
  "temperature": 0.7
}
```

#### Response Format
```json
{
  "id": "chatcmpl-xxx",
  "object": "chat.completion",
  "created": 1234567890,
  "model": "mistral-7b-instruct-v0.2",
  "choices": [
    {
      "index": 0,
      "message": {
        "content": "Response content",
        "role": "assistant"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 32,
    "completion_tokens": 100,
    "total_tokens": 132
  }
}
```

### Elasticsearch API

#### Search Documents
```json
{
  "query": {
    "script_score": {
      "query": {
        "match_all": {}
      },
      "script": {
        "source": "cosineSimilarity(params.query_vector, 'embedding') + 1.0",
        "params": {
          "query_vector": [0.1, 0.2, ...]
        }
      }
    }
  }
}
```

## Troubleshooting

### Common Issues

#### Model Not Responding
- Check model server status
- Verify endpoint URL
- Check SSL certificates
- Validate model file access

#### Elasticsearch Connection Issues
- Verify cluster status
- Check credentials
- Validate network access
- Check index existence

#### Application Deployment Issues
- Check pod logs
- Verify environment variables
- Check resource limits
- Validate image pull

### Debug Commands

#### Check Pod Logs
```bash
oc logs -f deployment/elastic-vectordb-chat -n elastic-vectordb-chat
```

#### Check Service Status
```bash
oc get services -n elastic-vectordb-chat
```

#### Check Events
```bash
oc get events -n elastic-vectordb-chat --sort-by='.lastTimestamp'
```

#### Debug Pod
```bash
oc debug deployment/elastic-vectordb-chat -n elastic-vectordb-chat
```

## Contributing

### Development Guidelines

1. **Code Style**
   - Follow PEP 8 for Python code
   - Use meaningful variable names
   - Add proper documentation
   - Include type hints

2. **Testing**
   - Test locally before committing
   - Validate functionality
   - Test edge cases
   - Performance testing

3. **Documentation**
   - Update relevant documentation
   - Include examples
   - Document configuration changes
   - Update troubleshooting guides

### Pull Request Process

1. **Fork Repository**
2. **Create Feature Branch**
3. **Make Changes**
4. **Test Locally**
5. **Submit Pull Request**
6. **Code Review**
7. **Merge Changes**

### Issue Reporting

When reporting issues, include:
- Environment details
- Steps to reproduce
- Expected vs actual behavior
- Logs and error messages
- Screenshots if applicable

---

## Support and Resources

- **Documentation**: [README.md](README.md)
- **Local Setup**: [LOCAL_SETUP.md](LOCAL_SETUP.md)
- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Podman AI Lab**: [Official Documentation](https://developers.redhat.com/articles/2024/05/07/podman-ai-lab-getting-started)
- **OpenShift AI**: [Official Documentation](https://access.redhat.com/documentation/en-us/red_hat_openshift_ai)
- **Elasticsearch**: [Official Documentation](https://www.elastic.co/guide/index.html)
