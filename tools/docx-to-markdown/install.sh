#!/bin/bash

# Word to Markdown Converter Installation Script

echo "Word to Markdown Converter - Installation Script"
echo "================================================"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7+ first."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

echo "✅ pip3 found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

# Check if Pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "⚠️  Pandoc is not installed. This is required for conversion."
    echo ""
    echo "Please install Pandoc:"
    echo ""
    
    # Detect OS and provide installation instructions
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macOS detected. Install with Homebrew:"
        echo "  brew install pandoc"
        echo ""
        echo "Or download from: https://pandoc.org/installing.html"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "Linux detected. Install with:"
        echo "  sudo apt-get install pandoc"
        echo ""
        echo "Or download from: https://pandoc.org/installing.html"
    else
        echo "Please download Pandoc from: https://pandoc.org/installing.html"
    fi
    
    echo ""
    echo "After installing Pandoc, you can run the converter with:"
    echo "  python3 word_to_markdown.py /path/to/your/word/documents"
else
    echo "✅ Pandoc found: $(pandoc --version | head -n 1)"
fi

# Make the script executable
chmod +x word_to_markdown.py

echo ""
echo "🎉 Installation complete!"
echo ""
echo "Usage:"
echo "  python3 word_to_markdown.py /path/to/your/word/documents"
echo ""
echo "Example:"
echo "  python3 word_to_markdown.py ~/Documents/word_files"
echo ""
echo "For more information, see README.md"
