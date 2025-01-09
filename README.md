### **How to Run the Script**

Once you have the `requirements.txt` file and your dependencies installed, here’s how you can run the script.

---

### **Step 1: Install Dependencies**
First, ensure all dependencies are installed using:
```bash
pip install -r requirements.txt
```

---

### **Step 2: Install Playwright Browsers (If Not Done Yet)**
Playwright requires browser binaries. Run:
```bash
playwright install
```
This installs the necessary browsers (Chromium, Firefox, WebKit).

---

### **Step 3: Run the Script**
To run the script:
```bash
python html2video.py <folder_path> <duration_in_seconds> <frame_rate>
```

- **`<folder_path>`**: Path to the folder containing the ZIP files.
- **`<duration_in_seconds>`**: Duration of the video/GIF.
- **`<frame_rate>`**: Frame rate for the video (e.g., `24` FPS).

---

### **Example Command:**
```bash
python html2video.py content/test2 10 12
```
- **`content/test2`**: Path to the folder with ZIP files containing ads.
- **`10`**: Duration in seconds for each video.
- **`12`**: Frame rate (12 frames per second).

---

### **Expected Output:**
For each ZIP file (e.g., `ad1.zip`, `ad2.zip`), the script will generate:
```plaintext
content/test2/
  ├── ad1.zip
  ├── ad1.mp4
  ├── ad1.gif
  ├── ad2.zip
  ├── ad2.mp4
  └── ad2.gif
```

---

### **Common Issues & Solutions:**

1. **"Playwright browsers not found"**  
   Solution:
   ```bash
   playwright install
   ```

2. **"ffmpeg not found"**  
   Solution:
   ```bash
   brew install ffmpeg  # macOS
   sudo apt install ffmpeg  # Linux
   ```

