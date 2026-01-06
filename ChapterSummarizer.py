import os
from pypdf import PdfReader, PdfWriter

# --- Configuration ---
# Source: The original big PDF (Required for accurate page numbers)
input_filename = r"C:\Pythoning\Statics and Dynamics\Statics & Dynamics 14e.pdf"

# Destination: Your new split folder
output_filename = r"C:\Pythoning\Statics and Dynamics\Hibbeler_Chapter_Reviews.pdf"

# Format: (Chapter Name, Start Page, End Page)
# These pages capture ONLY the "Chapter Review" (Summary points), skipping the problems.
review_pages = [
    # --- STATICS ---
    ("Ch01_Review", 37, 37),      # You listed 37
    ("Ch02_Review", 106, 108),    # You listed 106-108
    ("Ch03_Review", 142, 142),    # You listed 142
    ("Ch04_Review", 226, 228),    # You listed 226-228
    ("Ch05_Review", 293, 294),    # You listed 293-294
    ("Ch06_Review", 362, 364),    # You listed 362-364
    ("Ch07_Review", 421, 423),    # You listed 421-423
    ("Ch08_Review", 484, 486),    # You listed 484-486
    ("Ch09_Review", 548, 550),    # You listed 548-550
    ("Ch10_Review", 601, 602),    # You listed 601-602
    ("Ch11_Review", 637, 638),    # You listed 637-638
    ("Appendix", 641, 644),       # You listed 641-644

    # --- DYNAMICS ---
    ("Ch12_Review", 811, 814),    # You listed 811-814
    ("Ch13_Review", 880, 880),    # You listed 880
    ("Ch14_Review", 937, 938),    # You listed 937-938
    ("Ch15_Review", 1019, 1020),  # You listed 1019-1020
    ("Ch16_Review", 1109, 1110),  # You listed 1109-1110
    ("Ch17_Review", 1174, 1174),  # You listed 1174
    ("Ch18_Review", 1216, 1218),  # You listed 1216-1218
    ("Ch19_Review", 1261, 1262),  # You listed 1261-1262
    ("Ch20_Review", 1294, 1294),  # You listed 1294
    ("Ch21_Review", 1345, 1346),  # You listed 1345-1346
    ("Ch22_Review", 1385, 1386),  # You listed 1385-1386
    ("Equations", 1466, 1469)     # You listed 1466-1469
]
def create_review_pdf():
    # 1. Verify Source Exists
    if not os.path.exists(input_filename):
        print(f"Error: Could not find the source file at '{input_filename}'")
        print("Please make sure the original big PDF is still in that location.")
        return

    # 2. Verify/Create Output Directory
    output_dir = os.path.dirname(output_filename)
    if not os.path.exists(output_dir):
        # Just in case the folder name isn't exactly what you typed
        try:
            os.makedirs(output_dir)
            print(f"Created missing folder: {output_dir}")
        except OSError:
            print(f"Error: The folder '{output_dir}' does not exist.")
            return

    print(f"Reading from: {input_filename}...")
    
    try:
        reader = PdfReader(input_filename)
        writer = PdfWriter()
        
        page_count = 0
        
        for name, start, end in review_pages:
            # Convert 1-based page numbers to 0-based index
            start_idx = start - 1
            end_idx = end  
            
            # Loop through the range (inclusive)
            for i in range(start_idx, end_idx):
                if i < len(reader.pages):
                    writer.add_page(reader.pages[i])
                    page_count += 1
                else:
                    print(f"Warning: Page {i+1} out of bounds for {name}")

        print(f"\nMerging {page_count} pages into:")
        print(f"--> {output_filename}")
        
        with open(output_filename, "wb") as out_file:
            writer.write(out_file)
            
        print("\nSuccess! 'Hibbeler_Chapter_Reviews.pdf' created.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_review_pdf()