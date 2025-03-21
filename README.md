# PDF Font Stream Steganography: Technical Reproduction Study

By Gregory J. Ward  
SmartLedger Research (smartledger.solutions)  
March 17, 2025

## Disclaimers and Legal Notices

### Research Purpose
This research is conducted for academic and educational purposes only. The techniques described herein are intended to demonstrate technical feasibility and advance the understanding of PDF document analysis. This research does not encourage or endorse any unauthorized modification of existing documents.

### No Investment Advice
Nothing in this repository constitutes investment, legal, or tax advice. The information provided is purely technical in nature and should not be interpreted as commentary on any digital asset's value or potential future performance.

### Bitcoin Whitepaper Analysis
This research analyzes technical aspects of the Bitcoin whitepaper's PDF structure. It does not make claims about the document's authenticity, authorship, or implications for the Bitcoin protocol or network.

### Limitation of Liability
SmartLedger Research provides this information "as is" without warranty of any kind. We make no representations about the accuracy, reliability, completeness, or timeliness of the information provided.

### Usage Restrictions
While this repository is open source under the MIT License, any commercial use or implementation of these techniques should be conducted with appropriate legal consultation.

## Overview

This repository contains tools and documentation for reproducing and verifying the font stream steganography technique discovered in the Bitcoin whitepaper. Our research demonstrates the technical feasibility of embedding identifiers within PDF font streams while maintaining document functionality and surviving format conversions.

## Key Findings

1. **Pattern Structure**: We identified and reproduced the specific byte sequence structure:
   ```
   Offset   00  01  02  03  04  05  06  07    ASCII
   ------   6b  XX  7d  e8  XX  b4  17  XX    k.}.X..X
   ```
   where:
   - `0x6b` serves as a marker byte
   - `XX` positions contain identifier letters
   - `0x7d`, `0xe8`, `0xb4`, `0x17` are consistent separator bytes

2. **Technical Feasibility**: Successfully demonstrated:
   - Pattern injection into PDF font streams
   - Document functionality preservation
   - Pattern survival through OpenOffice conversion
   - Metadata manipulation

## Repository Contents

- `analysis.md`: Detailed technical analysis of the steganographic technique
- `create_steg.py`: Pattern creation and injection tool
- `convert_through_oo.py`: OpenOffice conversion utility
- `demo.tex`: LaTeX demonstration document
- `requirements.txt`: Python dependencies

## Reproduction Steps

### Prerequisites
```bash
# Install required packages
sudo apt-get install texlive-xetex unoconv
pip install -r requirements.txt
```

### Steps to Reproduce

1. **Generate Base PDF**
   ```bash
   xelatex demo.tex
   ```

2. **Create Steganographic Pattern**
   ```bash
   python3 create_steg.py
   ```

3. **Convert Through OpenOffice**
   ```bash
   python3 convert_through_oo.py
   ```

### Verification

The process generates three PDFs:
1. `demo.pdf`: Original LaTeX-generated PDF
2. `demo_steg.pdf`: PDF with injected pattern
3. `demo_final.pdf`: OpenOffice-processed PDF with re-injected pattern

Verify pattern presence using:
```bash
python3 create_steg.py --verify demo_final.pdf
```

## Technical Details

### Pattern Injection
The steganographic pattern is injected into the PDF's font stream using a carefully structured byte sequence that preserves font metrics and document functionality. The pattern consists of:

1. Marker byte (`0x6b`)
2. Three identifier bytes (e.g., 'G', 'J', 'W')
3. Four separator bytes (`0x7d`, `0xe8`, `0xb4`, `0x17`)

### OpenOffice Processing
To ensure document authenticity, we process the PDF through OpenOffice, which:
1. Strips the original font streams
2. Adds OpenOffice metadata
3. Requires pattern re-injection

## Tools and Dependencies

- Python 3.10+
- XeLaTeX
- OpenOffice/LibreOffice
- unoconv
- Required Python packages:
  - pikepdf
  - PyPDF2
  - numpy
  - matplotlib

## Research Applications

This research demonstrates:
1. Technical feasibility of PDF steganography
2. Pattern survival through document processing
3. Metadata manipulation techniques
4. Font stream integrity preservation

## Citation

When referencing this work, please cite:
```
Ward, G.J. (2025). "PDF Font Stream Steganography: Technical Reproduction Study"
SmartLedger Research, March 2025.
```

## License

This research is provided for academic and verification purposes only. All rights reserved.

---
Gregory J. Ward  
Principal Researcher  
SmartLedger Research  
https://smartledger.solutions
# bitcoin_steganography_findings_2025
