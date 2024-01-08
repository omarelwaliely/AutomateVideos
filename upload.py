import json
from instabot import Bot
import os
import shutil

class Upload:
    def __init__(self):
        if os.path.exists(os.getcwd() + "/config"): #removing previous config file to prevent bug in instabot
            shutil.rmtree(os.getcwd() + "/config")
        info = json.load(open('instagram.json')) #all the instagram information should be saved to the instagram json
        self.captions = json.load(open('captions.json')) #save captions here (edits the captions.json or create different implementation, but i liked it like this)
        self.username = info["username"] #save auth for later
        self.password = info["password"]
    def upload_to_instagram(self,video_path):
        bot = Bot() #we create an instance of the instabot module to use as a way of accessing instagram
        bot.login(username=self.username, password=self.password) #we first login
        bot.upload_video(video_path,caption = self.captions['default_caption']) #then we upload
        bot.logout() #and logout so we dont stay logged in later


        

