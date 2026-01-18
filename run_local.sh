#!/bin/bash

# Local Development Runner Script
echo "🚀 Starting local development environment..."

# Activate virtual environment
source venv/bin/activate

# Set environment variables
export $(cat .env | xargs)

# Run the Streamlit app
echo "Starting Streamlit app on port $STREAMLIT_SERVER_PORT..."
cd components/app
streamlit run chatbot_ui.py --server.port $STREAMLIT_SERVER_PORT --server.runOnSave $STREAMLIT_SERVER_RUN_ON_SAVE
