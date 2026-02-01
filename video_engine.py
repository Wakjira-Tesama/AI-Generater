from moviepy import ImageClip, AudioFileClip, VideoFileClip
import os

def create_video_with_clip(clip_path, audio_path=None, output_filename="final_video", keep_original_audio=False):
    """
    Creates a video from a clip. Can merge with new audio or keep original.
    """
    output_dir = "content/videos"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, f"{output_filename}.mp4")
    
    try:
        video = VideoFileClip(clip_path)
        
        if not keep_original_audio and audio_path:
            # Replace audio
            audio = AudioFileClip(audio_path)
            video = video.without_audio().with_duration(audio.duration)
            if video.duration < audio.duration:
                # Loop video to match audio length
                video = video.loop(duration=audio.duration)
            final_video = video.with_audio(audio)
        else:
            # Keep original audio
            final_video = video
            
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", temp_audiofile='temp-video-audio.m4a', remove_temp=True)
        return output_path
    except Exception as e:
        import traceback
        error_msg = f"Error creating video with clip: {e}\n{traceback.format_exc()}"
        print(error_msg)
        raise Exception(error_msg)

def create_video(image_path, audio_path, output_filename):
    """
    Creates a video by merging an image and an audio file.
    The video duration matches the audio duration.
    """
    output_dir = "content/videos"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, f"{output_filename}.mp4")
    
    try:
        # Load audio to get duration
        audio = AudioFileClip(audio_path)
        
        # Create image clip with same duration
        clip = ImageClip(image_path).with_duration(audio.duration)
        
        # Set audio to clip
        clip = clip.with_audio(audio)
        
        # Write file (low preset for speed, 24fps)
        # Using libx264 for high compatibility
        clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
        
        return output_path
    except Exception as e:
        import traceback
        error_msg = f"Error creating video: {e}\n{traceback.format_exc()}"
        print(error_msg)
        raise Exception(error_msg)
