# Local Setup Guide - Podman AI Lab to RHOAI

## Overview
This guide will help you set up and run the Podman AI Lab to RHOAI project locally for development and testing purposes.

## Prerequisites

### Required Software
- **Podman Desktop** (latest version)
- **Podman AI Lab Extension** for VS Code
- **Python 3.11+**
- **VS Code** with Python extension
- **Git**

### System Requirements
- **RAM**: Minimum 8GB, Recommended 16GB+
- **Storage**: At least 10GB free space
- **OS**: macOS, Linux, or Windows with WSL2

## Local Development Setup

### 1. Clone and Setup Project

```bash
# Clone the repository
git clone <your-repo-url>
cd podman-ai-lab-to-rhoai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r components/app/requirements.txt
```

### 2. Install Podman Desktop

1. Download Podman Desktop from [https://podman-desktop.io/](https://podman-desktop.io/)
2. Install and start Podman Desktop
3. Verify installation by running:
   ```bash
   podman --version
   ```

### 3. Install Podman AI Lab Extension

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X)
3. Search for "Podman AI Lab"
4. Install the extension
5. Restart VS Code

### 4. Download AI Model

1. Open VS Code with Podman AI Lab extension
2. Go to AI Lab → Models → Catalog
3. Search for "TheBloke/Mistral-7B-Instruct-v0.2-GGUF"
4. Download the model (this will take some time - ~4GB)

### 5. Test Local Model

1. In Podman AI Lab, go to Services
2. Start a model service with your downloaded Mistral model
3. Test the endpoint with a simple curl command:
   ```bash
   curl -X POST http://localhost:8000/v1/chat/completions \
     -H "Content-Type: application/json" \
     -d '{
       "messages": [
         {"role": "user", "content": "Hello, how are you?"}
       ]
     }'
   ```

## Local Development Workflow

### 1. Run Chatbot Locally

```bash
# Navigate to app directory
cd components/app

# Run the Streamlit app locally
streamlit run chatbot_ui.py --server.port 8501
```

The chatbot will be available at `http://localhost:8501`

### 2. Development with Hot Reload

```bash
# Run with auto-reload for development
streamlit run chatbot_ui.py --server.port 8501 --server.runOnSave true
```

### 3. Testing Locally

1. Open `http://localhost:8501` in your browser
2. Test the chatbot interface
3. Check console logs for any errors
4. Modify `chatbot_ui.py` and see changes automatically

## Local Testing Scenarios

### 1. Model Testing
- Test model responses locally before deployment
- Validate prompt formatting
- Check response quality and speed

### 2. UI Testing
- Test Streamlit interface responsiveness
- Validate chat history functionality
- Test error handling

### 3. Integration Testing
- Test LangChain integration locally
- Validate environment variable handling
- Test API endpoint connections

## Troubleshooting

### Common Issues

#### Podman Not Starting
```bash
# Reset Podman
podman system reset
podman machine init
podman machine start
```

#### Model Download Issues
- Check internet connection
- Verify sufficient disk space
- Try downloading during off-peak hours

#### Python Dependencies
```bash
# Reinstall dependencies
pip uninstall -r components/app/requirements.txt -y
pip install -r components/app/requirements.txt
```

#### Port Conflicts
```bash
# Check what's using port 8501
lsof -i :8501
# Kill process if needed
kill -9 <PID>
```

### Debug Mode

Enable debug logging in VS Code:
1. Open Command Palette (Ctrl+Shift+P)
2. Type "Developer: Toggle Developer Tools"
3. Check Console tab for errors

## Development Best Practices

### 1. Code Organization
- Keep model-specific code in separate modules
- Use environment variables for configuration
- Implement proper error handling

### 2. Testing
- Test locally before pushing changes
- Use different model configurations
- Validate API responses

### 3. Version Control
- Commit frequently with descriptive messages
- Use feature branches for new development
- Test before merging to main

## Next Steps

After local setup is complete:

1. **Deploy to OpenShift**: Follow the main README.md for OpenShift deployment
2. **Customize Models**: Experiment with different AI models
3. **Enhance UI**: Improve the Streamlit interface
4. **Add Features**: Implement additional chatbot capabilities

## Support

For issues and questions:
- Check the troubleshooting section above
- Review Podman AI Lab documentation
- Check OpenShift AI documentation
- Review project issues and discussions

## Local Development Checklist

- [ ] Podman Desktop installed and running
- [ ] Podman AI Lab extension installed in VS Code
- [ ] Python virtual environment created and activated
- [ ] Dependencies installed
- [ ] AI model downloaded
- [ ] Local model service tested
- [ ] Streamlit app running locally
- [ ] Chatbot interface accessible
- [ ] Basic functionality tested
- [ ] Development environment ready
