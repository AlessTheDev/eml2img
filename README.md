# eml2img

`eml2img` is a Python-based tool that extracts images from `.eml` files, commonly used for email messages. This utility scans `.eml` files or entire folders containing `.eml` files to extract image data encoded in Base64 format and saves them as image files. It supports extracting images from both individual files and directories, with options to specify output directories.

## Features
- Extracts images from individual `.eml` files or entire directories.
- Supports Base64-decoded images.
- Allows specifying custom output directories.
- Easily adaptable for automation or batch processing.

## Requirements
- Python 3.x
- Base64 decoding support (standard Python library).

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/AlessTheDev/eml2img.git
   ```

2. Add the folder containing the repository to your system's PATH environment variable to use the `eml2img` command globally.

   ### For Windows:
   - Open the Start menu, search for "Environment Variables," and select "Edit the system environment variables."
   - Click on "Environment Variables," then find "Path" under "System Variables," and click "Edit."
   - Add the full path to the cloned repository folder to the list.

   ### For Mac/Linux:
   - Haven't created a guide for those yet, but you can translate the code of the `email2img.bat` file or contribute to the repo.

## Usage

### 1. Display Help
Use the help command to view all available options and their descriptions:

```bash
eml2img -h
```

### 2. Parse a Single `.eml` File

Extract images from a single `.eml` file and save them to a folder based on the filename:

```bash
eml2img ./email.eml
```
> This command will extract images into a folder named `./email` by default.

#### Specify the Output Directory

To extract the images into a specific folder, use the `-o` option:

```bash
eml2img ./email.eml -o ./OutputDir
```

Alternatively, you can extract the images directly into the current directory:

```bash
eml2img ./email.eml -o .
```

### 3. Parse All `.eml` Files in a Directory

Scan an entire directory to extract images from all `.eml` files within:

```bash
eml2img --parse-folder
```
> This will scan the current directory for `.eml` files and extract images to folders named after each email file.

#### Scan a Specific Directory

To scan a specific directory, provide the path:

```bash
eml2img --parse-folder ./DirToScan
```

#### Specify an Output Directory for Folder Parsing

You can also specify a custom output directory for the extracted images:

```bash
eml2img --parse-folder ./DirToScan -o ./OutputDir
```

## How it Works

1. The tool detects and parses `.eml` files for `Content-Type: image/png;` or other image types.
2. Images are Base64-decoded and saved in the specified output directory.
3. For multipart `.eml` files, boundaries are detected and used to extract individual images.

## Example Scenarios

### Extracting Images from Multiple Emails

If you have a folder full of `.eml` files and you want to extract all images to a single directory:

```bash
eml2img --parse-folder ./Emails -o ./AllImages
```

This will scan all `.eml` files in the `./Emails` directory and save any extracted images to the `./AllImages` folder.

### Frames Extraction for Game Development
You can also use eml2img to automate tasks like extracting image frames from .eml files for game development projects like I do ;).
For example, if you need to extract sprite frames for a game, you can create a batch file to automate the process and place the frames into their respective project directories.
Here’s a sample batch script (framesToUndercup.bat) for extracting frames and saving them into the asset directory for my game:

```batch
:: framesToUndercup.bat
:: Run this in a folder containing the "just downloaded" .eml files
eml2img --parse-folder . -o D:\Projects\Cupflow\Undercup\Assets\Sprites %1
```

Usage:
To extract all frames for a specific game asset (e.g., "Player"), run:
```batch
framesToUndercup Player
```

This will extract all frames into the Player folder inside your game project directory `D:\Projects\Cupflow\Undercup\Assets\Sprites\Player`.