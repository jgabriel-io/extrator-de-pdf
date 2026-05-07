# cut_doc/processor.py
import fitz  # PyMuPDF
import io
import os
import re
import unicodedata
import zipfile
import tempfile


def sanitize_name_for_filename(name):
    """Removes accents, replaces spaces with hyphens, strips invalid characters."""
    nfkd_form = unicodedata.normalize('NFKD', name)
    sanitized = "".join([c for c in nfkd_form if not unicodedata.combining(c)])
    sanitized = re.sub(r'\s+', '-', sanitized)
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '', sanitized)
    return sanitized


def find_and_crop_bytes(name_to_find, pdf_bytes, save_pdf=True):
    """
    Searches for name_to_find in a PDF (given as bytes).
    Returns (zip_bytes, found_count) or (None, 0) if not found.
    """
    sanitized_name = sanitize_name_for_filename(name_to_find)
    name_lower = name_to_find.lower()
    name_normalized = "".join([
        c for c in unicodedata.normalize('NFKD', name_lower)
        if not unicodedata.combining(c)
    ])

    with tempfile.TemporaryDirectory() as work_dir:
        found_count = 0
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)

            # 1. Exact match via PyMuPDF
            found = bool(page.search_for(name_to_find, quads=False))

            if not found:
                page_text = page.get_text()
                # 2. Case-insensitive
                found = name_lower in page_text.lower()

            if not found:
                # 3. Accent-normalized comparison
                page_normalized = "".join([
                    c for c in unicodedata.normalize('NFKD', page_text.lower())
                    if not unicodedata.combining(c)
                ])
                found = name_normalized in page_normalized

            if found:
                found_count += 1
                pix = page.get_pixmap(dpi=300)
                pix.save(os.path.join(work_dir, f"{sanitized_name}_pagina_{page_num + 1}.png"))

                if save_pdf:
                    new_doc = fitz.open()
                    new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
                    new_doc.save(os.path.join(work_dir, f"{sanitized_name}_pagina_{page_num + 1}.pdf"))
                    new_doc.close()

        doc.close()

        if found_count == 0:
            return None, 0

        buf = io.BytesIO()
        with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for fname in os.listdir(work_dir):
                zipf.write(os.path.join(work_dir, fname), fname)
        buf.seek(0)
        return buf.read(), found_count
