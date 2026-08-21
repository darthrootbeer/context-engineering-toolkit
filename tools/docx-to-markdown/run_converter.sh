#!/bin/bash

# Word to Markdown Converter Launcher
# This script activates the virtual environment and runs the converter with a friendly menu

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_color() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if folder exists and contains .docx files
check_folder() {
    local folder=$1
    if [[ ! -d "$folder" ]]; then
        print_color $RED "❌ Folder not found: $folder"
        return 1
    fi
    
    local docx_count=$(find "$folder" -maxdepth 1 -name "*.docx" | wc -l)
    if [[ $docx_count -eq 0 ]]; then
        print_color $YELLOW "⚠️  No .docx files found in: $folder"
        return 2
    fi
    
    print_color $GREEN "✅ Found $docx_count .docx file(s) in: $folder"
    return 0
}

# Function to select folder interactively
select_folder() {
    print_color $BLUE "📁 Please select a folder containing Word documents:"
    echo ""
    
    # Show current directory and common locations
    echo "Current directory: $(pwd)"
    echo ""
    print_color $BLUE "Available locations:"
    echo ""
    echo "  1. Current directory (.)"
    echo "  2. Desktop (~/Desktop)"
    echo "  3. Documents (~/Documents)"
    echo "  4. Downloads (~/Downloads)"
    echo "  5. Enter custom path"
    echo "  6. Browse with file picker"
    echo ""
    print_color $YELLOW "Enter your choice (1-6): "
    
    read -p "" choice
    
    case $choice in
        1)
            selected_folder="."
            ;;
        2)
            selected_folder="$HOME/Desktop"
            ;;
        3)
            selected_folder="$HOME/Documents"
            ;;
        4)
            selected_folder="$HOME/Downloads"
            ;;
        5)
            read -p "Enter the full path to your folder: " selected_folder
            ;;
        6)
            # Try to use macOS file picker
            if command -v osascript &> /dev/null; then
                selected_folder=$(osascript -e 'tell application "System Events"
                    set folderPath to choose folder with prompt "Select folder containing Word documents"
                    return POSIX path of folderPath
                end tell' 2>/dev/null)
                if [[ -z "$selected_folder" ]]; then
                    print_color $YELLOW "File picker cancelled or not available"
                    return 1
                fi
            else
                print_color $YELLOW "File picker not available on this system"
                return 1
            fi
            ;;
        *)
            print_color $RED "Invalid choice"
            return 1
            ;;
    esac
    
    # Check the selected folder
    check_folder "$selected_folder"
    local result=$?
    
    if [[ $result -eq 0 ]]; then
        echo "$selected_folder"
        return 0
    elif [[ $result -eq 2 ]]; then
        print_color $YELLOW "Would you like to continue anyway? (y/n): "
        read -p "" continue_anyway
        if [[ $continue_anyway =~ ^[Yy]$ ]]; then
            echo "$selected_folder"
            return 0
        fi
    fi
    
    return 1
}

# Function to show main menu
show_menu() {
    clear
    print_color $BLUE "╔══════════════════════════════════════════════════════════════╗"
    print_color $BLUE "║                Word to Markdown Converter                    ║"
    print_color $BLUE "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    print_color $GREEN "Current folder: $1"
    echo ""
    print_color $BLUE "Available Options:"
    echo ""
    echo "  1. Convert single file"
    echo "  2. Convert all files (batch)"
    echo "  3. Change folder"
    echo "  4. Create test documents"
    echo "  5. View help"
    echo "  6. Exit"
    echo ""
    print_color $YELLOW "Enter your choice (1-6): "
}

# Function to activate virtual environment
activate_venv() {
    if [[ ! -d "$SCRIPT_DIR/venv" ]]; then
        print_color $RED "❌ Virtual environment not found. Please run the installation first."
        echo "Run: ./install.sh"
        exit 1
    fi
    
    source "$SCRIPT_DIR/venv/bin/activate"
}

# Main script logic
main() {
    # Activate virtual environment
    activate_venv
    
    # Check if folder was provided as argument
    if [[ $# -eq 1 ]]; then
        folder="$1"
        check_folder "$folder"
        if [[ $? -ne 0 ]]; then
            print_color $YELLOW "Let's select a different folder..."
            folder=$(select_folder)
            if [[ $? -ne 0 ]]; then
                print_color $RED "No valid folder selected. Exiting."
                exit 1
            fi
        fi
    else
        # No folder provided, select interactively
        folder=$(select_folder)
        if [[ $? -ne 0 ]]; then
            print_color $RED "No folder selected. Exiting."
            exit 1
        fi
    fi
    
    # Main menu loop
    while true; do
        show_menu "$folder"
        read -p "" choice
        
        case $choice in
            1|2)
                print_color $BLUE "Starting converter..."
                python "$SCRIPT_DIR/word_to_markdown.py" "$folder"
                echo ""
                read -p "Press Enter to continue..."
                ;;
            3)
                new_folder=$(select_folder)
                if [[ $? -eq 0 ]]; then
                    folder="$new_folder"
                fi
                ;;
            4)
                print_color $BLUE "Creating test documents..."
                python "$SCRIPT_DIR/test_example.py"
                echo ""
                read -p "Press Enter to continue..."
                ;;
            5)
                clear
                print_color $BLUE "Word to Markdown Converter Help"
                echo "=================================="
                echo ""
                echo "This tool converts Microsoft Word documents (.docx) to Markdown format."
                echo ""
                echo "Features:"
                echo "• High-quality conversion using Pandoc"
                echo "• Content verification to ensure no text is lost"
                echo "• Error logging for failed conversions"
                echo "• Interactive menu system"
                echo ""
                echo "Output:"
                echo "• Converted files saved to '_converted/' subfolder"
                echo "• Error logs saved as 'filename_errors.txt'"
                echo ""
                echo "For more information, see README.md"
                echo ""
                read -p "Press Enter to continue..."
                ;;
            6)
                print_color $GREEN "Goodbye! 👋"
                exit 0
                ;;
            *)
                print_color $RED "Invalid choice. Please try again."
                sleep 2
                ;;
        esac
    done
}

# Run main function with all arguments
main "$@"
