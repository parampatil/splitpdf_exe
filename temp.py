import os

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

import pdf2image
from pytesseract import Output, image_to_data
from PIL import Image, ImageDraw

pdf_path = "123456.pdf"

images = pdf2image.convert_from_path(pdf_path)

pil_im = images[0] # assuming that we're interested in the first page only
# pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR'

# Define the coordinates of the rectangle (top-left-x, top-left-y, bottom-right-x, bottom-right-y)
# Example coordinates (adjust these according to your requirements)
# top_left_x = 668
top_left_x = 348
# top_left_y = 1112
top_left_y = 581
# bottom_right_x = 2740
bottom_right_x = 1367
# bottom_right_y = 1390
bottom_right_y = 706

# Draw a rectangle on the image
draw = ImageDraw.Draw(pil_im)
draw.rectangle([top_left_x, top_left_y, bottom_right_x, bottom_right_y], outline="red", width=2)

# Display the image with the drawn rectangle (optional)
pil_im.show()

# Crop the image to the specified coordinates
cropped_im = pil_im.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))


ocr_dict = image_to_data(cropped_im, lang='eng', output_type=Output.DICT)
# ocr_dict now holds all the OCR info including text and location on the image

text = " ".join(ocr_dict['text'])

print(text)