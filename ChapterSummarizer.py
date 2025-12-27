import os
from pypdf import PdfReader, PdfWriter

# --- Configuration ---
input_filename = r"C:\Pythoning\Statics & Dynamics 14e.pdf"
output_filename = r"C:\Pythoning\All_Chapter_Summaries.pdf"

# Ranges for "Chapter Review" and "Review Problems" sections
# Format: (Chapter Name, Start Page, End Page) - All pages are absolute PDF numbers
review_ranges = [
    # --- STATICS ---
    ("Ch01_Summary", 40, 41),
    ("Ch02_Summary", 95, 111),
    ("Ch03_Summary", 132, 145),
    ("Ch04_Summary", 216, 231),
    ("Ch05_Summary", 277, 297),
    ("Ch06_Summary", 331, 367),
    ("Ch07_Summary", 407, 425),
    ("Ch08_Summary", 478, 489),
    ("Ch09_Summary", 538, 553),
    ("Ch10_Summary", 589, 605),
    ("Ch11_Summary", 627, 640),
    
    # --- DYNAMICS ---
    ("Ch12_Summary", 733, 753),
    ("Ch13_Summary", 806, 819),
    ("Ch14_Summary", 859, 877),
    ("Ch15_Summary", 942, 959),
    ("Ch16_Summary", 1031, 1049),
    ("Ch17_Summary", 1098, 1113),
    ("Ch18_Summary", 1138, 1157),
    ("Ch19_Summary", 1186, 1201),
    ("Ch20_Summary", 1220, 1231),
    ("Ch21_Summary", 1274, 1283),
    ("Ch22_Summary", 1315, 1322)
]

def create_summary_pdf():
    if not os.path.exists(input_filename):
        print(f"Error: Could not find file at '{input_filename}'")
        return

    print(f"Reading from: {input_filename}...")
    try:
        reader = PdfReader(input_filename)
        writer = PdfWriter()
        total_pages = len(reader.pages)
        
        page_count = 0

        for name, start, end in review_ranges:
            # Convert to 0-based index
            start_idx = start - 1
            end_idx = end 
            
            if start_idx < 0 or end_idx > total_pages:
                print(f"Warning: Skipping {name} (Range {start}-{end} out of bounds)")
                continue
            
            print(f"Adding {name} (Pages {start}-{end})")
            
            for i in range(start_idx, end_idx):
                writer.add_page(reader.pages[i])
                page_count += 1

        print(f"\nWriting {page_count} pages to {output_filename}...")
        
        with open(output_filename, "wb") as out_file:
            writer.write(out_file)
            
        print("Success! Summary PDF created.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    create_summary_pdf()