#!/bin/bash

# Local Elasticsearch Setup Script
# This script sets up Elasticsearch locally for development

set -e

echo "🔍 Setting up local Elasticsearch for RAG chatbot..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Podman is available
if command -v podman &> /dev/null; then
    CONTAINER_CMD="podman"
    print_success "Using Podman: $(podman --version)"
elif command -v docker &> /dev/null; then
    CONTAINER_CMD="docker"
    print_success "Using Docker: $(docker --version)"
else
    print_error "Neither Podman nor Docker is available. Please install one of them."
    exit 1
fi

# Stop and remove existing container if it exists
print_status "Stopping existing Elasticsearch container..."
$CONTAINER_CMD stop elasticsearch-local 2>/dev/null || true
$CONTAINER_CMD rm elasticsearch-local 2>/dev/null || true

# Start Elasticsearch
print_status "Starting Elasticsearch container..."
$CONTAINER_CMD run -d \
    --name elasticsearch-local \
    -p 9200:9200 \
    -p 9300:9300 \
    -e "discovery.type=single-node" \
    -e "xpack.security.enabled=false" \
    -e "ES_JAVA_OPTS=-Xms512m -Xmx512m" \
    docker.elastic.co/elasticsearch/elasticsearch:8.11.0

# Wait for Elasticsearch to be ready
print_status "Waiting for Elasticsearch to be ready..."
attempts=0
max_attempts=60

while [ $attempts -lt $max_attempts ]; do
    if curl -s http://localhost:9200 > /dev/null 2>&1; then
        print_success "Elasticsearch is ready!"
        break
    fi
    
    attempts=$((attempts + 1))
    echo "Attempt $attempts/$max_attempts - waiting for Elasticsearch..."
    sleep 5
done

if [ $attempts -eq $max_attempts ]; then
    print_error "Elasticsearch failed to start within expected time"
    exit 1
fi

# Test the connection
print_status "Testing Elasticsearch connection..."
if curl -s http://localhost:9200 | grep -q "cluster_name"; then
    print_success "Elasticsearch connection successful!"
else
    print_error "Failed to connect to Elasticsearch"
    exit 1
fi

# Create .env file with Elasticsearch configuration
print_status "Creating .env file with Elasticsearch configuration..."
cat > .env << EOF
# Local Development Environment Variables
MODEL_ENDPOINT=http://localhost:8000
ELASTIC_URL=http://localhost:9200
ELASTIC_PASS=no_password_needed
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_RUN_ON_SAVE=true
EOF

print_success ".env file created with Elasticsearch configuration"

echo ""
echo "=========================================="
print_success "Local Elasticsearch setup completed!"
echo "=========================================="
echo ""
echo "Elasticsearch is now running on: http://localhost:9200"
echo "No authentication required for local development"
echo ""
echo "To use the RAG chatbot:"
echo "1. Make sure your model service is running on http://localhost:8000"
echo "2. Run the chatbot: ./run_local.sh"
echo ""
echo "To stop Elasticsearch:"
echo "$CONTAINER_CMD stop elasticsearch-local"
echo ""
echo "To start Elasticsearch again:"
echo "$CONTAINER_CMD start elasticsearch-local"
