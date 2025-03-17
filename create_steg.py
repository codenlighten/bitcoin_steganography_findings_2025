import pikepdf
import struct
import os
import shutil
from datetime import datetime
import zlib

def create_identifier_pattern(id_bytes):
    """Create the steganographic pattern with the same structure as found in the Bitcoin paper."""
    return bytes([
        0x6b,         # Marker byte ('k')
        id_bytes[0],  # First identifier letter
        0x7d,         # Separator
        0xe8,         # Separator
        id_bytes[1],  # Second identifier letter
        0xb4,         # Separator
        0x17,         # Separator
        id_bytes[2]   # Third identifier letter
    ])

def inject_pattern_into_pdf(pdf_path, pattern, output_path):
    """Inject the pattern into a copy of the PDF file."""
    # Open the PDF with pikepdf
    pdf = pikepdf.Pdf.open(pdf_path)
    
    # Find the first font object
    font_obj = None
    for obj in pdf.objects:
        if isinstance(obj, pikepdf.Stream) and obj.get("/Type", "") == "/Font":
            font_obj = obj
            break
    
    if not font_obj:
        # If no font object found, try to find any stream object
        for obj in pdf.objects:
            if isinstance(obj, pikepdf.Stream):
                font_obj = obj
                break
    
    if not font_obj:
        raise Exception("Could not find suitable stream object in PDF")
    
    # Get the stream data
    stream_data = font_obj.read_raw_bytes()
    
    # Create new stream with our pattern
    new_stream = bytearray(stream_data)
    
    # Insert pattern at specific offset
    offset = min(0x184B0, len(new_stream) - len(pattern))
    new_stream[offset:offset + len(pattern)] = pattern
    
    # Update the stream
    font_obj.write(bytes(new_stream))
    
    # Save the modified PDF
    pdf.save(output_path)

def verify_pattern(pdf_path, pattern, expected_offset=None):
    """Verify that the pattern exists in the PDF at the expected location."""
    with open(pdf_path, 'rb') as f:
        content = f.read()
    
    positions = []
    pos = -1
    while True:
        pos = content.find(pattern, pos + 1)
        if pos == -1:
            break
        positions.append(pos)
    
    print(f"\nPattern verification in {os.path.basename(pdf_path)}:")
    if not positions:
        print("Pattern not found!")
        return False
    
    print(f"Found pattern at {len(positions)} location(s):")
    for pos in positions:
        print(f"  Offset: 0x{pos:x}")
        if expected_offset and pos == expected_offset:
            print("  Matches expected offset!")
    
    return bool(positions)

def analyze_pdf_structure(pdf_path):
    """Analyze the PDF structure to help with debugging."""
    pdf = pikepdf.Pdf.open(pdf_path)
    print("\nPDF Structure Analysis:")
    
    stream_count = 0
    font_count = 0
    
    for obj in pdf.objects:
        if isinstance(obj, pikepdf.Stream):
            stream_count += 1
            if obj.get("/Type", "") == "/Font":
                font_count += 1
                print(f"Found font object: {obj}")
                print(f"Stream size: {len(obj.read_raw_bytes())} bytes")
    
    print(f"Total streams found: {stream_count}")
    print(f"Font streams found: {font_count}")

def main():
    # Create our pattern
    id_bytes = b'GJW'
    pattern = create_identifier_pattern(id_bytes)
    
    print("Created steganographic pattern:")
    print("Offset   00  01  02  03  04  05  06  07    ASCII")
    hex_bytes = ' '.join(f'{b:02x}' for b in pattern)
    ascii_chars = ''.join(chr(b) if 32 <= b <= 126 else '.' for b in pattern)
    print(f"184b0   {hex_bytes}    {ascii_chars}")
    
    # Process the PDF
    input_pdf = "demo.pdf"
    output_pdf = "demo_steg.pdf"
    
    # First analyze the PDF structure
    print("\nAnalyzing input PDF structure...")
    analyze_pdf_structure(input_pdf)
    
    print(f"\nInjecting pattern into {input_pdf}...")
    inject_pattern_into_pdf(input_pdf, pattern, output_pdf)
    
    # Verify the pattern was injected correctly
    verify_pattern(output_pdf, pattern)
    
    print("\nAnalyzing output PDF structure...")
    analyze_pdf_structure(output_pdf)

if __name__ == "__main__":
    main()
