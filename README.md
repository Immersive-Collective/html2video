# HTML2Video Converter

This script processes ZIP files containing HTML ads, extracts the ad size, and creates both **MP4 videos** and **GIFs** from the `index.html` files found within.

## Features
- Automatically extracts ad size from embedded or external CSS (`.gwd-page-size`).
- Records frames using Playwright and generates MP4 and GIF outputs.
- Supports batch processing of multiple ZIP files.

---

## Requirements

Before running the script, make sure to install the following:

1. Python 3.10+
2. `ffmpeg` for creating video outputs:
   ```bash
   brew install ffmpeg  # macOS
   sudo apt install ffmpeg  # Linux
