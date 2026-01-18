#!/bin/bash

echo "🧪 Testing Services for RAG Chatbot"
echo "=================================="

# Test Model Service
echo ""
echo "🔍 Testing Model Service (localhost:8000)..."
if curl -s http://localhost:8000/v1/models > /dev/null; then
    echo "✅ Model service is responding"
    
    # Get available models
    models=$(curl -s http://localhost:8000/api/tags | jq -r '.models[].name' | tr '\n' ', ')
    echo "📋 Available models: ${models%, }"
    
    # Test a simple completion
    echo "🧠 Testing model completion..."
    response=$(curl -s -X POST http://localhost:8000/v1/chat/completions \
        -H "Content-Type: application/json" \
        -d '{"messages": [{"role": "user", "content": "Say hello!"}], "model": "qwen2.5:0.5b", "max_tokens": 20}')
    
    if echo "$response" | grep -q "choices"; then
        echo "✅ Model completion test successful"
    else
        echo "❌ Model completion test failed"
        echo "Response: $response"
    fi
else
    echo "❌ Model service is not responding"
fi

# Test Elasticsearch
echo ""
echo "🔍 Testing Elasticsearch (localhost:9200)..."
if curl -s http://localhost:9200 > /dev/null; then
    echo "✅ Elasticsearch is responding"
    
    # Get cluster info
    cluster_name=$(curl -s http://localhost:9200 | jq -r '.cluster_name')
    version=$(curl -s http://localhost:9200 | jq -r '.version.number')
    echo "📊 Cluster: $cluster_name (v$version)"
    
    # Test index creation
    echo "📝 Testing index creation..."
    if curl -s -X PUT "localhost:9200/test-index" > /dev/null; then
        echo "✅ Index creation test successful"
        
        # Clean up test index
        curl -s -X DELETE "localhost:9200/test-index" > /dev/null
        echo "🧹 Test index cleaned up"
    else
        echo "❌ Index creation test failed"
    fi
else
    echo "❌ Elasticsearch is not responding"
fi

echo ""
echo "=================================="
echo "🎯 Service Status Summary:"
echo ""

# Final status check
if curl -s http://localhost:8000/v1/models > /dev/null && curl -s http://localhost:9200 > /dev/null; then
    echo "🎉 All services are running! Your RAG chatbot should work perfectly."
    echo ""
    echo "Next steps:"
    echo "1. Create a .env file with the configuration"
    echo "2. Run the chatbot: ./run_local.sh"
    echo "3. Start chatting with RAG capabilities!"
else
    echo "⚠️  Some services are not running. Please check the configuration."
fi
