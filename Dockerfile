# Use Python slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install qrcode library with pillow for image generation
# Using --no-cache-dir to reduce image size
RUN pip install --no-cache-dir qrcode[pil]

# Copy the QR generator script
COPY generate_qr.py /app/generate_qr.py

# Make script executable
RUN chmod +x /app/generate_qr.py

# Create output directory
RUN mkdir -p /output

# Create non-root user for security (optional but best practice)
RUN useradd -m -u 1000 qruser && \
    chown -R qruser:qruser /app /output

# Switch to non-root user
USER qruser

# Set environment variables with defaults
ENV PYTHONUNBUFFERED=1

# Run the QR generator script
CMD ["python", "/app/generate_qr.py"]
