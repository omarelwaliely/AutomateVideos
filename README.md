# Automatic Short Videos

## Overview

This is an ongoing experiment which will be an automatic video uploader. 

## Features

- **Reddit Scraper**: Retrieve a set of posts from a specified subreddit.
- **Text-to-Speech**: Utilize the TikTok-Voice-TTS library for converting text to voice.
- **Video**: Create videos with an AI voice and automatic captioning.
- **Automatic Uploading**: Create videos automatically and uploads to instagram at set times.

## Credits
The utilized libarries are listed below
- **Tiktok TTS**: [TikTok-Voice-TTS](https://github.com/Giooorgiooo/TikTok-Voice-TTS) repository for text-to-speech functionality. By  [Giooorgiooo](https://github.com/Giooorgiooo) 
- **Whisper ASR**: [Whisper AI](https://openai.com/research/whisper) used for speech to text captioning.
- **Instabot**: [Instabot](https://pypi.org/project/instabot/) used to upload to instagram. (note I commented out error 429 in api.py and had to replace [api_video.py](https://github.com/ohld/igbot/blob/ad75eb86beacc5fe11ae5321caa8482e00f782d3/instabot/api/api_video.py)

