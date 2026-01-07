import os
from pathlib import Path
from pdf2image import convert_from_path

def extract_first_page_as_jpg(pdf_path, output_path):
    """
    Extract the first page from a PDF and save it as JPG
    
    Args:
        pdf_path: Path to the PDF file
        output_path: Full path where the JPG will be saved
    """
    try:
        # Convert only the first page to image
        images = convert_from_path(pdf_path, first_page=1, last_page=1, dpi=300)
        
        if images:
            # Save the first page as JPG
            images[0].save(output_path, 'JPEG', quality=95)
            print(f"  ✓ Saved: {Path(output_path).name} from {Path(pdf_path).name}")
            return True
        else:
            print(f"  ✗ No pages found in {Path(pdf_path).name}")
            return False
            
    except Exception as e:
        print(f"  ✗ Error processing {Path(pdf_path).name}: {str(e)}")
        return False

def convert_pdfs_to_jpg(input_folder, output_folder=None):
    """
    Extract first page from all PDFs in a folder and save as sequential JPG files
    
    Args:
        input_folder: Folder containing PDF files
        output_folder: Folder where JPG images will be saved (default: input_folder/jpg_output)
    """
    # Set default output folder if not provided
    if output_folder is None:
        output_folder = os.path.join(input_folder, "jpg_output")
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all PDF files in the input folder
    pdf_files = sorted([f for f in os.listdir(input_folder) 
                       if f.lower().endswith('.pdf')])
    
    if not pdf_files:
        print(f"No PDF files found in {input_folder}")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s) in {input_folder}\n")
    print(f"Output folder: {output_folder}\n")
    print("=" * 50)
    
    # Process each PDF and save with sequential naming
    success_count = 0
    for idx, pdf_file in enumerate(pdf_files, start=1):
        pdf_path = os.path.join(input_folder, pdf_file)
        
        # Create sequential output filename: image_01.jpg, image_02.jpg, etc.
        output_filename = f"image_{idx:02d}.jpg"
        output_path = os.path.join(output_folder, output_filename)
        
        print(f"Processing PDF {idx}/{len(pdf_files)}: {pdf_file}")
        if extract_first_page_as_jpg(pdf_path, output_path):
            success_count += 1
    
    print("=" * 50)
    print(f"\n✓ All done! {success_count}/{len(pdf_files)} images saved to: {output_folder}")

if __name__ == "__main__":
    # CONFIGURE THESE PATHS
    input_folder = "/Users/abhi/Downloads/sample_documents"  # Folder containing your PDF files
    output_folder = "./jpg_output"  # Where to save JPG images (optional)
    
    # Run the converter
    convert_pdfs_to_jpg(input_folder, output_folder)
