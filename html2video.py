import asyncio
import os
import sys
import zipfile
import shutil
from multiprocessing import Process
from playwright.async_api import async_playwright
import imageio
from bs4 import BeautifulSoup

# Function to extract ad size from the HTML file
import re

import requests
from urllib.parse import urljoin

def extract_size_from_html(html_path):
    with open(html_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        width = 1280  # Default width fallback
        height = 720  # Default height fallback

        # Combine all <style> tags
        css_content = ""
        style_tags = soup.find_all("style")
        for style_tag in style_tags:
            if style_tag.string:
                css_content += style_tag.string

        # Improved regex to handle various formats
        # match = re.search(r'\.gwd-page-size\s*\{[^}]*width\s*:\s*(\d+)px\s*;[^}]*height\s*:\s*(\d+)px\s*;', css_content, re.IGNORECASE)
        match = re.search(r'\.gwd-page-size\s*\{[^}]*width\s*:\s*(\d+)\s*px[^}]*height\s*:\s*(\d+)\s*px', css_content, re.DOTALL | re.IGNORECASE)

        if match:
            width = int(match.group(1))
            height = int(match.group(2))
            print(f"Extracted size from CSS: {width}x{height}")
        else:
            print("Warning: Could not find .gwd-page-size size in CSS. Using default size.")

        return width, height





async def record_html_ad_headless(html_path, output_path, duration, frame_rate):
    width, height = extract_size_from_html(html_path)
    print(f"Extracted size from HTML: {width}x{height}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={"width": width, "height": height})
        page = await context.new_page()

        # Load the local HTML file
        html_file_url = f"file://{os.path.abspath(html_path)}"
        await page.goto(html_file_url)

        frame_path = f"{output_path}_frames"
        os.makedirs(frame_path, exist_ok=True)

        # Record screenshots as frames
        for i in range(duration * frame_rate):
            await page.screenshot(path=f"{frame_path}/frame_{i:04d}.png")
            await asyncio.sleep(1 / frame_rate)

        await browser.close()

        # Create video and GIF using proper file paths (quote paths for spaces)
        video_output = f"{output_path}.mp4"
        gif_output = f"{output_path}.gif"

        os.system(f'ffmpeg -framerate {frame_rate} -i "{frame_path}/frame_%04d.png" -r {frame_rate} -pix_fmt yuv420p "{video_output}"')
        print(f"Video saved as {video_output}")

        with imageio.get_writer(gif_output, mode='I', fps=frame_rate) as writer:
            for i in range(duration * frame_rate):
                frame_file = f"{frame_path}/frame_{i:04d}.png"
                image = imageio.imread(frame_file)
                writer.append_data(image)

        print(f"GIF saved as {gif_output}")

        # Clean up frames
        for f in os.listdir(frame_path):
            os.remove(os.path.join(frame_path, f))
        os.rmdir(frame_path)


def background_task(folder_path, duration, frame_rate):
    temp_extraction_path = "temp_unzipped"
    os.makedirs(temp_extraction_path, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(".zip"):
            zip_path = os.path.join(folder_path, filename)
            base_name = os.path.splitext(filename)[0]  # Remove ".zip" extension
            output_path = os.path.join(folder_path, base_name)  # Output folder path

            # Unzip and find index.html
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_extraction_path)

            index_html_path = None
            for root, _, files in os.walk(temp_extraction_path):
                if "index.html" in files:
                    index_html_path = os.path.join(root, "index.html")
                    break

            if index_html_path:
                print(f"Processing: {index_html_path}")
                # Ensure proper video and GIF file paths
                mp4_output_path = os.path.join(folder_path, f"{base_name}.mp4")
                gif_output_path = os.path.join(folder_path, f"{base_name}.gif")
                asyncio.run(record_html_ad_headless(index_html_path, base_name, duration, frame_rate))
            else:
                print(f"Skipped {filename}: No index.html found.")

            # Clean up extracted files
            shutil.rmtree(temp_extraction_path)


def main():
    if len(sys.argv) != 4:
        print("Usage: python html2video.py <folder_path> <duration_in_seconds> <frame_rate>")
        sys.exit(1)

    folder_path = sys.argv[1]
    try:
        duration = int(sys.argv[2])
        frame_rate = int(sys.argv[3])
    except ValueError:
        print("Duration and frame rate must be integers.")
        sys.exit(1)

    process = Process(target=background_task, args=(folder_path, duration, frame_rate))
    process.start()
    process.join()

if __name__ == "__main__":
    main()
