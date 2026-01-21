# 📱 QR Code Generator - Docker Image

A lightweight, secure Docker image that generates QR codes from text input. Perfect for URLs, text messages, contact info, and more!

## 🎯 What is this?

This Docker image provides a simple command-line interface to generate QR codes without installing Python or any dependencies on your local machine. Just run a single Docker command and get your QR code instantly!

**Features:**
- ✨ Simple and fast QR code generation
- 🐳 Dockerized - no local setup required
- 🔒 Runs as non-root user for security
- 📦 Lightweight image (~150MB)
- 🎨 Customizable output filename
- 💪 Error handling with helpful messages

## 🚀 Quick Start

### Basic Usage

Generate a QR code for any text:

```bash
docker run -e TEXT="Hello World" -v "$(pwd)":/output utkarsh2325/qr-generator
```

This creates `qr.png` in your current directory.

### For URLs

```bash
docker run -e TEXT="https://github.com" -v "$(pwd)":/output utkarsh2325/qr-generator
```

### Custom Filename

```bash
docker run -e TEXT="https://youtube.com" -e FILENAME="youtube.png" -v "$(pwd)":/output utkarsh2325/qr-generator
```

## 📋 Parameters

### Required

| Parameter | Description | Example |
|-----------|-------------|---------|
| `TEXT` | The text/URL to encode in QR code | `TEXT="Hello World"` |
| `-v $(pwd):/output` | Mount volume to save output | Mount current directory |

### Optional

| Parameter | Description | Default |
|-----------|-------------|---------|
| `FILENAME` | Custom output filename | `qr.png` |

## 💡 Examples

### 1. Generate WiFi QR Code

```bash
docker run -e TEXT="WIFI:T:WPA;S:MyNetwork;P:MyPassword;;" \
  -e FILENAME="wifi.png" \
  -v "$(pwd)":/output \
  utkarsh2325/qr-generator
```

### 2. Business Card / Contact Info

```bash
docker run -e TEXT="BEGIN:VCARD
VERSION:3.0
FN:John Doe
TEL:+1234567890
EMAIL:john@example.com
END:VCARD" \
  -e FILENAME="contact.png" \
  -v "$(pwd)":/output \
  utkarsh2325/qr-generator
```

### 3. Batch Generation Script

Create multiple QR codes:

```bash
#!/bin/bash
urls=(
  "https://github.com"
  "https://docker.com"
  "https://python.org"
)

for url in "${urls[@]}"; do
  name=$(echo $url | sed 's/https:\/\///' | sed 's/\///')
  docker run -e TEXT="$url" -e FILENAME="${name}.png" -v "$(pwd)":/output utkarsh2325/qr-generator
done
```

### 4. Generate from Variable

```bash
MY_URL="https://example.com"
docker run -e TEXT="$MY_URL" -v "$(pwd)":/output utkarsh2325/qr-generator
```

## 🛠️ Building Locally

### Clone and Build

```bash
cd QR_Code
docker build -t utkarsh2325/qr-generator .
```

### Run Local Build

```bash
docker run -e TEXT="Test" -v "$(pwd)":/output utkarsh2325/qr-generator
```

## 📤 Publishing to Docker Hub

### Tag and Push

```bash
# Build with version tag
docker build -t utkarsh2325/qr-generator:v1.0.0 .

# Tag as latest
docker tag utkarsh2325/qr-generator:v1.0.0 utkarsh2325/qr-generator:latest

# Push to Docker Hub
docker push utkarsh2325/qr-generator:v1.0.0
docker push utkarsh2325/qr-generator:latest
```

### Multi-Architecture Build (ARM + x86)

For Apple Silicon (M1/M2) and Intel compatibility:

```bash
docker buildx create --use
docker buildx build --platform linux/amd64,linux/arm64 \
  -t utkarsh2325/qr-generator:latest \
  -t utkarsh2325/qr-generator:v1.0.0 \
  --push .
```

## 🖼️ Output Format

- **Format:** PNG image
- **Color:** Black QR code on white background
- **Size:** Auto-adjusts based on text length
- **Border:** 4 modules (standard)
- **Error Correction:** Level L (7% recovery)

## 🐧 Supported Platforms

- ✅ Linux (x86_64)
- ✅ macOS (Intel)
- ✅ macOS (Apple Silicon M1/M2) - with multi-arch build
- ✅ Windows (WSL2 / Docker Desktop)

## ⚠️ Error Handling

### Missing TEXT Variable

```bash
docker run -v "$(pwd)":/output utkarsh2325/qr-generator
```

**Output:**
```
❌ ERROR: TEXT environment variable is required!

Usage:
  docker run -e TEXT="Your text here" -v "$(pwd)":/output utkarsh2325/qr-generator

Optional:
  -e FILENAME="custom.png"  (default: qr.png)
```

## 🔍 Troubleshooting

### Permission Issues on Linux

If you get permission errors with the output file:

```bash
# Option 1: Run with current user
docker run --user $(id -u):$(id -g) -e TEXT="Hello" -v "$(pwd)":/output utkarsh2325/qr-generator

# Option 2: Fix permissions after generation
sudo chown $USER:$USER qr.png
```

### Output Directory Not Found

Make sure to mount a volume:

```bash
# ✅ Correct - mounts current directory
docker run -e TEXT="Hello" -v "$(pwd)":/output utkarsh2325/qr-generator

# ❌ Wrong - no volume mounted (file stays in container)
docker run -e TEXT="Hello" utkarsh2325/qr-generator
```

## 🚀 Advanced Usage

### Alias for Convenience

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
alias qr='docker run -e TEXT="$1" -v "$(pwd)":/output utkarsh2325/qr-generator'
```

Usage:
```bash
qr "https://github.com"
```

### Integration with CI/CD

Use in GitHub Actions:

```yaml
- name: Generate QR Code
  run: |
    docker run -e TEXT="${{ secrets.DEPLOYMENT_URL }}" \
      -e FILENAME="deployment-qr.png" \
      -v "$(pwd)":/output \
      utkarsh2325/qr-generator
    
- name: Upload QR Code
  uses: actions/upload-artifact@v3
  with:
    name: qr-code
    path: deployment-qr.png
```

## 📚 Technical Details

### Image Specifications

- **Base Image:** `python:3.11-slim`
- **Python Version:** 3.11
- **Dependencies:** `qrcode[pil]`
- **User:** Non-root user (UID 1000)
- **Working Directory:** `/app`
- **Output Directory:** `/output`

### Security Features

- Runs as non-root user (`qruser`)
- Minimal attack surface (slim base image)
- No unnecessary packages installed
- Read-only application code

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

- [ ] Add SVG output support
- [ ] Support colored QR codes
- [ ] Add batch processing from text file
- [ ] TOTP QR code generation
- [ ] Custom QR code styling options

## 📄 License

MIT License - feel free to use this in your projects!

## 🔗 Links

- **Docker Hub:** `https://hub.docker.com/r/utkarsh2325/qr-generator`
- **GitHub:** `https://github.com/utkarsh232005/QR_Code`
- **Issues:** Report bugs or request features

## 📊 Version History

### v1.0.0 (Current)
- Initial release
- Basic QR code generation
- Custom filename support
- Non-root user security
- Comprehensive error handling

---

**Made with ❤️ for the Docker community**

*Generate QR codes in seconds, not minutes!*
