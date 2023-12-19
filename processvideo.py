from moviepy.video.io.VideoFileClip import VideoFileClip

def process_video(input_file, cut):
    video = VideoFileClip(input_file)
    video = video.without_audio().resize(height=1080, width= 1920)
    duration = video.duration
    num_segments = int(duration / cut)
    video.close()
    
    for i in range(num_segments):
        start = i * cut
        end = (i + 1) * cut
        segment = video.subclip(start, end)
        segment_output_file = f"segment_{i + 1}.mp4"
        segment.write_videofile(segment_output_file, codec="libx264", audio_codec="aac")
    video.close()