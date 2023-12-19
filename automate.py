import json
import praw
from tiktokvoice import tts
import audiosegment
from moviepy.editor import TextClip,VideoFileClip,AudioFileClip,CompositeVideoClip,ColorClip
from processvideo import process_video
import os
import whisper
import random

class automate():
    #authentication to access reddit api. All info should be placed in information.json
    def __init__(self):
        info = open('information.json')
        info = json.load(info) #performing reddit authentication
        self.reddit = praw.Reddit(
            client_id=info["client_id"],
            client_secret=info["client_secret"],
            password=info["password"],
            user_agent=info["user_agent"],
            username=info["username"],
        )
        self.model = whisper.load_model("base") #loading the speech to text model (whisper)
    #creating parseing a subreddit here, name is name of subreddit, limit is the amount of posts and skip is the number of posts to skip, useful if the top posts are moderator pins
    def parse_subreddit(self, name = "programmer",limit = 3, skip = 1): #this parses a subreddits hot posts and makes an array of submissiob
        subreddit = self.reddit.subreddit(name)
        return list(subreddit.hot(limit=limit+skip))[skip:] #I convert to list first since the object type isnt iteratable then slice
    def choose_random_file(self,directory):
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
        if not files:
            print("No files found in the specified directory.")
            return None
        random_file = random.choice(files)
        return os.path.join(directory, random_file)
    def create_audio(self,title,internal_text):
        voice = "en_us_ghostface" #check tts for other voices to choose from
        tts(title, voice, "temp_title.mp3", play_sound=False)
        tts(internal_text, voice, "temp_text.mp3", play_sound=False)
        audio_title = audiosegment.from_file("temp_title.mp3") #title of post
        audio_internal = audiosegment.from_file("temp_text.mp3") #text of post
        combined_audio = audio_title+ audiosegment.silent(duration=1000) + audio_internal #merging the audio but putting a pause in the middle first
        combined_audio = combined_audio.speedup(playback_speed=2.0) #speed of the AI was slow so changed it here
        try: #removing the temporary files but incase of error putting try and catch
            os.remove("temp_title.mp3")
            os.remove("temp_text.mp3")
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Skipping: {e}")
        combined_audio.export("output.mp3", format="mp3")
    def merge_audio_video(self,input_audio_path,input_video_path,output_video_path): #function to put the generated audio with some dummy video
        video_clip = VideoFileClip(input_video_path)
        audio_clip = AudioFileClip(input_audio_path)
        video_clip_with_audio = video_clip.set_audio(audio_clip)
        video_clip_with_audio.subclip(0, audio_clip.duration).write_videofile(output_video_path) #trimming the video to be the size of audio
    def create_video(self, title, internal_text,outputpath): #function to create the final video to upload
        self.create_audio(title, internal_text) #first we create the audio for the clip
        audio = whisper.load_audio("output.mp3") #next load into whispers model
        data = self.model.transcribe(audio)# then we create captions for the audio with time stamps
        random_vid = self.choose_random_file(os.getcwd() + "/videos") #note I chose a random video from the videos directory so its somewhat different each time
        self.merge_audio_video("output.mp3",random_vid,"temp.mp4")
        self.add_captions("temp.mp4" ,data["segments"],outputpath) #finally I add the captions and save the video
    def add_captions(self, video_file, segments, output_file):
        video = VideoFileClip(video_file)  # Load the video
        # position = (video.size[0]//2, video.size[1]) #putting the caption somewhere near the bottom center
        captions = [] #the  clips that contain the captions and their time stamps will be stored here

        for segment in segments:
            caption_clip = TextClip(
                segment["text"], #the segment contains time stamps and text so i take the text part here
                fontsize=70, #this seems like a pretty good size but might be experimented with
                color="purple", #put a color here I put purple so it shows for both dark and light videos
                bg_color="transparent", #we already have a video at the back so we should make the caption video transparent
                method="caption", #making it caption so it wraps if it exceeds the size
                align="center", #putting at center
                size=video.size, #setting size to be that of the original video
                stroke_color="white",  # putting white outline
                stroke_width=3,        # making the size of outline
                font="Comic-Sans MS",  # using a more funner font
            ).set_position(("center","bottom"),relative = True).set_start(segment["start"]).set_end(segment["end"]) #creating the clips of which contain a the caption a long with time stamp saved in segement as start and end and putting it at the bottom center
            captions.append(caption_clip) #adding it to the captions array to be all merged at the end to save time
        final_clip = CompositeVideoClip([video] + captions, size=video.size) #merge the captions and the video needs to be fixed should be center bottom but for some reason is at center. doesnt look bad though so kept for now
        final_clip.write_videofile(output_file, codec="libx264", audio_codec="aac", fps=60) #write the file
test= automate()
subredditpost = test.parse_subreddit()
test.create_video(subredditpost[1].title,subredditpost[1].selftext,os.getcwd() + "/upload/test.mp4")
# process_video("parkour.mp4",120)