import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

try:
    import piexif
    import pikepdf
    from docx import Document
    from openpyxl import load_workbook
    from pptx import Presentation
except ImportError as e:
    tk.Tk().withdraw()
    messagebox.showerror("Missing Dependency", f"A required Python package is missing: {e}\nPlease install all dependencies and restart the program.")
    raise
import subprocess

import pathlib
# Set log file to user's Documents folder
LOG_FILE = str(pathlib.Path.home() / "Documents" / "metadata-log.txt")

def log(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

def clean_image(file_path):
    try:
        img = Image.open(file_path)
        clean_path = os.path.splitext(file_path)[0] + "_clean" + os.path.splitext(file_path)[1]
        if file_path.lower().endswith(('.jpg', '.jpeg')):
            exif_bytes = piexif.dump({"0th": {}, "Exif": {}, "GPS": {}, "1st": {}, "thumbnail": None})
            img.save(clean_path, exif=exif_bytes)
        else:
            img.save(clean_path)
        log(f"[IMAGE] Cleaned {file_path} -> {clean_path}")
        return clean_path
    except Exception as e:
        log(f"[IMAGE] Failed {file_path}: {e}")
        return None

def clean_pdf(file_path):
    try:
        clean_path = os.path.splitext(file_path)[0] + "_clean.pdf"
        with pikepdf.open(file_path) as pdf:
            pdf.docinfo.clear()
            pdf.save(clean_path)
        log(f"[PDF] Cleaned {file_path} -> {clean_path}")
        return clean_path
    except Exception as e:
        log(f"[PDF] Failed {file_path}: {e}")
        return None

def clean_docx(file_path):
    try:
        doc = Document(file_path)
        clean_path = os.path.splitext(file_path)[0] + "_clean.docx"
        core_props = doc.core_properties
        core_props.author = ""
        core_props.title = ""
        core_props.subject = ""
        core_props.keywords = ""
        core_props.comments = ""
        core_props.last_modified_by = ""
        doc.save(clean_path)
        log(f"[DOCX] Cleaned {file_path} -> {clean_path}")
        return clean_path
    except Exception as e:
        log(f"[DOCX] Failed {file_path}: {e}")
        return None

def clean_xlsx(file_path):
    try:
        wb = load_workbook(file_path)
        clean_path = os.path.splitext(file_path)[0] + "_clean.xlsx"
        props = wb.properties
        props.creator = ""
        props.title = ""
        props.subject = ""
        props.keywords = ""
        props.lastModifiedBy = ""
        wb.save(clean_path)
        log(f"[XLSX] Cleaned {file_path} -> {clean_path}")
        return clean_path
    except Exception as e:
        log(f"[XLSX] Failed {file_path}: {e}")
        return None

def clean_pptx(file_path):
    try:
        prs = Presentation(file_path)
        clean_path = os.path.splitext(file_path)[0] + "_clean.pptx"
        props = prs.core_properties
        props.author = ""
        props.title = ""
        props.subject = ""
        props.keywords = ""
        props.last_modified_by = ""
        prs.save(clean_path)
        log(f"[PPTX] Cleaned {file_path} -> {clean_path}")
        return clean_path
    except Exception as e:
        log(f"[PPTX] Failed {file_path}: {e}")
        return None

def clean_video(file_path):
    try:
        clean_path = os.path.splitext(file_path)[0] + "_clean" + os.path.splitext(file_path)[1]
        cmd = ["ffmpeg", "-i", file_path, "-map_metadata", "-1", "-c", "copy", clean_path]
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        except FileNotFoundError:
            messagebox.showerror("Missing Dependency", "ffmpeg is not installed or not in PATH. Please install ffmpeg and try again.")
            log(f"[VIDEO] ffmpeg not found for {file_path}")
            return None
        except subprocess.CalledProcessError as e:
            log(f"[VIDEO] ffmpeg failed for {file_path}: {e}")
            return None
        if os.path.exists(clean_path):
            log(f"[VIDEO] Cleaned {file_path} -> {clean_path}")
            return clean_path
        else:
            log(f"[VIDEO] Failed to create {clean_path}")
            return None
    except Exception as e:
        log(f"[VIDEO] Failed {file_path}: {e}")
        return None

def process_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext in ['.jpg', '.jpeg', '.png']:
        return clean_image(file_path)
    elif ext == '.pdf':
        return clean_pdf(file_path)
    elif ext == '.docx':
        return clean_docx(file_path)
    elif ext == '.xlsx':
        return clean_xlsx(file_path)
    elif ext == '.pptx':
        return clean_pptx(file_path)
    elif ext in ['.mp4', '.mov']:
        return clean_video(file_path)
    else:
        log(f"[SKIP] Unsupported file type {file_path}")
        return None

import shutil

def select_files():
    files = filedialog.askopenfilenames(title="Select files to clean")
    if not files:
        messagebox.showinfo("Cancelled", "No files selected.")
        return

    if len(files) == 1:
        # Single file: ask for save location
        cleaned = process_file(files[0])
        if cleaned and os.path.exists(cleaned):
            save_path = filedialog.asksaveasfilename(
                title="Save Cleaned File As",
                initialfile=os.path.basename(cleaned),
                defaultextension=os.path.splitext(cleaned)[1],
                filetypes=[("All Files", "*.*")]
            )
            if save_path:
                try:
                    shutil.move(cleaned, save_path)
                    messagebox.showinfo("Saved", f"Cleaned file saved to:\n{save_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to save cleaned file:\n{e}")
    else:
        # Multiple files: ask for a folder to save all cleaned files
        dest_folder = filedialog.askdirectory(title="Select folder to save cleaned files")
        if dest_folder:
            for f in files:
                cleaned = process_file(f)
                if cleaned and os.path.exists(cleaned):
                    try:
                        dest_path = os.path.join(dest_folder, os.path.basename(cleaned))
                        # Avoid overwriting existing files
                        if os.path.exists(dest_path):
                            messagebox.showwarning("Warning", f"File already exists and will be overwritten: {dest_path}")
                        shutil.move(cleaned, dest_path)
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to save {os.path.basename(cleaned)}:\n{e}")
            messagebox.showinfo("Done", f"All cleaned files saved to:\n{dest_folder}\nSee {LOG_FILE}")
        else:
            messagebox.showinfo("Cancelled", "No folder selected. Cleaned files remain in default location.")

def select_folder():
    folder = filedialog.askdirectory(title="Select folder to clean")
    if not folder:
        messagebox.showinfo("Cancelled", "No folder selected.")
        return

    dest_folder = filedialog.askdirectory(title="Select folder to save cleaned files (optional, cancel to keep in place)")
    errors = []
    for root, dirs, files in os.walk(folder):
        for name in files:
            file_path = os.path.join(root, name)
            cleaned = process_file(file_path)
            if cleaned and os.path.exists(cleaned) and dest_folder:
                try:
                    dest_path = os.path.join(dest_folder, os.path.basename(cleaned))
                    if os.path.exists(dest_path):
                        messagebox.showwarning("Warning", f"File already exists and will be overwritten: {dest_path}")
                    shutil.move(cleaned, dest_path)
                except Exception as e:
                    errors.append(f"Failed to save {os.path.basename(cleaned)}: {e}")
    if errors:
        messagebox.showerror("Errors Occurred", "\n".join(errors))
    messagebox.showinfo("Done", f"Batch cleaning completed.\nSee {LOG_FILE}")

root = tk.Tk()
root.title("Universal Metadata Cleaner")
root.geometry("400x200")

tk.Button(root, text="Select File(s) to Clean", command=select_files, height=2, width=30).pack(pady=10)
tk.Button(root, text="Select Folder to Clean", command=select_folder, height=2, width=30).pack(pady=10)

root.mainloop()
