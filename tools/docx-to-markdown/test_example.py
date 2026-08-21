#!/usr/bin/env python3
"""
Test script for Word to Markdown Converter
Creates sample Word documents for testing the conversion functionality.
"""

import os
from pathlib import Path
import subprocess

def create_sample_word_document(filename: str, content: str):
    """Create a sample Word document using Pandoc."""
    # Create a temporary markdown file
    md_content = f"""# Sample Document: {filename}

This is a sample Word document created for testing the Word to Markdown converter.

## Features to Test

### Headers
This document contains various header levels to test conversion.

### Lists
Here are some lists to test:

**Bulleted List:**
- First item
- Second item
- Third item with **bold text**
- Fourth item with *italic text*

**Numbered List:**
1. First numbered item
2. Second numbered item
3. Third numbered item

### Tables
Here's a sample table:

| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
| Data 4   | Data 5   | Data 6   |

### Text Formatting
This paragraph contains **bold text**, *italic text*, and `inline code`.

### Callout Box
> **Note:** This is a callout box that should be converted to a blockquote in Markdown.

### Code Block
```python
def hello_world():
    print("Hello, World!")
    return "Success"
```

### Links
Here's a [link to Google](https://www.google.com) and another to [GitHub](https://github.com).

{content}

---
*Document created for testing purposes*
"""
    
    # Write markdown content to temporary file
    temp_md = f"temp_{filename}.md"
    with open(temp_md, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    # Convert markdown to Word using Pandoc
    docx_file = f"{filename}.docx"
    try:
        cmd = [
            'pandoc',
            temp_md,
            '-f', 'markdown',
            '-t', 'docx',
            '-o', docx_file
        ]
        subprocess.run(cmd, check=True, capture_output=True)
        print(f"✅ Created: {docx_file}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to create {docx_file}: {e}")
    except FileNotFoundError:
        print(f"❌ Pandoc not found. Please install Pandoc to create test documents.")
        return False
    finally:
        # Clean up temporary markdown file
        if os.path.exists(temp_md):
            os.remove(temp_md)
    
    return True

def main():
    """Create sample Word documents for testing."""
    print("Creating sample Word documents for testing...")
    print("=" * 50)
    
    # Create test documents
    test_docs = [
        ("sample_document_1", "This is additional content for the first sample document."),
        ("sample_document_2", "This document contains different content to test various scenarios."),
        ("sample_document_3", "A third document with unique content and formatting examples."),
    ]
    
    success_count = 0
    for filename, content in test_docs:
        if create_sample_word_document(filename, content):
            success_count += 1
    
    print("\n" + "=" * 50)
    print(f"Created {success_count}/{len(test_docs)} sample documents")
    
    if success_count > 0:
        print("\nTo test the converter:")
        print("1. Run: python3 word_to_markdown.py .")
        print("2. Choose option 1 (Convert single file) or 2 (Convert all files)")
        print("3. Check the _converted/ folder for results")
    else:
        print("\nNo documents were created. Please install Pandoc first.")

if __name__ == "__main__":
    main()
