import os
import argparse
from pytube import YouTube
from urllib.parse import urlparse, parse_qs
import traceback

def clean_url(url):
    parsed_url = urlparse(url)
    clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path
    return clean_url

def download_video(url, resolution=None, audio_only=False):
    try:
        url = clean_url(url)
        
        # Youtube Object
        yt = YouTube(url)
        
        # If only audio
        if audio_only:
            print(f"Downloading audio from: {yt.title}")
            audio_stream = yt.streams.filter(only_audio=True).first()
            out_file = audio_stream.download()
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
        else:
            
            # Filter strem by resolution if provided
            stream = yt.streams.filter(res=resolution, file_extension='mp4').first()
            
            if not stream:
                print(f"Resolution {resolution} not available. Downloading heighest resolution instead.")
                stream = yt.streams.get_highest_resolution()
            
            print(f"Downloading video: {yt.title} at {stream.resolution}")
            stream.download()
            print('Download completed!')
    except Exception as e:
        print(f"Error occured: {e}")
        traceback.print_exc()

def main():
    # Setting up argument parser
    parser = argparse.ArgumentParser(description="Youtube Video Downloader")
    parser.add_argument("url", help="Youtube video URL")
    parser.add_argument("--resolution", help="Specify resolution (e.g., 720p, 1080p)", default=None)
    parser.add_argument("--audio", action="store_true", help="Download only audio as mp3")
    
    args = parser.parse_args()
    
    # Call the download function
    download_video(args.url, resolution=args.resolution, audio_only=args.audio)

if __name__ == "__main__":
    main()