import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import Response, HTMLResponse
import re

app = FastAPI()
is_starting = True

server_url = 'https://DASH.onrender.com'
input_file = r'storage/dance-monkey.mp4'
output_folder = 'output'


def generate_dash():
    global is_starting

    if is_starting:
        # Delete any file with .mpd or .m4s extension in output_folder
        for file in os.listdir(output_folder):
            if file.endswith(".mpd") or file.endswith(".m4s"):
                os.remove(os.path.join(output_folder, file))

        # Generate DASH segments from the video using ffmpeg
        subprocess.call([
            'ffmpeg', '-i', input_file, '-b:v', '235k', f'{output_folder}/video 235kbps.mp4', '-b:v', '1050k',
            f'{output_folder}/video 1050kbps.mp4', '-b:v', '4300k', f'{output_folder}/video 4300kbps.mp4'
        ])

        subprocess.call([
            'ffmpeg', '-i', f'{output_folder}/video 235kbps.mp4', '-i', f'{output_folder}/video 1050kbps.mp4',
            '-i', f'{output_folder}/video 4300kbps.mp4', '-map', '0:v', '-map', '0:a', '-map', '1:v', '-map', '1:a',
            '-map', '2:v', '-map', '2:a', '-c:v', 'libx264', '-b:v:0', '235k', '-c:v:1', 'libx264', '-b:v:1', '1050k',
            '-c:v:2', 'libx264', '-b:v:2', '4300k', '-c:a', 'aac', '-f', 'dash', f'{output_folder}/video.mpd'
        ])

        for file in os.listdir(output_folder):
            if file.endswith(".mp4"):
                os.remove(os.path.join(output_folder, file))

        is_starting = False


generate_dash()


@app.get('/dash')
def generate_dash():
    content = prefix_dash_urls(f'{output_folder}/video.mpd')
    return Response(content=content, media_type="application/dash+xml")


def prefix_dash_urls(file_path):
    prefix = f"{output_folder}/"
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if '<SegmentTemplate' in line:
                lines[i] = re.sub(r'initialization="', f'initialization="{prefix}',
                                  line)
                lines[i] = re.sub(r'media="', f'media="{prefix}', lines[i])
    content = ''.join(lines)
    return content


@app.get(f'/{output_folder}/{{segment}}')
async def dash(segment: str):
    with open(f'{output_folder}/{segment}', 'rb') as f:
        content = f.read()
    return Response(content=content, media_type="video/mp4")


# Serve the HTML file for playing the DASH content
@app.get("/")
async def get_index():
    with open("index.html", "r") as f:
        html_content = f.read().replace("{server_url}", server_url)
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/video")
async def get_video():
    with open("storage/dance-monkey.mp4", "rb") as f:
        content = f.read()
    return Response(content=content, media_type="video/mp4")
