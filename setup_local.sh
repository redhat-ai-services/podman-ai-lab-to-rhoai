#!/bin/bash

# Local Setup Script for Podman AI Lab to RHOAI
# This script automates the local development environment setup

set -e

echo "🚀 Setting up local development environment for Podman AI Lab to RHOAI..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if Python is installed
check_python() {
    print_status "Checking Python installation..."
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
        print_success "Python 3 found: $(python3 --version)"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
        print_success "Python found: $(python --version)"
    else
        print_error "Python is not installed. Please install Python 3.11+ first."
        exit 1
    fi
}

# Check if pip is installed
check_pip() {
    print_status "Checking pip installation..."
    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
        print_success "pip3 found: $(pip3 --version)"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
        print_success "pip found: $(pip --version)"
    elif python3 -m pip --version &> /dev/null; then
        PIP_CMD="python3 -m pip"
        print_success "python3 -m pip found: $(python3 -m pip --version)"
    elif python -m pip --version &> /dev/null; then
        PIP_CMD="python -m pip"
        print_success "python -m pip found: $(python -m pip --version)"
    else
        print_error "pip is not installed. Please install pip first."
        exit 1
    fi
}

# Check if podman is installed
check_podman() {
    print_status "Checking Podman installation..."
    if command -v podman &> /dev/null; then
        print_success "Podman found: $(podman --version)"
    else
        print_warning "Podman not found. Please install Podman Desktop from https://podman-desktop.io/"
        print_status "You can continue with Python setup, but Podman features won't work."
    fi
}

# Create virtual environment
create_venv() {
    print_status "Creating Python virtual environment..."
    if [ ! -d "venv" ]; then
        $PYTHON_CMD -m venv venv
        print_success "Virtual environment created"
    else
        print_warning "Virtual environment already exists"
    fi
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    print_success "Virtual environment activated"
}

# Install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    $PIP_CMD install --upgrade pip
    $PIP_CMD install -r components/app/requirements.txt
    print_success "Dependencies installed successfully"
}

# Create .env file for local development
create_env_file() {
    print_status "Creating .env file for local development..."
    if [ ! -f ".env" ]; then
        cat > .env << EOF
# Local Development Environment Variables
MODEL_ENDPOINT=http://localhost:8000/v1/chat/completions
ELASTIC_URL=http://localhost:9200
ELASTIC_PASS=your_elastic_password_here
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_RUN_ON_SAVE=true
EOF
        print_success ".env file created"
        print_warning "Please update the .env file with your actual values"
    else
        print_warning ".env file already exists"
    fi
}

# Create local development script
create_dev_script() {
    print_status "Creating local development script..."
    cat > run_local.sh << 'EOF'
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
EOF

    chmod +x run_local.sh
    print_success "Local development script created: run_local.sh"
}

# Main setup function
main() {
    echo "=========================================="
    echo "  Podman AI Lab to RHOAI - Local Setup"
    echo "=========================================="
    echo ""

    # Check prerequisites
    check_python
    check_pip
    check_podman

    # Setup Python environment
    create_venv
    activate_venv
    install_dependencies

    # Create configuration files
    create_env_file
    create_dev_script

    echo ""
    echo "=========================================="
    print_success "Local setup completed successfully!"
    echo "=========================================="
    echo ""
    echo "Next steps:"
    echo "1. Install Podman Desktop if not already installed"
    echo "2. Install Podman AI Lab extension in VS Code"
    echo "3. Download the Mistral model in Podman AI Lab"
    echo "4. Update the .env file with your configuration"
    echo "5. Run './run_local.sh' to start development"
    echo ""
    echo "For detailed instructions, see LOCAL_SETUP.md"
    echo ""
}

# Run main function
main "$@"
