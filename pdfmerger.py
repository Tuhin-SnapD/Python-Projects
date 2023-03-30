# This code uses the Python library PyPDF2 to merge multiple PDF files into a single PDF file.

# PyPDF2 is a pure-python PDF library that allows manipulation of PDFs, including merging, splitting, cropping, and transforming pages. It is built on top of the lower-level PDFMiner library and provides a high-level interface for working with PDF documents.

# First, a list of PDF file names is created. Then, a PdfMerger object is initialized from PyPDF2.

# A for loop iterates over each file name in the list. For each file, the code opens the file using open function in "rb" (read binary) mode and creates a PdfReader object using PyPDF2.

# The append method of the PdfMerger object is called with the PdfReader object as an argument. This appends the contents of the PdfReader object to the PdfMerger object.

# After the loop is complete, the code closes the PDF files and writes the merged PDF to disk using the write method of the PdfMerger object.

# Import necessary modules
import PyPDF2

# List of PDF files to merge
pdfiles = ["1.pdf", "2.pdf"]

# Create PdfMerger object
merger = PyPDF2.PdfMerger()

# Loop through PDF files and append them to merger object
for filename in pdfiles:
    with open(filename, 'rb') as pdfFile:
        merger.append(PyPDF2.PdfReader(pdfFile))

# Write merged PDF file to disk
with open('merged.pdf', 'wb') as mergedPdf:
    merger.write(mergedPdf)