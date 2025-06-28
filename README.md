# Universal Metadata Cleaner

🚀 A Python app that strips metadata from images, PDFs, Office docs, and videos.  
Auto-detects file type and cleans with the right method.

## Features
- Strips EXIF, GPS, thumbnails from images (JPEG/PNG).
- Clears author, title, subject, producer from PDFs.
- Clears core and custom properties in DOCX, XLSX, PPTX.
- Attempts to wipe container tags in MP4/MOV.
- Batch mode or single file.
- Logs metadata before/after to `metadata-log.txt`.

## Requirements
```
pip install -r requirements.txt
```

## Usage
```
python metadata_cleaner.py
```
GUI will open to let you pick files or folders.
