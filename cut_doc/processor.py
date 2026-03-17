# cut_doc/processor.py
import fitz  # PyMuPDF
import os
import re
import unicodedata
from datetime import datetime
import zipfile
import shutil

def sanitize_name_for_filename(name):
    """
    Sanitizes a name for use in a filename.
    - Removes accents.
    - Replaces spaces with underscores.
    - Converts to lowercase.
    """
    # Remove accents
    nfkd_form = unicodedata.normalize('NFKD', name)
    sanitized_name = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    # Replace spaces and remove invalid characters
    sanitized_name = re.sub(r'\s+', '-', sanitized_name)
    sanitized_name = re.sub(r'[^a-zA-Z0-9_-]', '', sanitized_name)
    return sanitized_name

def _zip_work_dir(work_dir, output_folder, zip_filename_base):
    """Zips the contents of the working directory and places it in the output folder."""
    zip_filename = f"{zip_filename_base}-certificados.zip"
    zip_filepath = os.path.join(output_folder, zip_filename)

    with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(work_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, work_dir)
                zipf.write(file_path, arcname)
    
    print(f"Successfully created ZIP file: {zip_filepath}")
    return zip_filepath

def find_and_crop(name_to_find, pdf_folder, output_folder, save_pdf=True):
    """
    Finds pages in PDFs containing a specific name, crops them, and saves them as PNG and optionally PDF.
    All output files are placed in a single ZIP archive.
    """
    sanitized_name = sanitize_name_for_filename(name_to_find)
    
    # Create a temporary working directory for this operation
    temp_work_dir = os.path.join(output_folder, f"temp_{sanitized_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}")
    os.makedirs(temp_work_dir, exist_ok=True)

    found_count = 0
    pdf_files = [f for f in os.listdir(pdf_folder) if f.lower().endswith(".pdf")]

    if not pdf_files:
        print(f"No PDF files found in '{pdf_folder}'.")
        shutil.rmtree(temp_work_dir)
        return

    print(f"Searching for '{name_to_find}' in {len(pdf_files)} PDF files...")

    for filename in pdf_files:
        pdf_path = os.path.join(pdf_folder, filename)
        try:
            doc = fitz.open(pdf_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                if page.search_for(name_to_find, quads=False):
                    found_count += 1
                    print(f"  Found '{name_to_find}' in '{filename}' on page {page_num + 1}.")

                    # Save as PNG
                    pix = page.get_pixmap(dpi=300)
                    png_output_path = os.path.join(temp_work_dir, f"{sanitized_name}_pagina_{page_num + 1}.png")
                    pix.save(png_output_path)
                    print(f"    Saved PNG: {png_output_path}")

                    # Save as individual PDF
                    if save_pdf:
                        pdf_output_path = os.path.join(temp_work_dir, f"{sanitized_name}_pagina_{page_num + 1}.pdf")
                        new_doc = fitz.open()
                        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                        new_doc.save(pdf_output_path)
                        new_doc.close()
                        print(f"    Saved PDF: {pdf_output_path}")
            doc.close()
        except Exception as e:
            print(f"Error processing file '{filename}': {e}")

    if found_count > 0:
        print(f"\nFound {found_count} occurrences in total.")
        # Create a single ZIP file with all the found items
        _zip_work_dir(temp_work_dir, output_folder, sanitized_name)
    else:
        print(f"\nNo occurrences of '{name_to_find}' found in any PDF files.")

    # Clean up the temporary directory
    try:
        shutil.rmtree(temp_work_dir)
        print(f"Successfully removed temporary directory: {temp_work_dir}")
    except Exception as e:
        print(f"Error removing temporary directory '{temp_work_dir}': {e}")

    print("\nProcessing complete.")
