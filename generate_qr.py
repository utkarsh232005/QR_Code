#!/usr/bin/env python3
"""
QR Code Generator Script
Reads TEXT from environment variable and generates a QR code image.
"""

import os
import sys
import qrcode
from pathlib import Path


def main():
    # Prefer env vars; fall back to interactive prompts for convenience
    text = os.getenv("TEXT")
    if not text:
        try:
            text = input("Enter text/URL for the QR code: ").strip()
        except EOFError:
            text = ""
    if not text:
        print("❌ ERROR: No text provided. Set TEXT env or enter a value interactively.")
        print("\nUsage:")
        print('  docker run -e TEXT="Your text here" -v "$(pwd)":/output utkarsh2325/qr-generator')
        print("\nOptional:")
        print('  -e FILENAME="custom.png"  (default: qr.png)')
        print('  -e OUTPUT_DIR="/your/output/path"  (default: /output)')
        sys.exit(1)

    # Get optional FILENAME from environment variable, else prompt
    filename = os.getenv("FILENAME")
    if not filename:
        try:
            filename = input("Output filename (default qr.png): ").strip()
        except EOFError:
            filename = ""
    if not filename:
        filename = "qr.png"

    # Get optional OUTPUT_DIR from environment variable, else prompt
    output_dir_str = os.getenv("OUTPUT_DIR")
    if not output_dir_str:
        try:
            output_dir_str = input("Output directory (default /output): ").strip()
        except EOFError:
            output_dir_str = ""
    if not output_dir_str:
        output_dir_str = "/output"

    # Ensure filename has .png extension
    if not filename.endswith(".png"):
        filename += ".png"
    
    # Output directory
    output_dir = Path(output_dir_str)
    output_path = output_dir / filename
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        print(f"🔄 Generating QR code for: {text[:50]}{'...' if len(text) > 50 else ''}")
        
        # Create QR code instance
        qr = qrcode.QRCode(
            version=1,  # Auto-adjust size
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        
        # Add data and optimize
        qr.add_data(text)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save to output directory
        img.save(str(output_path))
        
        print(f"✅ QR code successfully generated: {filename}")
        print(f"📁 Location: {output_path}")
        
    except Exception as e:
        print(f"❌ ERROR: Failed to generate QR code: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
