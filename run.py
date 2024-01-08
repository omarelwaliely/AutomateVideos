from upload import Upload
from automate import Automate
import schedule
import time
import os

def upload_to_all_platforms(uploader: Upload):
    parse = os.getcwd() + "/upload/"
    filename = parse + os.listdir(parse)[0]
    uploader.upload_to_instagram(parse + filename) #currently only platform is instagram but ill add more under here
    os.remove(filename)

video_creater = Automate()
uploader = Upload()
video_creater.replacement_words['aka'] = 'also known as' #example of setting a replacement word yourself

def create_videos(): #making a function for this so i can use it as a lambda funuction in the scheduler
    video_creater.create_videos_all("subredditnamehere", 5, 1, os.getcwd() + "/upload")
    print('Creating videos')

# Scheduling is done here
schedule.every().day.at("00:00").do(lambda: create_videos, 'creating all videos')
for i in range(12, 17):
    schedule.every().day.at(f"{str(i)}:00").do(upload_to_all_platforms(uploader), 'uploaded to all platforms')

#running according to the scheduler is done here
while 1:
    schedule.run_pending()
    time.sleep(1)
