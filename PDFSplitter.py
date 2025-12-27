import os
from pypdf import PdfReader, PdfWriter

# --- Configuration ---
# Updated input path as requested
input_filename = r"C:\Pythoning\Statics & Dynamics 14e.pdf"
output_folder = r"C:\Pythoning\Hibbeler_Split_Chapters"

# Format: (Chapter Name, Start Page (PDF absolute), End Page (PDF absolute))
chapters = [
    # --- STATICS ---
    ("Chapter_01_General_Principles", 28, 41),
    ("Chapter_02_Force_Vectors", 42, 111),
    ("Chapter_03_Equilibrium_of_a_Particle", 112, 145),
    ("Chapter_04_Force_System_Resultants", 146, 231),
    ("Chapter_05_Equilibrium_of_a_Rigid_Body", 232, 297),
    ("Chapter_06_Structural_Analysis", 298, 367),
    ("Chapter_07_Internal_Forces", 368, 425),
    ("Chapter_08_Friction", 426, 489),
    ("Chapter_09_Center_of_Gravity_and_Centroid", 490, 553),
    ("Chapter_10_Moments_of_Inertia", 554, 605),
    ("Chapter_11_Virtual_Work", 606, 640),
    
    # --- DYNAMICS ---
    ("Chapter_12_Kinematics_of_a_Particle", 644, 753),
    ("Chapter_13_Kinetics_of_a_Particle_Force_and_Acceleration", 754, 819),
    ("Chapter_14_Kinetics_of_a_Particle_Work_and_Energy", 820, 877),
    ("Chapter_15_Kinetics_of_a_Particle_Impulse_and_Momentum", 878, 959),
    ("Chapter_16_Planar_Kinematics_of_a_Rigid_Body", 960, 1049),
    ("Chapter_17_Planar_Kinetics_of_a_Rigid_Body_Force_and_Acceleration", 1050, 1113),
    ("Chapter_18_Planar_Kinetics_of_a_Rigid_Body_Work_and_Energy", 1114, 1157),
    ("Chapter_19_Planar_Kinetics_of_a_Rigid_Body_Impulse_and_Momentum", 1158, 1201),
    ("Chapter_20_Three_Dimensional_Kinematics_of_a_Rigid_Body", 1202, 1231),
    ("Chapter_21_Three_Dimensional_Kinetics_of_a_Rigid_Body", 1232, 1283),
    ("Chapter_22_Vibrations", 1284, 1322)
]

def split_pdf():
    if not os.path.exists(input_filename):
        print(f"Error: Could not find file at '{input_filename}'")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output folder: {output_folder}")

    print(f"Reading PDF from: {input_filename}...")
    try:
        reader = PdfReader(input_filename)
        total_pages = len(reader.pages)
        print(f"Total pages in PDF: {total_pages}\n")

        for name, start_page, end_page in chapters:
            start_idx = start_page - 1
            end_idx = end_page
            
            if start_idx < 0 or end_idx > total_pages:
                print(f"Skipping {name}: Range {start_page}-{end_page} is outside file limits.")
                continue

            writer = PdfWriter()
            for i in range(start_idx, end_idx):
                writer.add_page(reader.pages[i])

            output_path = os.path.join(output_folder, f"{name}.pdf")
            with open(output_path, "wb") as output_file:
                writer.write(output_file)
            
            print(f"Saved: {name}.pdf")

        print("\nSuccess! All chapters split.")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    split_pdf()