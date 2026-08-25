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

if ! command -v claude &> /dev/null; then
    echo ""
    echo "⚠️  The 'claude' CLI (Claude Code) was not found on your PATH."
    echo "   This tool scores postings by shelling out to 'claude -p' — it does"
    echo "   NOT use a raw Anthropic API key."
    echo ""
    echo "   Install Claude Code: https://docs.claude.com/claude-code"
    echo "   Then log in once by running 'claude' interactively before using this tool."
else
    echo "✅ claude CLI found: $(claude --version 2>&1 | head -n 1)"
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
