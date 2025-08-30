# Quick Start Guide - Podman AI Lab to RHOAI

## 🚀 Get Started in 5 Minutes

This guide will get you up and running with the Podman AI Lab to RHOAI project quickly.

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.11+ installed
- ✅ Git installed
- ✅ At least 8GB RAM available
- ✅ 10GB free disk space

## Step 1: Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd podman-ai-lab-to-rhoai

# Run the automated setup script
# On macOS/Linux:
./setup_local.sh

# On Windows:
setup_local.bat
```

## Step 2: Install Podman Desktop

1. Download from [https://podman-desktop.io/](https://podman-desktop.io/)
2. Install and start Podman Desktop
3. Verify installation: `podman --version`

## Step 3: Install VS Code Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Podman AI Lab"
4. Install and restart VS Code

## Step 4: Download AI Model

1. In VS Code, go to AI Lab → Models → Catalog
2. Search for "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
3. Download the model (~4GB, takes a few minutes)

## Step 5: Start Development

```bash
# Run the local development script
./run_local.sh

# Or manually:
cd components/app
streamlit run chatbot_ui.py --server.port 8501
```

## Step 6: Test Your Setup

1. Open `http://localhost:8501` in your browser
2. You should see the chatbot interface
3. Type a message and test the response

## 🎯 What You've Accomplished

- ✅ Local development environment setup
- ✅ Python dependencies installed
- ✅ AI model downloaded
- ✅ Chatbot running locally
- ✅ Ready for development and testing

## 🔧 Next Steps

### For Local Development
- Modify `components/app/chatbot_ui.py` to customize the chatbot
- Test different models and configurations
- Develop RAG functionality locally

### For OpenShift Deployment
- Follow the main [README.md](README.md) for OpenShift deployment
- Deploy Elasticsearch and other infrastructure components
- Scale your application in the enterprise environment

## 🆘 Need Help?

- **Local Setup Issues**: Check [LOCAL_SETUP.md](LOCAL_SETUP.md)
- **Project Details**: See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
- **Deployment**: Follow [README.md](README.md)
- **Issues**: Check GitHub Issues or Discussions

## 🚨 Common Quick Fixes

### Port Already in Use
```bash
# Kill process using port 8501
lsof -ti:8501 | xargs kill -9
```

### Python Issues
```bash
# Recreate virtual environment
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r components/app/requirements.txt
```

### Model Not Responding
- Check if Podman Desktop is running
- Verify model service is started in Podman AI Lab
- Check the endpoint URL in your configuration

---

**🎉 Congratulations! You're now ready to develop AI applications locally with Podman AI Lab!**
