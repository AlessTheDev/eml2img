import base64
import argparse
import os

# Initialize parser
parser = argparse.ArgumentParser(
    description="Parses .eml file(s) to extract image data"
)

def add_options():
    # Mutually exclusive group to allow either single file or folder parsing
    group = parser.add_mutually_exclusive_group(required=True)

    # Group for parsing a single file
    group.add_argument(
        "filename", 
        nargs="?",  # Optional positional argument
        help="Specify a single .eml file to parse"
    )
    
    # Group for parsing a folder
    group.add_argument(
        "--parse-folder", 
        nargs="?",  # Optional folder argument
        const=".",  # Defaults to the current directory if no folder is specified
        default=None,  # Default when --parse-folder is not provided
        help="Specify a folder to parse. Defaults to the current folder if no folder name is provided."
    )

    # Optional output directory for both single file and folder parsing
    parser.add_argument(
        "-o", "--output", 
        help="Specify a destination folder for output images."
    )

def main():
    add_options()
    args = parser.parse_args()

    output_folder = args.output

    if args.parse_folder:
        parse_folder(args.parse_folder, output_folder)
    else:
        with open(args.filename, 'r') as file:
            parse_file(file, output_folder)

def parse_folder(folder_name, output_folder):
    if output_folder is None:
        output_folder = "."
        
    for root, _, files in os.walk(folder_name):
        for file in files:
            if file.endswith(".eml"):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as eml_file:
                    parse_file(eml_file, os.path.join(output_folder, extract_file_name_no_extension(eml_file.name)))

def parse_file(file, output_folder):
    # Create the output folder if not provided
    if output_folder is None:
        output_folder = extract_file_name_no_extension(file.name)

    os.makedirs(output_folder, exist_ok=True)

    boundary = ""
    has_found_image = False
    is_reading_image_data = False
    image_name = ""
    image_content = ""

    for line in file:
        # Detect boundary for multipart sections
        if 'Content-Type: multipart/related;' in line:
            boundary = extract_boundary(line)
            continue
        
        # Check for end of an image section based on boundary
        if is_reading_image_data and line.startswith(boundary):
            # Save the content to file
            image_path = os.path.join(output_folder, image_name)
            save_image(image_path, image_content)

            has_found_image = False
            is_reading_image_data = False
            continue

        if is_reading_image_data:
            image_content += line
        
        if 'Content-Type: image/png;' in line:
            image_name = extract_image_name(line)
            has_found_image = True
            is_reading_image_data = False
            image_content = ""
        
        if has_found_image and len(line.split()) == 0:  # Base64 data is between empty lines
            is_reading_image_data = True

def extract_file_name_no_extension(file_name):
    """Removes the file extension from the file name"""
    return os.path.splitext(file_name)[0]

def extract_boundary(str):
    """Extracts the boundary string from the Content-Type header"""
    try:
        return '--' + str.split('boundary="')[1].split('"')[0]
    except IndexError:
        print("Error: Could not find boundary in Content-Type.")
        return ""

def save_image(path, content):
    """Saves the Base64-decoded image content to a file"""
    try:
        with open(path, "wb") as image_file:
            image_file.write(base64.b64decode(content))
            print(f"Extracted image: {path}")
    except Exception as e:
        print(f"Error saving image: {e}")

def extract_image_name(line):
    """Extracts the image file name from the Content-Type header"""
    try:
        return line.split('; ')[1].split('"')[1]  # name="image.png"
    except IndexError:
        print("Error: Could not extract image name.")
        return "unknown_image.png" 

main()
