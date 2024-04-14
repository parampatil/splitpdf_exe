import re
import os
import sys
import time

# Imports for Splitting PDF
import configparser
from PIL import Image, ImageDraw
from pytesseract import Output, image_to_data
import pdf2image
from PyPDF2 import PdfReader, PdfWriter

# Imports for GUI
import tkinter as tk
from tkinter import filedialog

# ################ CONFIGURATION SECTION #####################

# current_dir = os.getcwd()

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Relative path to the Poppler bin directory within the project
poppler_rel_path = r'Release-24.02.0-0\poppler-24.02.0\Library\bin'
tesseract_rel_path = r'Tesseract-OCR'

# # Construct the absolute path to the Poppler bin directory
# poppler_abs_path = os.path.join(current_dir, poppler_rel_path)
poppler_abs_path = resource_path(poppler_rel_path)
# tesseract_abs_path = os.path.join(current_dir, tesseract_rel_path)
tesseract_abs_path = resource_path(tesseract_rel_path)

# # Add Poppler bin directory to the PATH environment variable
os.environ['PATH'] += os.pathsep + poppler_abs_path
os.environ['PATH'] += os.pathsep + tesseract_abs_path

# ############## GUI for Config Creator ##########################

# Function to save configuration file
def save_config(filename, config):
    with open(filename, 'w') as configfile:
        config.write(configfile)

# Function to browse and select folder
def browse_folder(entry):
    foldername = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, foldername)

# Create GUI
def create_gui():
    gui = tk.Tk()
    gui.title("PDF Splitter")
    gui.geometry('800x800')  # Set initial width and height of the window

    # Add background color
    gui.configure(bg='#F0F0F0')

    # Declare Entry variables as global
    global input_entry, output_entry, text1_entry, loc1_entry, text2_entry, loc2_entry, text3_entry, loc3_entry
    # Function to save configuration
    def save_and_generate():
        # Create a new configuration
        config = configparser.ConfigParser()

        # Update configuration based on user input
        config['Files'] = {
            'INPUT': input_entry.get(),
            'OUTPUT': output_entry.get()
        }

        config['OCR'] = {
            'Text1': text1_entry.get(),
            'Loc1': loc1_entry.get(),
            'Text2': text2_entry.get(),
            'Loc2': loc2_entry.get(),
            'Text3': text3_entry.get(),
            'Loc3': loc3_entry.get()
        }

        # Save configuration
        save_config('sample.cfg', config)
        gui.destroy()
        next_function()

    # Input folder entry
    input_frame = tk.Frame(gui, bg='#F0F0F0', padx=10, pady=10)
    input_frame.grid(row=0, column=0, sticky='w')
    tk.Label(input_frame, text="Input Folder:", bg='#F0F0F0').pack(side='left')
    input_entry = tk.Entry(input_frame, width=50)
    input_entry.pack(side='left', padx=(0, 5), ipady=2)
    input_button = tk.Button(input_frame, text="Browse", command=lambda: browse_folder(input_entry))
    input_button.pack(side='left', padx=5)

    # Output folder entry
    output_frame = tk.Frame(gui, bg='#F0F0F0', padx=10, pady=10)
    output_frame.grid(row=1, column=0, sticky='w')
    tk.Label(output_frame, text="Output Folder:", bg='#F0F0F0').pack(side='left')
    output_entry = tk.Entry(output_frame, width=50)
    output_entry.pack(side='left', padx=(0, 5), ipady=2)
    output_button = tk.Button(output_frame, text="Browse", command=lambda: browse_folder(output_entry))
    output_button.pack(side='left', padx=5)

    # OCR settings
    ocr_frame = tk.Frame(gui, bg='#F0F0F0', padx=10, pady=10)
    ocr_frame.grid(row=2, columnspan=2, sticky='w')
    tk.Label(ocr_frame, text="OCR Settings:", bg='#F0F0F0', font=('Arial', 14, 'bold'), pady=10).pack(side='top')

    entry_frame1 = tk.Frame(ocr_frame, bg='#F0F0F0')
    entry_frame1.pack(anchor='w', pady=5)
    tk.Label(entry_frame1, text="Text1:", bg='#F0F0F0').pack(side='left')
    text1_entry = tk.Entry(entry_frame1, width=50)
    text1_entry.pack(side='left', padx=(0, 5), ipady=2)
    tk.Label(entry_frame1, text="Loc1:", bg='#F0F0F0').pack(side='left')
    loc1_entry = tk.Entry(entry_frame1, width=50)
    loc1_entry.pack(side='left', padx=(0, 5), ipady=2)

    entry_frame2 = tk.Frame(ocr_frame, bg='#F0F0F0')
    entry_frame2.pack(anchor='w', pady=5)
    tk.Label(entry_frame2, text="Text2:", bg='#F0F0F0').pack(side='left')
    text2_entry = tk.Entry(entry_frame2, width=50)
    text2_entry.pack(side='left', padx=(0, 5), ipady=2)
    tk.Label(entry_frame2, text="Loc2:", bg='#F0F0F0').pack(side='left')
    loc2_entry = tk.Entry(entry_frame2, width=50)
    loc2_entry.pack(side='left', padx=(0, 5), ipady=2)

    entry_frame3 = tk.Frame(ocr_frame, bg='#F0F0F0')
    entry_frame3.pack(anchor='w', pady=5)
    tk.Label(entry_frame3, text="Text3:", bg='#F0F0F0').pack(side='left')
    text3_entry = tk.Entry(entry_frame3, width=50)
    text3_entry.pack(side='left', padx=(0, 5), ipady=2)
    tk.Label(entry_frame3, text="Loc3:", bg='#F0F0F0').pack(side='left')
    loc3_entry = tk.Entry(entry_frame3, width=50)
    loc3_entry.pack(side='left', padx=(0, 5), ipady=2)

    def skip_generation():
        gui.destroy()
        next_function()

    # Save and Generate button
    generate_button = tk.Button(gui, text="Save and Generate PDFs", command=save_and_generate, bg='#0078D7', fg='white', padx=10, pady=5)
    generate_button.grid(row=3, columnspan=2, pady=20)

    # Skip Generation button
    skip_button = tk.Button(gui, text="Skip Generation", command=skip_generation, bg='#FF5733', fg='white', padx=10, pady=5)
    skip_button.grid(row=4, columnspan=2, pady=10)

    gui.mainloop()

