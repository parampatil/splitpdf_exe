import tkinter as tk
from tkinter import filedialog, messagebox

# Global variables
input_path = ''
output_path = ''
config_path = ''


def select_input_folder():
    global input_path
    input_path = filedialog.askdirectory()
    input_folder_var.set(input_path)


def select_output_folder():
    global output_path
    output_path = filedialog.askdirectory()
    output_folder_var.set(output_path)


def select_config_file():
    global config_path
    config_path = filedialog.askopenfilename(
        filetypes=[('Config Files', '*.cfg')])
    config_file_var.set(config_path)


def split_pdf():
    if not input_path or not output_path or not config_path:
        messagebox.showwarning(
            'Warning', 'Please select input folder, output folder, and config file.')
        return

    # Read the config file with UTF-8 encoding
    import configparser
    config = configparser.ConfigParser()
    with open(config_path, 'r', encoding='utf-8') as f:
        config.read_file(f)

    input_folder = config['Files']['INPUT']
    output_folder = config['Files']['OUTPUT']
    OCR_Text1 = config['OCR']['Text1']
    OCR_Loc1 = config['OCR']['Loc1']
    OCR_Text2 = config['OCR']['Text2']
    OCR_Loc2 = config['OCR']['Loc2']
    OCR_Text3 = config['OCR']['Text3']
    OCR_Loc3 = config['OCR']['Loc3']

    print("Input folder selected: ", input_folder)
    print("Output folder selected: ", output_folder)
    print("OCR_Text1: ",  OCR_Text1)
    print("OCR_Loc1: ",   OCR_Loc1)
    print("OCR_Text2: ", OCR_Text2)
    print("OCR_Loc2: ",   OCR_Loc2)
    print("OCR_Text3: ", OCR_Text2)
    print("OCR_Loc3: ",   OCR_Loc3)

    # Continue with the rest of the function...


# GUI setup
root = tk.Tk()
root.title('PDF Splitter')
root.geometry('800x800')  # Set initial width and height of the window

# Add padding to the window
padding = 20
root.configure(padx=padding, pady=padding)

# Set background colors
bg_color = '#f0f0f0'  # Light gray
entry_bg_color = '#ffffff'  # White

input_folder_var = tk.StringVar()
output_folder_var = tk.StringVar()
config_file_var = tk.StringVar()

# Input Folder
tk.Label(root, text='Input Folder:', bg=bg_color).pack()
input_folder_entry = tk.Entry(
    root, textvariable=input_folder_var, state='disabled', bg=entry_bg_color)
input_folder_entry.pack(fill=tk.X, padx=padding, pady=(0, padding))

tk.Button(root, text='Select Input Folder', command=select_input_folder).pack(
    fill=tk.X, padx=padding, pady=(0, padding))

# Output Folder
tk.Label(root, text='Output Folder:', bg=bg_color).pack()
output_folder_entry = tk.Entry(
    root, textvariable=output_folder_var, state='disabled', bg=entry_bg_color)
output_folder_entry.pack(fill=tk.X, padx=padding, pady=(0, padding))

tk.Button(root, text='Select Output Folder', command=select_output_folder).pack(
    fill=tk.X, padx=padding, pady=(0, padding))

# Config File
tk.Label(root, text='Config File:', bg=bg_color).pack()
config_file_entry = tk.Entry(
    root, textvariable=config_file_var, state='disabled', bg=entry_bg_color)
config_file_entry.pack(fill=tk.X, padx=padding, pady=(0, padding))

tk.Button(root, text='Select Config File', command=select_config_file).pack(
    fill=tk.X, padx=padding, pady=(0, padding))

# Split PDF Button
split_button = tk.Button(root, text='Split PDF',
                         command=split_pdf, bg='lightgreen')
split_button.pack(fill=tk.X, padx=padding, pady=(padding, 0))

root.mainloop()
