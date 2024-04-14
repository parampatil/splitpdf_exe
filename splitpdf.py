import re
import configparser
from PIL import Image, ImageDraw
from pytesseract import Output, image_to_data
import pdf2image
from PyPDF2 import PdfReader, PdfWriter
import os
import time
current_dir = os.getcwd()

# Relative path to the Poppler bin directory within the project
poppler_rel_path = r'Release-24.02.0-0\poppler-24.02.0\Library\bin'
tesseract_rel_path = r'Tesseract-OCR'

# Construct the absolute path to the Poppler bin directory
poppler_abs_path = os.path.join(current_dir, poppler_rel_path)
tesseract_abs_path = os.path.join(current_dir, tesseract_rel_path)

# Add Poppler bin directory to the PATH environment variable
os.environ['PATH'] += os.pathsep + poppler_abs_path
os.environ['PATH'] += os.pathsep + tesseract_abs_path


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
            
            output_file_name = os.path.join(output_path, f"{defendant_id}_{documents}.pdf")
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

    return text, loc


def main():
    # Get a list of all files in the folder
    input_folder = r"Firm1/Cases"
    output_path = r"Firm1/Out"
    config_file_path = "Sample.cfg"

    if os.path.exists(input_folder) and os.path.exists(output_path):
        print("Folder exists!")
    else:
        print("Folder does not exist or path is incorrect.")
    files_in_folder = os.listdir(input_folder)
    pdf_files = [file for file in files_in_folder if file.lower().endswith('.pdf')]

    for pdf in pdf_files:
        source_pdf_path = os.path.join(input_folder, pdf)

        # Find defendant name
        defendant_id, file_extension = pdf.split('.')

        text_dict, loc_dict = read_config(config_file_path)
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
    main()
