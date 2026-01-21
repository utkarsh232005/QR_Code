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
    # Get TEXT from environment variable
    text = os.getenv("TEXT")
    
    # Error handling: TEXT is required
    if not text:
        print("❌ ERROR: TEXT environment variable is required!")
        print("\nUsage:")
        print('  docker run -e TEXT="Your text here" -v $(pwd):/output utkarsh/qr-generator')
        print("\nOptional:")
        print('  -e FILENAME="custom.png"  (default: qr.png)')
        sys.exit(1)
    
    # Get optional FILENAME from environment variable (default: qr.png)
    filename = os.getenv("FILENAME", "qr.png")
    
    # Ensure filename has .png extension
    if not filename.endswith(".png"):
        filename += ".png"
    
    # Output directory
    output_dir = Path("/output")
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
        print(f"📁 Location: /output/{filename}")
        
    except Exception as e:
        print(f"❌ ERROR: Failed to generate QR code: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
