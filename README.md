pip install -r requirements.txt

# Universal Metadata Cleaner

A simple, cross-platform GUI tool to remove metadata from common file types, including images, PDFs, Office documents, and videos. Designed for privacy and security, this tool helps you clean sensitive metadata before sharing files.

## Features
- **Batch or single file cleaning**
- Supports:
  - Images: JPG, JPEG, PNG
  - PDF documents
  - Microsoft Office: DOCX, XLSX, PPTX
  - Videos: MP4, MOV
- Simple graphical interface (Tkinter)
- Logs all actions to a file in your Documents folder
- Handles missing dependencies gracefully

## Requirements
- Python 3.7+
- Dependencies (see `requirements.txt`):
  - Pillow
  - piexif
  - pikepdf
  - python-docx
  - openpyxl
  - python-pptx
- [ffmpeg](https://ffmpeg.org/) (for video cleaning, must be in your PATH)

## Installation
1. Clone or download this repository.
2. Install Python dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. (Optional) Install ffmpeg for video support:
   - [Download ffmpeg](https://ffmpeg.org/download.html) and add it to your system PATH.

## Usage
1. Run the tool:
   ```sh
   python metadata_cleaner.py
   ```
2. Use the GUI to select files or folders to clean.
3. Cleaned files will be saved with `_clean` appended to the filename, or to a folder you select.
4. See the log file in your Documents folder (`metadata-log.txt`) for details.

## Notes
- The tool does **not** overwrite your original files.
- If a required Python package is missing, you will be prompted to install it.
- For video files, ensure ffmpeg is installed and accessible from your command line.

## License
MIT License

## Disclaimer
This tool is provided as-is. Always verify that metadata has been removed to your satisfaction before sharing sensitive files.
