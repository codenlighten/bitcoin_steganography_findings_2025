import os
import subprocess
import time
from create_steg import create_identifier_pattern, verify_pattern, inject_pattern_into_pdf

def convert_through_openoffice(input_pdf, output_pdf):
    """Convert PDF through OpenOffice to add OpenOffice metadata"""
    # Get absolute paths
    current_dir = os.getcwd()
    input_pdf_abs = os.path.abspath(input_pdf)
    output_pdf_abs = os.path.abspath(output_pdf)
    
    print(f"Working directory: {current_dir}")
    print(f"Input PDF: {input_pdf_abs}")
    print(f"Output PDF: {output_pdf_abs}")
    
    # List files before
    print("\nFiles before conversion:")
    print(os.listdir(current_dir))
    
    # Start the unoconv listener in the background
    print("\nStarting unoconv listener...")
    subprocess.Popen(["unoconv", "--listener"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(3)  # Give it time to start
    
    # Convert using unoconv
    print("\nConverting through unoconv...")
    try:
        result = subprocess.run(
            ["unoconv", "-f", "pdf", "-o", output_pdf_abs, input_pdf_abs],
            capture_output=True,
            text=True,
            check=True
        )
        print("\nCommand output:")
        print(result.stdout)
        print("\nCommand error:")
        print(result.stderr)
    except subprocess.CalledProcessError as e:
        print("Error during conversion:")
        print(f"Command output: {e.output}")
        print(f"Command stderr: {e.stderr}")
        raise
    finally:
        # Kill the listener
        subprocess.run(["pkill", "soffice.bin"], capture_output=True)
    
    # List files after
    print("\nFiles after conversion:")
    print(os.listdir(current_dir))
    
    if not os.path.exists(output_pdf_abs):
        raise Exception(f"Output PDF not created at {output_pdf_abs}")

def main():
    # Input is our steganographic PDF
    current_dir = os.getcwd()
    input_pdf = os.path.join(current_dir, "demo_steg.pdf")
    temp_pdf = os.path.join(current_dir, "temp_openoffice.pdf")
    final_pdf = os.path.join(current_dir, "demo_final.pdf")
    
    # Verify input file exists
    if not os.path.exists(input_pdf):
        raise Exception(f"Input PDF not found: {input_pdf}")
    
    # Create pattern for verification
    pattern = create_identifier_pattern(b'GJW')
    
    print("1. Verifying original steganographic pattern...")
    verify_pattern(input_pdf, pattern)
    
    print("\n2. Converting through OpenOffice...")
    convert_through_openoffice(input_pdf, temp_pdf)
    
    print("\n3. Verifying if pattern survived (unlikely)...")
    verify_pattern(temp_pdf, pattern)
    
    print("\n4. Re-injecting pattern into OpenOffice PDF...")
    inject_pattern_into_pdf(temp_pdf, pattern, final_pdf)
    
    print("\n5. Verifying final pattern...")
    verify_pattern(final_pdf, pattern)
    
    # Clean up
    try:
        os.remove(temp_pdf)
    except:
        print(f"Warning: Could not remove temporary PDF file: {temp_pdf}")
    
    print("\nProcess complete!")
    print(f"Final PDF with OpenOffice metadata and steganographic pattern: {final_pdf}")

if __name__ == "__main__":
    main()
