#!/usr/bin/env python3
"""
Word to Markdown Converter
Converts Microsoft Word documents to Markdown format with content verification.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path
from typing import List, Tuple, Optional
import click
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.panel import Panel
import difflib

console = Console()

class WordToMarkdownConverter:
    def __init__(self, input_folder: str):
        self.input_folder = Path(input_folder)
        self.output_folder = self.input_folder / "_converted"
        self.error_logs = []
        
    def check_pandoc_installed(self) -> bool:
        """Check if Pandoc is installed and available."""
        try:
            result = subprocess.run(['pandoc', '--version'], 
                                  capture_output=True, text=True, timeout=10)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_docx_files(self) -> List[Path]:
        """Get all .docx files in the input folder."""
        return list(self.input_folder.glob("*.docx"))
    
    def create_output_folder(self):
        """Create the output folder if it doesn't exist."""
        self.output_folder.mkdir(exist_ok=True)
    
    def extract_text_from_docx(self, docx_path: Path) -> str:
        """Extract plain text from Word document for comparison."""
        try:
            import docx
            doc = docx.Document(docx_path)
            text = []
            for paragraph in doc.paragraphs:
                text.append(paragraph.text)
            return '\n'.join(text)
        except ImportError:
            console.print("[yellow]Warning: python-docx not available, skipping text extraction[/yellow]")
            return ""
    
    def extract_text_from_markdown(self, md_path: Path) -> str:
        """Extract plain text from Markdown file for comparison."""
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remove markdown formatting for comparison
            import re
            # Remove headers
            content = re.sub(r'^#{1,6}\s+', '', content, flags=re.MULTILINE)
            # Remove bold/italic
            content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)
            content = re.sub(r'\*(.*?)\*', r'\1', content)
            # Remove links
            content = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', content)
            # Remove code blocks
            content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            # Remove inline code
            content = re.sub(r'`([^`]+)`', r'\1', content)
            
            return content.strip()
        except Exception as e:
            console.print(f"[red]Error reading markdown file: {e}[/red]")
            return ""
    
    def verify_content(self, docx_path: Path, md_path: Path) -> Tuple[bool, List[str]]:
        """Verify that all content from Word document exists in Markdown."""
        docx_text = self.extract_text_from_docx(docx_path)
        md_text = self.extract_text_from_markdown(md_path)
        
        if not docx_text:
            return True, []  # Skip verification if we couldn't extract text
        
        # Normalize whitespace for comparison
        docx_lines = [line.strip() for line in docx_text.split('\n') if line.strip()]
        md_lines = [line.strip() for line in md_text.split('\n') if line.strip()]
        
        missing_content = []
        
        # Check if all docx lines exist in markdown (allowing for reordering)
        for docx_line in docx_lines:
            if docx_line not in md_lines:
                missing_content.append(docx_line)
        
        return len(missing_content) == 0, missing_content
    
    def convert_single_file(self, docx_path: Path) -> bool:
        """Convert a single Word document to Markdown."""
        filename = docx_path.stem
        md_path = self.output_folder / f"{filename}.md"
        error_path = self.output_folder / f"{filename}_errors.txt"
        
        console.print(f"\n[blue]Converting: {docx_path.name}[/blue]")
        
        try:
            # Convert using Pandoc
            cmd = [
                'pandoc',
                str(docx_path),
                '-f', 'docx',
                '-t', 'markdown',
                '-o', str(md_path),
                '--wrap=none',  # Don't wrap lines
                '--markdown-headings=atx'  # Use # style headers
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                error_msg = f"Pandoc conversion failed: {result.stderr}"
                self.log_error(error_path, error_msg)
                console.print(f"[red]❌ Conversion failed[/red]")
                return False
            
            # Verify content
            content_ok, missing_content = self.verify_content(docx_path, md_path)
            
            if not content_ok:
                error_msg = f"Content verification failed. Missing content:\n" + "\n".join(missing_content)
                self.log_error(error_path, error_msg)
                console.print(f"[yellow]⚠️  Content verification failed - check error log[/yellow]")
                return False
            
            console.print(f"[green]✅ Successfully converted to {md_path.name}[/green]")
            return True
            
        except subprocess.TimeoutExpired:
            error_msg = "Conversion timed out after 60 seconds"
            self.log_error(error_path, error_msg)
            console.print(f"[red]❌ Conversion timed out[/red]")
            return False
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.log_error(error_path, error_msg)
            console.print(f"[red]❌ Unexpected error[/red]")
            return False
    
    def log_error(self, error_path: Path, error_msg: str):
        """Log error to file."""
        try:
            with open(error_path, 'w', encoding='utf-8') as f:
                f.write(f"Error converting file:\n{error_msg}\n")
            self.error_logs.append(str(error_path))
        except Exception as e:
            console.print(f"[red]Failed to write error log: {e}[/red]")
    
    def show_file_menu(self, files: List[Path]) -> Optional[Path]:
        """Show interactive menu for file selection."""
        table = Table(title="Available Word Documents")
        table.add_column("Number", style="cyan", no_wrap=True)
        table.add_column("Filename", style="green")
        table.add_column("Size", style="yellow")
        
        for i, file_path in enumerate(files, 1):
            size = file_path.stat().st_size
            size_str = f"{size / 1024:.1f} KB"
            table.add_row(str(i), file_path.name, size_str)
        
        console.print(table)
        
        while True:
            choice = Prompt.ask(
                "Enter file number to convert (or 'q' to quit)",
                default="q"
            )
            
            if choice.lower() == 'q':
                return None
            
            try:
                file_num = int(choice)
                if 1 <= file_num <= len(files):
                    return files[file_num - 1]
                else:
                    console.print("[red]Invalid file number. Please try again.[/red]")
            except ValueError:
                console.print("[red]Please enter a valid number.[/red]")
    
    def batch_convert(self, files: List[Path]) -> Tuple[int, int]:
        """Convert all files in batch."""
        successful = 0
        total = len(files)
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Converting files...", total=total)
            
            for file_path in files:
                progress.update(task, description=f"Converting {file_path.name}...")
                
                if self.convert_single_file(file_path):
                    successful += 1
                
                progress.advance(task)
        
        return successful, total
    
    def run(self):
        """Main application loop."""
        # Check if Pandoc is installed
        if not self.check_pandoc_installed():
            console.print(Panel(
                "[red]Pandoc is not installed or not found in PATH.\n\n"
                "Please install Pandoc:\n"
                "• macOS: brew install pandoc\n"
                "• Windows: Download from https://pandoc.org/installing.html\n"
                "• Linux: sudo apt-get install pandoc[/red]",
                title="Installation Required"
            ))
            return
        
        # Get Word files
        docx_files = self.get_docx_files()
        if not docx_files:
            console.print(Panel(
                f"[yellow]No .docx files found in: {self.input_folder}[/yellow]",
                title="No Files Found"
            ))
            return
        
        # Create output folder
        self.create_output_folder()
        
        # Main menu loop
        while True:
            console.print("\n" + "="*50)
            console.print("[bold blue]Word to Markdown Converter[/bold blue]")
            console.print("="*50)
            console.print(f"Input folder: {self.input_folder}")
            console.print(f"Output folder: {self.output_folder}")
            console.print(f"Found {len(docx_files)} Word document(s)")
            console.print()
            
            console.print("Options:")
            console.print("1. Convert single file")
            console.print("2. Convert all files (batch)")
            console.print("3. View error logs")
            console.print("4. Exit")
            
            choice = Prompt.ask("Select option", choices=["1", "2", "3", "4"], default="1")
            
            if choice == "1":
                selected_file = self.show_file_menu(docx_files)
                if selected_file:
                    self.convert_single_file(selected_file)
                    input("\nPress Enter to continue...")
            
            elif choice == "2":
                if Confirm.ask(f"Convert all {len(docx_files)} files?"):
                    successful, total = self.batch_convert(docx_files)
                    console.print(f"\n[green]Batch conversion complete: {successful}/{total} successful[/green]")
                    if self.error_logs:
                        console.print(f"[yellow]Check error logs for {len(self.error_logs)} failed conversions[/yellow]")
                    input("\nPress Enter to continue...")
            
            elif choice == "3":
                if self.error_logs:
                    console.print("\n[bold]Error Logs:[/bold]")
                    for error_log in self.error_logs:
                        console.print(f"• {Path(error_log).name}")
                else:
                    console.print("\n[yellow]No error logs found.[/yellow]")
                input("\nPress Enter to continue...")
            
            elif choice == "4":
                console.print("\n[green]Goodbye![/green]")
                break

@click.command()
@click.argument('folder', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def main(folder):
    """Convert Microsoft Word documents to Markdown format."""
    converter = WordToMarkdownConverter(folder)
    converter.run()

if __name__ == '__main__':
    main()
