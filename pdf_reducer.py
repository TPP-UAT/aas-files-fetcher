import argparse
import os.path
import shutil
import subprocess
import sys
import os

"""Function to compress PDF via Ghostscript command line interface"""
def compress(input_file_path, power=0, pdf_counter=0):
    print("input_file_path: ", input_file_path)
    quality = {
        0: "/default",
        1: "/prepress",
        2: "/printer",
        3: "/ebook",
        4: "/screen"
    }

    # Basic controls
    # Check if valid path
    if not os.path.isfile(input_file_path):
        print("Error: invalid path for input PDF file.", input_file_path)
        sys.exit(1)

    # Check compression level
    if power < 0 or power > len(quality) - 1:
        print("Error: invalid compression level, run pdfc -h for options.", power)
        sys.exit(1)

    # Check if file is a PDF by extension
    if input_file_path.split('.')[-1].lower() != 'pdf':
        print(f"Error: input file is not a PDF.", input_file_path)
        sys.exit(1)

    # Create temp filename
    temp_filename = "temp" + str(pdf_counter) + ".pdf"
    print("temp_filename: ", temp_filename)

    gs = get_ghostscript_path()
    print("Compress PDF...")
    initial_size = os.path.getsize(input_file_path)
    subprocess.call(
        [
            gs,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS={}".format(quality[power]),
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            "-sOutputFile={}".format(temp_filename),
            input_file_path,
        ]
    )
    final_size = os.path.getsize(temp_filename)
    ratio = 1 - (final_size / initial_size)
    print("Compression by {0:.0%}.".format(ratio))
    print("Final file size is {0:.5f}MB".format(final_size / 1000000))
    print("Done.")
    delete_temp_file(input_file_path, temp_filename)


def get_ghostscript_path():
    gs_names = ["gs", "gswin32", "gswin64"]
    for name in gs_names:
        if shutil.which(name):
            return shutil.which(name)
    raise FileNotFoundError(
        f"No GhostScript executable was found on path ({'/'.join(gs_names)})"
    )

def delete_temp_file(new_path, old_path):
    if "temp" in old_path:
        shutil.copyfile(old_path, new_path)
        os.remove(old_path)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("input", help="Relative or absolute path of the folder where the PDFs are located")
    parser.add_argument("-c", "--compress", type=int, help="Compression level from 0 to 4")
    args = parser.parse_args()

    # In case no compression level is specified, default is 4 '/ screen'
    if not args.compress:
        args.compress = 4
    
    pdf_counter = 0

    # Iterate over files in the folder
    directory = os.fsencode(args.input)
    for file in os.listdir(directory):
        # Check if the file is a PDF
        filename = os.fsdecode(file)
        if filename.endswith('.pdf'):
            file_with_path = os.path.join(args.input, filename)
            compress(file_with_path, power=args.compress, pdf_counter=pdf_counter)
            pdf_counter += 1

if __name__ == "__main__":
    main()