def display_completion():
    completion_gui = tk.Tk()
    completion_gui.title("PDF Splitting Completed")
    completion_gui.geometry('400x100')
    completion_gui.configure(bg='#F0F0F0')
    tk.Label(completion_gui, text="PDF Splitting Completed", bg='#F0F0F0', font=('Arial', 16, 'bold'), pady=20).pack()
    completion_gui.mainloop()

# Function to skip generation


def next_function():
    # Call the next function in your main script
    start_time = time.time()
    main()

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
    
    display_completion()

# ############## Functions for PDF Handling #######################

def extract_images(source_pdf_path):
    images = pdf2image.convert_from_path(source_pdf_path, dpi=400)
    return images


def run_OCR(image, search_area):
    # search_area: (top_left_x, top_left_y, bottom_right_x, bottom_right_y)
    cropped_im = image.crop(tuple(search_area))
    ocr_dict = image_to_data(cropped_im, lang='eng', output_type=Output.DICT)
    return ocr_dict['text']

# Check what sub-document this page belongs to, and return the document name


def find_subDocument(image, text_dict, loc_dict):
    for key in text_dict.keys():
        image_data = run_OCR(image, loc_dict[f'loc{key[-1]}'])
        for word in image_data:
            if text_dict[key].lower() == word.lower():
                return text_dict[key]
    return None

def reduce_subdocument(subdocuments):
    reduced_data = {}
    current_key = None
    for key, value in subdocuments.items():
        if value is not None:
            if value in reduced_data:
                reduced_data[value].append(key)
            else:
                reduced_data[value] = [key]
            current_key = value
        elif current_key is not None:
            if current_key in reduced_data:
                reduced_data[current_key].append(key)
            else:
                reduced_data[current_key] = [key]

    return reduced_data

def save_documents(reduce_subdocuments, source_pdf_path, defendant_id, output_path):
    with open(source_pdf_path, 'rb') as input_file:
        pdf_reader = PdfReader(input_file)
        
        for documents, page_list in reduce_subdocuments.items():
            pdf_writer = PdfWriter()

            for page_num in page_list:
                pdf_writer.add_page(pdf_reader.pages[page_num])
            
            output_file_name = os.path.join(output_path, f"{defendant_id}_{documents.capitalize()}.pdf")
            with open(output_file_name, 'wb') as output_file:
                pdf_writer.write(output_file)


def preview_image(image, search_area):
    # Draw a rectangle on the image
    draw = ImageDraw.Draw(image)
    draw.rectangle(search_area, outline="blue", width=3)

    # Display the image with the drawn rectangle (optional)
    image.show()


def read_config(config_file_path):
    config = configparser.ConfigParser()

    with open(config_file_path, 'r', encoding='utf-8') as f:
        config.read_file(f)
    input_path = config['Files']['INPUT']
    output_path = config['Files']['OUTPUT']
    text = {}
    loc = {}
    for key in config['OCR']:
        if key.startswith('text'):  # Check if key starts with "Text"
            text_str = config.get('OCR', key)
            text[key] = re.sub(r'\W+', '', text_str)

        elif key.startswith('loc'):
            location_str = config.get('OCR', key)
            location = [int(x) for x in location_str.split(',')]
            loc[key] = location

        else:
            raise ValueError(f"Unexpected key '{key}' in 'OCR' section. "
                             "Expected keys to start with 'Text'.")

    return input_path,output_path,text, loc


def main():
    config_file_path = "Sample.cfg"
    input_folder, output_path, text_dict, loc_dict = read_config(config_file_path)
    

    if os.path.exists(input_folder) and os.path.exists(output_path):
        print("Folder exists!",input_folder, output_path)
    else:
        print("Folder does not exist or path is incorrect.")
    files_in_folder = os.listdir(input_folder)
    pdf_files = [file for file in files_in_folder if file.lower().endswith('.pdf')]

    print("Number of PDF Files: ", len(pdf_files))

    for pdf in pdf_files:
        source_pdf_path = os.path.join(input_folder, pdf)

        # Find defendant name
        defendant_id, file_extension = pdf.split('.')

        
        images = extract_images(source_pdf_path)
        subdocuments = {}

        #  Process each page of PDF file and find the document name on each page
        for page_no, image in enumerate(images):
            document_name = find_subDocument(image, text_dict, loc_dict)
            subdocuments[page_no] = document_name
                
        # Group pages by  their corresponding documents name
        reduce_subdocuments = reduce_subdocument(subdocuments)

        # Split and save the pdf in outputs folder
        save_documents(reduce_subdocuments, source_pdf_path, defendant_id, output_path)

if __name__ == "__main__":
        create_gui()