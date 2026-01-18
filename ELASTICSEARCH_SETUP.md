# Elasticsearch Setup Guide for RAG Chatbot

## Overview
This guide helps you set up Elasticsearch locally to enable RAG (Retrieval Augmented Generation) capabilities in the chatbot.

## Quick Setup (Recommended for Development)

### 1. Run the Setup Script
```bash
# Make sure you're in the project root directory
chmod +x setup_elasticsearch_local.sh
./setup_elasticsearch_local.sh
```

This script will:
- Start Elasticsearch in a container (Podman/Docker)
- Configure it for local development (no authentication)
- Create a `.env` file with the correct configuration
- Test the connection

### 2. Verify Elasticsearch is Running
```bash
# Check if Elasticsearch is responding
curl http://localhost:9200

# Expected response:
# {
#   "name" : "elasticsearch-local",
#   "cluster_name" : "docker-cluster",
#   "version" : { ... },
#   "tagline" : "You Know, for Search"
# }
```

### 3. Start the Chatbot
```bash
# Run the chatbot with RAG capabilities
./run_local.sh
```

## Manual Setup

### Option 1: Podman/Docker
```bash
# Start Elasticsearch container
podman run -d \
    --name elasticsearch-local \
    -p 9200:9200 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
    docker.elastic.co/elasticsearch/elasticsearch:8.11.0

# Wait for it to be ready
curl -s http://localhost:9200 > /dev/null && echo "Ready!" || echo "Still starting..."
```

### Option 2: Homebrew (macOS)
```bash
# Install Elasticsearch
brew tap elastic/tap
brew install elastic/tap/elasticsearch-full

# Start Elasticsearch
brew services start elasticsearch-full

# Check status
brew services list | grep elasticsearch
```

### Option 3: Direct Download
1. Download from [Elasticsearch Downloads](https://www.elastic.co/downloads/elasticsearch)
2. Extract and run: `./bin/elasticsearch`
3. Configure `config/elasticsearch.yml` for local development

## Configuration

### Environment Variables
Create a `.env` file in your project root:
```bash
# Elasticsearch Configuration
ELASTIC_URL=http://localhost:9200
ELASTIC_PASS=no_password_needed  # For local development

# Model Service
MODEL_ENDPOINT=http://localhost:8000

# Streamlit
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_RUN_ON_SAVE=true
```

### Elasticsearch Settings
For local development, the setup script configures:
- **Port**: 9200 (HTTP) and 9300 (Transport)
- **Security**: Disabled (no authentication required)
- **Memory**: 512MB heap (suitable for development)
- **Discovery**: Single-node mode

## Testing the Setup

### 1. Basic Connection Test
```bash
curl http://localhost:9200
```

### 2. Create a Test Index
```bash
curl -X PUT "localhost:9200/test-index"
```

### 3. Check Index Creation
```bash
curl "localhost:9200/_cat/indices?v"
```

## Troubleshooting

### Common Issues

#### 1. Port Already in Use
```bash
# Check what's using port 9200
lsof -i :9200

# Kill the process or use a different port
```

#### 2. Container Won't Start
```bash
# Check container logs
podman logs elasticsearch-local

# Check system resources
podman system df
```

#### 3. Connection Refused
- Ensure Elasticsearch is running
- Check firewall settings
- Verify port configuration

#### 4. Memory Issues
```bash
# Increase memory allocation
podman run -d \
    --name elasticsearch-local \
    -p 9200:9200 \
    -e "ES_JAVA_OPTS=-Xms1g -Xmx1g" \
    docker.elastic.co/elasticsearch/elasticsearch:8.11.0
```

## Production Considerations

For production use, consider:
- **Security**: Enable authentication and TLS
- **Persistence**: Use volumes for data persistence
- **Monitoring**: Set up logging and monitoring
- **Backup**: Implement regular backup strategies
- **Scaling**: Use multi-node clusters

## Next Steps

Once Elasticsearch is running:
1. **Start your model service** on localhost:8000
2. **Run the chatbot** with `./run_local.sh`
3. **Ingest documents** using the provided notebook
4. **Test RAG capabilities** by asking questions

## Useful Commands

```bash
# Start Elasticsearch
./setup_elasticsearch_local.sh

# Stop Elasticsearch
podman stop elasticsearch-local

# Start existing container
podman start elasticsearch-local

# Remove container
podman rm elasticsearch-local

# View logs
podman logs -f elasticsearch-local

# Check status
curl -s http://localhost:9200/_cluster/health | jq
```

## Support

If you encounter issues:
1. Check the container logs
2. Verify network connectivity
3. Ensure sufficient system resources
4. Check the [Elasticsearch documentation](https://www.elastic.co/guide/index.html)
