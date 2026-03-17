# cut_doc/cli.py
import argparse
import os
from .processor import find_and_crop

def main():
    parser = argparse.ArgumentParser(description="Find pages in PDFs and crop them.")
    parser.add_argument("name", type=str, help="Name to search for in the PDFs.")
    parser.add_argument(
        "--pdf-folder",
        type=str,
        default="pdf",
        help="Folder containing the PDF files. Defaults to 'pdf'.",
    )
    parser.add_argument(
        "--output-folder",
        type=str,
        default="out",
        help="Folder to save the output files. Defaults to 'out'.",
    )
    parser.add_argument(
        "--no-pdf",
        action="store_true",
        help="Do not save individual PDF pages.",
    )

    args = parser.parse_args()

    # Garante que as pastas de entrada e saída existam
    if not os.path.isdir(args.pdf_folder):
        print(f"Error: PDF folder not found at '{args.pdf_folder}'")
        return
    if not os.path.isdir(args.output_folder):
        os.makedirs(args.output_folder)
        print(f"Created output folder at '{args.output_folder}'")

    find_and_crop(
        name_to_find=args.name,
        pdf_folder=args.pdf_folder,
        output_folder=args.output_folder,
        save_pdf=not args.no_pdf,
    )

if __name__ == "__main__":
    main()
