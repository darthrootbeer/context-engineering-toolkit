#!/bin/bash

# job-fit-screen Installation Script

echo "job-fit-screen - Installation Script"
echo "====================================="

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9+ first."
    exit 1
fi
echo "✅ Python 3 found: $(python3 --version)"

if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi
echo "✅ pip3 found"

echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo ""
    echo "⚠️  ANTHROPIC_API_KEY is not set. This tool calls the Claude API and"
    echo "   needs a real key to run."
    echo ""
    echo "   Get one from: https://console.anthropic.com"
    echo "   Then set it:  export ANTHROPIC_API_KEY=sk-ant-..."
    echo ""
    echo "   Add that export line to your shell profile (~/.zshrc or ~/.bashrc)"
    echo "   so it persists across sessions."
else
    echo "✅ ANTHROPIC_API_KEY is set"
fi

chmod +x job_fit_screen.py

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Next steps:"
echo "  1. Copy criteria.example.yaml to a private location and fill in your own values."
echo "  2. Run: ./run_screen.sh --criteria /path/to/your-criteria.yaml --posting /path/to/posting.txt"
echo ""
echo "For more information, see README.md"
