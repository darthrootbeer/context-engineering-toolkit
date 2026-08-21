# Word to Markdown Converter

A Python CLI application that converts Microsoft Word documents (.docx) to Markdown format with content verification and error logging.

## Features

- **High-quality conversion**: Uses Pandoc for best-in-class Word to Markdown conversion
- **Content verification**: Line-by-line verification to ensure no content is lost
- **Interactive CLI**: Menu-driven interface with single file and batch processing options
- **Error logging**: Detailed error logs for failed conversions
- **Local processing**: All conversion happens locally - no cloud services or external APIs
- **Format preservation**: Maintains headers, tables, lists, and formatting structure

## Prerequisites

### 1. Install Pandoc

**macOS:**
```bash
brew install pandoc
```

**Windows:**
Download from [https://pandoc.org/installing.html](https://pandoc.org/installing.html)

**Linux:**
```bash
sudo apt-get install pandoc
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
# Using the friendly launcher script (recommended)
./run_converter.sh

# Or specify a folder directly
./run_converter.sh /path/to/your/word/documents

# Or manually with virtual environment
source venv/bin/activate
python word_to_markdown.py /path/to/your/word/documents
```

### Example

```bash
# Interactive mode - the script will guide you
./run_converter.sh

# Direct folder specification
./run_converter.sh ~/Documents/word_files

# Manual mode
source venv/bin/activate
python word_to_markdown.py ~/Documents/word_files
```

## How It Works

1. **File Discovery**: Scans the specified folder for `.docx` files
2. **Conversion**: Uses Pandoc to convert each Word document to Markdown
3. **Content Verification**: Extracts text from both original and converted files to ensure no content is lost
4. **Output**: Saves converted files to `_converted/` subfolder
5. **Error Logging**: Creates detailed error logs for any failed conversions

## Output Structure

```
your_folder/
├── document1.docx
├── document2.docx
└── _converted/
    ├── document1.md
    ├── document2.md
    ├── document1_errors.txt (if conversion failed)
    └── document2_errors.txt (if conversion failed)
```

## CLI Options

The application provides an interactive menu with the following options:

1. **Convert single file**: Choose and convert one file at a time
2. **Convert all files (batch)**: Process all files in the folder
3. **Change folder**: Select a different folder to process
4. **Create test documents**: Generate sample Word files for testing
5. **View help**: Display help information
6. **Exit**: Quit the application

### Folder Selection

When no folder is specified, the launcher provides several options:
- Current directory
- Desktop folder
- Documents folder
- Downloads folder
- Custom path entry
- macOS file picker (if available)

## Content Verification

The application performs comprehensive content verification:

- Extracts plain text from both Word and Markdown files
- Removes formatting for comparison (headers, bold, italic, etc.)
- Checks that all text content from the original exists in the converted file
- Reports any missing content in error logs

## Error Handling

- **Conversion errors**: Logged to `filename_errors.txt`
- **Content verification failures**: Detailed reports of missing content
- **Timeout protection**: 60-second timeout for each conversion
- **Graceful degradation**: Continues processing other files if one fails

## Supported Formats

### Input
- Microsoft Word documents (.docx)

### Output
- Markdown (.md) with preserved structure:
  - Headers (H1-H6)
  - Tables
  - Numbered and bulleted lists
  - Bold and italic text
  - Links
  - Code blocks

## Troubleshooting

### Pandoc Not Found
If you see "Pandoc is not installed" error:
1. Install Pandoc using the instructions above
2. Ensure Pandoc is in your system PATH
3. Restart your terminal

### Conversion Failures
- Check error logs in the `_converted/` folder
- Ensure Word documents are not password-protected
- Verify files are valid .docx format

### Content Verification Warnings
- Some formatting differences are expected (Word-specific features)
- The verification focuses on text content, not exact formatting
- Check error logs for specific missing content

## Development

### Requirements
- Python 3.7+
- Pandoc
- Dependencies listed in `requirements.txt`

### Running Tests
```bash
# Create sample Word documents for testing
source venv/bin/activate
python test_example.py

# Test the converter
./run_converter.sh .
```

## License

This project is open source and available under the MIT License.
