"""
Enhanced PDF Merger

A comprehensive PDF merging tool with GUI interface, progress tracking,
file validation, and advanced merging options.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from typing import List, Optional
import PyPDF2
from PyPDF2 import PdfReader, PdfWriter
import threading
import time


class PDFMerger:
    """Enhanced PDF merger with GUI and advanced features."""
    
    def __init__(self):
        self.pdf_files = []
        self.output_file = ""
        self.root = None
        self.progress_var = None
        self.status_var = None
        
    def validate_pdf(self, file_path: str) -> bool:
        """Validate if a file is a valid PDF."""
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                if len(reader.pages) == 0:
                    return False
            return True
        except Exception:
            return False
    
    def get_pdf_info(self, file_path: str) -> dict:
        """Get information about a PDF file."""
        try:
            with open(file_path, 'rb') as file:
                reader = PdfReader(file)
                return {
                    'pages': len(reader.pages),
                    'size': os.path.getsize(file_path),
                    'filename': os.path.basename(file_path)
                }
        except Exception as e:
            return {'error': str(e)}
    
    def merge_pdfs_simple(self, input_files: List[str], output_file: str) -> bool:
        """Simple PDF merging using PyPDF2."""
        try:
            merger = PdfWriter()
            
            for i, file_path in enumerate(input_files):
                with open(file_path, 'rb') as file:
                    reader = PdfReader(file)
                    for page in reader.pages:
                        merger.add_page(page)
                
                # Update progress
                if self.progress_var:
                    progress = ((i + 1) / len(input_files)) * 100
                    self.progress_var.set(progress)
                    self.root.update_idletasks()
            
            with open(output_file, 'wb') as output:
                merger.write(output)
            
            return True
            
        except Exception as e:
            if self.status_var:
                self.status_var.set(f"Error: {str(e)}")
            return False
    
    def merge_pdfs_advanced(self, input_files: List[str], output_file: str, 
                           page_ranges: Optional[List[str]] = None) -> bool:
        """Advanced PDF merging with page range support."""
        try:
            merger = PdfWriter()
            
            for i, file_path in enumerate(input_files):
                with open(file_path, 'rb') as file:
                    reader = PdfReader(file)
                    
                    if page_ranges and i < len(page_ranges) and page_ranges[i]:
                        # Parse page range (e.g., "1-5,7,9-12")
                        pages_to_add = self.parse_page_range(page_ranges[i], len(reader.pages))
                        for page_num in pages_to_add:
                            if 0 <= page_num < len(reader.pages):
                                merger.add_page(reader.pages[page_num])
                    else:
                        # Add all pages
                        for page in reader.pages:
                            merger.add_page(page)
                
                # Update progress
                if self.progress_var:
                    progress = ((i + 1) / len(input_files)) * 100
                    self.progress_var.set(progress)
                    self.root.update_idletasks()
            
            with open(output_file, 'wb') as output:
                merger.write(output)
            
            return True
            
        except Exception as e:
            if self.status_var:
                self.status_var.set(f"Error: {str(e)}")
            return False
    
    def parse_page_range(self, range_str: str, max_pages: int) -> List[int]:
        """Parse page range string into list of page numbers."""
        pages = []
        try:
            parts = range_str.split(',')
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start, end = part.split('-')
                    start = int(start.strip()) - 1  # Convert to 0-based
                    end = int(end.strip()) - 1
                    pages.extend(range(start, end + 1))
                else:
                    page = int(part.strip()) - 1  # Convert to 0-based
                    pages.append(page)
            
            # Filter valid pages
            pages = [p for p in pages if 0 <= p < max_pages]
            return pages
        except:
            return list(range(max_pages))  # Return all pages if parsing fails
    
    def create_gui(self):
        """Create the GUI interface."""
        self.root = tk.Tk()
        self.root.title("📄 Enhanced PDF Merger")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Enhanced PDF Merger", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File list frame
        list_frame = ttk.LabelFrame(main_frame, text="PDF Files", padding="10")
        list_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # File list
        self.file_listbox = tk.Listbox(list_frame, height=10)
        self.file_listbox.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        # Scrollbar for file list
        file_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.file_listbox.yview)
        file_scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=file_scrollbar.set)
        
        # File list buttons
        file_btn_frame = ttk.Frame(list_frame)
        file_btn_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(file_btn_frame, text="Add Files", command=self.add_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(file_btn_frame, text="Remove Selected", command=self.remove_file).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(file_btn_frame, text="Clear All", command=self.clear_files).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(file_btn_frame, text="Move Up", command=self.move_up).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(file_btn_frame, text="Move Down", command=self.move_down).pack(side=tk.LEFT)
        
        # File info frame
        info_frame = ttk.LabelFrame(main_frame, text="File Information", padding="10")
        info_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        info_frame.columnconfigure(1, weight=1)
        
        self.info_text = tk.Text(info_frame, height=4, wrap=tk.WORD)
        self.info_text.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        info_scrollbar = ttk.Scrollbar(info_frame, orient=tk.VERTICAL, command=self.info_text.yview)
        info_scrollbar.grid(row=0, column=2, sticky=(tk.N, tk.S))
        self.info_text.configure(yscrollcommand=info_scrollbar.set)
        
        # Output file frame
        output_frame = ttk.LabelFrame(main_frame, text="Output File", padding="10")
        output_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        output_frame.columnconfigure(1, weight=1)
        
        ttk.Label(output_frame, text="Output:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.output_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.output_var, state='readonly').grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(0, 10))
        ttk.Button(output_frame, text="Browse", command=self.select_output).grid(row=0, column=2)
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(progress_frame, textvariable=self.status_var).grid(row=1, column=0, sticky=tk.W)
        
        # Merge button
        merge_frame = ttk.Frame(main_frame)
        merge_frame.grid(row=5, column=0, columnspan=3, pady=(10, 0))
        
        ttk.Button(merge_frame, text="Merge PDFs", command=self.merge_pdfs, 
                  style='Accent.TButton').pack()
        
        # Bind events
        self.file_listbox.bind('<<ListboxSelect>>', self.on_file_select)
        
        # Configure grid weights for main frame
        main_frame.rowconfigure(1, weight=1)
    
    def add_files(self):
        """Add PDF files to the list."""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        for file_path in files:
            if file_path not in self.pdf_files:
                if self.validate_pdf(file_path):
                    self.pdf_files.append(file_path)
                    self.file_listbox.insert(tk.END, os.path.basename(file_path))
                else:
                    messagebox.showerror("Error", f"Invalid PDF file: {os.path.basename(file_path)}")
        
        self.update_info()
    
    def remove_file(self):
        """Remove selected file from the list."""
        selection = self.file_listbox.curselection()
        if selection:
            index = selection[0]
            self.file_listbox.delete(index)
            self.pdf_files.pop(index)
            self.update_info()
    
    def clear_files(self):
        """Clear all files from the list."""
        self.file_listbox.delete(0, tk.END)
        self.pdf_files.clear()
        self.update_info()
    
    def move_up(self):
        """Move selected file up in the list."""
        selection = self.file_listbox.curselection()
        if selection and selection[0] > 0:
            index = selection[0]
            # Move in listbox
            text = self.file_listbox.get(index)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index - 1, text)
            self.file_listbox.selection_set(index - 1)
            
            # Move in pdf_files list
            self.pdf_files[index], self.pdf_files[index - 1] = self.pdf_files[index - 1], self.pdf_files[index]
    
    def move_down(self):
        """Move selected file down in the list."""
        selection = self.file_listbox.curselection()
        if selection and selection[0] < len(self.pdf_files) - 1:
            index = selection[0]
            # Move in listbox
            text = self.file_listbox.get(index)
            self.file_listbox.delete(index)
            self.file_listbox.insert(index + 1, text)
            self.file_listbox.selection_set(index + 1)
            
            # Move in pdf_files list
            self.pdf_files[index], self.pdf_files[index + 1] = self.pdf_files[index + 1], self.pdf_files[index]
    
    def select_output(self):
        """Select output file location."""
        output_file = filedialog.asksaveasfilename(
            title="Save Merged PDF As",
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if output_file:
            self.output_var.set(output_file)
            self.output_file = output_file
    
    def on_file_select(self, event):
        """Handle file selection event."""
        self.update_info()
    
    def update_info(self):
        """Update file information display."""
        selection = self.file_listbox.curselection()
        self.info_text.delete(1.0, tk.END)
        
        if selection:
            index = selection[0]
            file_path = self.pdf_files[index]
            info = self.get_pdf_info(file_path)
            
            if 'error' not in info:
                self.info_text.insert(tk.END, f"File: {info['filename']}\n")
                self.info_text.insert(tk.END, f"Pages: {info['pages']}\n")
                self.info_text.insert(tk.END, f"Size: {info['size']:,} bytes\n")
            else:
                self.info_text.insert(tk.END, f"Error reading file: {info['error']}")
        else:
            total_pages = sum(self.get_pdf_info(f).get('pages', 0) for f in self.pdf_files)
            total_size = sum(self.get_pdf_info(f).get('size', 0) for f in self.pdf_files)
            self.info_text.insert(tk.END, f"Total files: {len(self.pdf_files)}\n")
            self.info_text.insert(tk.END, f"Total pages: {total_pages}\n")
            self.info_text.insert(tk.END, f"Total size: {total_size:,} bytes")
    
    def merge_pdfs(self):
        """Merge the selected PDF files."""
        if not self.pdf_files:
            messagebox.showerror("Error", "No PDF files selected!")
            return
        
        if not self.output_file:
            messagebox.showerror("Error", "No output file selected!")
            return
        
        # Disable merge button during operation
        for widget in self.root.winfo_children():
            if isinstance(widget, ttk.Button) and widget.cget('text') == "Merge PDFs":
                widget.configure(state='disabled')
        
        # Run merge in separate thread
        thread = threading.Thread(target=self._merge_thread)
        thread.daemon = True
        thread.start()
    
    def _merge_thread(self):
        """Merge PDFs in a separate thread."""
        try:
            self.status_var.set("Merging PDFs...")
            self.progress_var.set(0)
            
            success = self.merge_pdfs_simple(self.pdf_files, self.output_file)
            
            if success:
                self.status_var.set("Merge completed successfully!")
                self.progress_var.set(100)
                messagebox.showinfo("Success", f"PDFs merged successfully!\nOutput: {self.output_file}")
            else:
                self.status_var.set("Merge failed!")
                messagebox.showerror("Error", "Failed to merge PDFs!")
                
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        finally:
            # Re-enable merge button
            for widget in self.root.winfo_children():
                if isinstance(widget, ttk.Button) and widget.cget('text') == "Merge PDFs":
                    widget.configure(state='normal')
    
    def run(self):
        """Run the PDF merger application."""
        self.create_gui()
        self.root.mainloop()


def main():
    """Main function to start the PDF merger."""
    try:
        merger = PDFMerger()
        merger.run()
    except Exception as e:
        print(f"Error starting PDF Merger: {e}")
        # Fallback to command line interface
        run_cli_merger()


def run_cli_merger():
    """Fallback command line interface."""
    print("📄 PDF Merger (Command Line)")
    print("=" * 30)
    
    # Get input files
    print("Enter PDF file paths (one per line, empty line to finish):")
    pdf_files = []
    while True:
        file_path = input().strip()
        if not file_path:
            break
        if os.path.exists(file_path) and file_path.lower().endswith('.pdf'):
            pdf_files.append(file_path)
        else:
            print(f"Invalid file: {file_path}")
    
    if not pdf_files:
        print("No valid PDF files provided.")
        return
    
    # Get output file
    output_file = input("Enter output file path: ").strip()
    if not output_file:
        output_file = "merged.pdf"
    
    # Merge PDFs
    print("Merging PDFs...")
    merger = PDFMerger()
    success = merger.merge_pdfs_simple(pdf_files, output_file)
    
    if success:
        print(f"✅ PDFs merged successfully! Output: {output_file}")
    else:
        print("❌ Failed to merge PDFs.")


if __name__ == "__main__":
    main()