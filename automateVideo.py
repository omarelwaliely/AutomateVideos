import json
import praw
from tiktokvoice import tts
import audiosegment
from moviepy.editor import TextClip,VideoFileClip,AudioFileClip,CompositeVideoClip,ColorClip
import os

class automate():
    #authentication to access reddit api. All info should be placed in information.json
    def authenticate(self):
        info = open('information.json')
        info = json.load(info)
        self.reddit = praw.Reddit(
            client_id=info["client_id"],
            client_secret=info["client_secret"],
            password=info["password"],
            user_agent=info["user_agent"],
            username=info["username"],
        )
    #creating parseing a subreddit here, name is name of subreddit, limit is the amount of posts and skip is the number of posts to skip, useful if the top posts are moderator pins
    def parse_subreddit(self, name = "askreddit",limit = 3, skip = 1):
        subreddit = self.reddit.subreddit(name)
        return list(subreddit.hot(limit=limit+skip))[skip:] #I convert to list first since the object type isnt iteratable then slice
    def create_audio(self,title,internal_text):
        voice = "en_us_ghostface"
        tts(title, voice, "temp_title.mp3", play_sound=False)
        tts(internal_text, voice, "temp_text.mp3", play_sound=False)
        audio_title = audiosegment.from_file("temp_title.mp3")
        audio_internal = audiosegment.from_file("temp_text.mp3")
        combined_audio = audio_title+ audiosegment.silent(duration=1000) + audio_internal
        try:
            os.remove("temp_title.mp3")
            os.remove("temp_text.mp3")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Skipping: {e}")
        combined_audio.export("output.mp3", format="mp3")
    def create_video(self, title, internal_text):
        self.create_audio(title, internal_text)

        ColorClip((200,100), (0,0,0), duration=3).write_videofile("black_screen.mp4", fps=60)
        video_duration = audiosegment.from_file("output.mp3").duration_seconds
        video_clip = VideoFileClip("black_screen.mp4")

        captions = TextClip(internal_text, fontsize=24, color='white', bg_color='black')
        captions = captions.set_pos('center').set_duration(video_duration)

        video_clip = video_clip.set_audio(AudioFileClip("output.mp3")).set_duration(video_duration)
        final_clip = CompositeVideoClip([video_clip, captions])

        final_clip.write_videofile("output_video.mp4", codec='libx264', audio_codec='aac')
            


test= automate()
test.authenticate()
test.create_video("this is a test.", "this is still a test.")