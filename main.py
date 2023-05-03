import os
import subprocess
from fastapi import FastAPI
from fastapi.responses import Response, HTMLResponse
import re

app = FastAPI()
is_starting = True

server_url = 'http://bdc2-102-166-14-118.ngrok-free.app'
input_file = r'E:\Videos\MKSU Portal.mp4'
output_folder = 'output'


def generate_dash():
    global is_starting

    if is_starting:
        # Delete any file with .mpd or .m4s extension in output_folder
        for file in os.listdir(output_folder):
            if file.endswith(".mpd") or file.endswith(".m4s"):
                os.remove(os.path.join(output_folder, file))

        # # Generate DASH segments from the video using ffmpeg
        # subprocess.call([
        #     'ffmpeg', '-i', input_file, '-c:a', 'copy', '-c:v', 'h264', '-preset', 'fast',
        #     '-crf', '20', '-sc_threshold', '0', '-g', '48', '-keyint_min', '48',
        #     '-hls_playlist', '0', '-f', 'dash', f'{output_folder}/video.mpd'
        # ])
        subprocess.call(
            ['ffmpeg', '-i', input_file, '-c:a', 'copy', '-c:v', 'h264', '-preset', 'fast', '-sc_threshold', '0', '-g',
             '48', '-keyint_min', '48', '-hls_playlist', '0', '-f', 'dash', '-b:v:0', '6000k', '-b:v:1', '3000k',
             '-b:v:2', '1500k', '-b:v:3', '750k', '-profile:v', 'high', '-level:v', '4.2',
             f'{output_folder}/video.mpd'])

        is_starting = False


# generate_dash()


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
    with open("D:\Multimedia\Shrek The Third (2007) [1080p]\Shrek.The.Third.2007.1080p.HDDVD.x264.YIFY.mp4", "rb") as f:
        content = f.read()
    return Response(content=content, media_type="video/mp4")
