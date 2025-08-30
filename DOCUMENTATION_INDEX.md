# Documentation Index - Podman AI Lab to RHOAI

## 📚 Complete Documentation Guide

Welcome to the Podman AI Lab to RHOAI project documentation! This index will help you find the right information for your needs.

## 🚀 Getting Started

### For New Users
- **[QUICK_START.md](QUICK_START.md)** - Get up and running in 5 minutes
- **[LOCAL_SETUP.md](LOCAL_SETUP.md)** - Detailed local development setup
- **[README.md](README.md)** - Main project overview and OpenShift deployment

### For Developers
- **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Comprehensive technical documentation
- **[LOCAL_SETUP.md](LOCAL_SETUP.md)** - Development environment setup
- **[components/app/](components/app/)** - Application source code

## 📖 Documentation by Category

### 🏗️ Architecture & Design
- **[PROJECT_DOCUMENTATION.md#architecture](PROJECT_DOCUMENTATION.md#architecture)** - System architecture and design
- **[README.md#arch](README.md#arch)** - High-level architecture overview
- **[components/](components/)** - Component structure and organization

### 🛠️ Development & Testing
- **[LOCAL_SETUP.md](LOCAL_SETUP.md)** - Local development setup
- **[PROJECT_DOCUMENTATION.md#development-guide](PROJECT_DOCUMENTATION.md#development-guide)** - Development workflow
- **[components/app/chatbot_ui.py](components/app/chatbot_ui.py)** - Main application code
- **[components/app/requirements.txt](components/app/requirements.txt)** - Python dependencies

### 🚀 Deployment & Operations
- **[README.md](README.md)** - Complete OpenShift deployment guide
- **[PROJECT_DOCUMENTATION.md#deployment-guide](PROJECT_DOCUMENTATION.md#deployment-guide)** - Deployment procedures
- **[components/app/deployment.yaml](components/app/deployment.yaml)** - Kubernetes deployment config
- **[components/app/Containerfile](components/app/Containerfile)** - Container image definition

### 🔧 Configuration & Setup
- **[env.example](env.example)** - Environment configuration template
- **[PROJECT_DOCUMENTATION.md#configuration](PROJECT_DOCUMENTATION.md#configuration)** - Configuration options
- **[components/](components/)** - Infrastructure component configurations

### 📊 Infrastructure Components
- **[components/openshift-ai/](components/openshift-ai/)** - OpenShift AI configuration
- **[components/elasticsearch/](components/elasticsearch/)** - Elasticsearch setup
- **[components/minio/](components/minio/)** - MinIO S3 storage
- **[components/openshift-servicemesh/](components/openshift-servicemesh/)** - Service Mesh
- **[components/openshift-serverless/](components/openshift-serverless/)** - Serverless components

### 🤖 AI & ML Components
- **[components/custom-model-serving-runtime/](components/custom-model-serving-runtime/)** - Custom model runtime
- **[components/model-server/](components/model-server/)** - Model serving configuration
- **[notebooks/](notebooks/)** - Jupyter notebooks for data ingestion

## 🎯 User Journey Maps

### 🆕 New User Journey
```
1. QUICK_START.md → Get basic understanding
2. LOCAL_SETUP.md → Set up local environment
3. README.md → Learn about full capabilities
4. PROJECT_DOCUMENTATION.md → Deep dive into technical details
```

### 👨‍💻 Developer Journey
```
1. LOCAL_SETUP.md → Development environment
2. components/app/ → Application code
3. PROJECT_DOCUMENTATION.md → Architecture and APIs
4. README.md → Deployment options
```

### 🚀 DevOps Journey
```
1. README.md → Deployment overview
2. PROJECT_DOCUMENTATION.md → Infrastructure details
3. components/ → Component configurations
4. PROJECT_DOCUMENTATION.md#troubleshooting → Operations
```

## 📋 Quick Reference

### Essential Commands
```bash
# Local setup
./setup_local.sh                    # Linux/macOS
setup_local.bat                     # Windows

# Run locally
./run_local.sh                      # Linux/macOS
run_local.bat                       # Windows

# Manual run
cd components/app
streamlit run chatbot_ui.py --server.port 8501
```

### Key Files
- **`chatbot_ui.py`** - Main application
- **`requirements.txt`** - Python dependencies
- **`deployment.yaml`** - Kubernetes deployment
- **`Containerfile`** - Container image
- **`.env`** - Environment configuration

### Important URLs
- **Local App**: http://localhost:8501
- **Podman Desktop**: https://podman-desktop.io/
- **VS Code**: https://code.visualstudio.com/

## 🔍 Search by Topic

### Looking for...
- **Setup instructions** → [LOCAL_SETUP.md](LOCAL_SETUP.md)
- **Quick start** → [QUICK_START.md](QUICK_START.md)
- **Architecture details** → [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
- **Deployment guide** → [README.md](README.md)
- **API reference** → [PROJECT_DOCUMENTATION.md#api-reference](PROJECT_DOCUMENTATION.md#api-reference)
- **Troubleshooting** → [PROJECT_DOCUMENTATION.md#troubleshooting](PROJECT_DOCUMENTATION.md#troubleshooting)
- **Configuration** → [PROJECT_DOCUMENTATION.md#configuration](PROJECT_DOCUMENTATION.md#configuration)

## 📝 Documentation Maintenance

### Keeping Documentation Updated
- Update relevant sections when code changes
- Test all setup instructions regularly
- Validate deployment procedures
- Review and update troubleshooting guides

### Contributing to Documentation
- Follow the existing structure and format
- Include practical examples
- Test all instructions before committing
- Update this index when adding new documents

## 🆘 Getting Help

### Documentation Issues
- Check if the information is in the right place
- Verify links and references
- Ensure consistency across documents

### Technical Issues
- **Local Development**: [LOCAL_SETUP.md](LOCAL_SETUP.md)
- **Deployment**: [README.md](README.md)
- **Architecture**: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
- **GitHub Issues**: Project issue tracker

---

## 📊 Documentation Status

- ✅ **Complete**: README.md, LOCAL_SETUP.md, QUICK_START.md
- ✅ **Complete**: PROJECT_DOCUMENTATION.md
- ✅ **Complete**: Setup scripts and examples
- 🔄 **In Progress**: Component-specific documentation
- 📋 **Planned**: Video tutorials, troubleshooting guides

---

**📚 This documentation is continuously updated. Check back regularly for the latest information!**
