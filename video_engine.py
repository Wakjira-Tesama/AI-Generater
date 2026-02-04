from moviepy.editor import ImageClip, AudioFileClip, VideoFileClip, concatenate_videoclips
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

def create_video(image_paths, audio_path, output_filename):
    """
    Creates a video by merging image(s) and an audio file.
    If multiple images are provided, they are displayed sequentially.
    The total video duration matches the audio duration.
    """
    output_dir = "content/videos"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, f"{output_filename}.mp4")
    
    try:
        # Load audio to get duration
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
        
        # Determine image inputs
        if isinstance(image_paths, str):
            image_paths = [image_paths]
            
        if not image_paths:
            raise ValueError("No images provided for video creation.")
            
        # Calculate duration per image
        duration_per_image = total_duration / len(image_paths)
        
        clips = []
        for img_path in image_paths:
            clip = ImageClip(img_path).with_duration(duration_per_image)
            clips.append(clip)
            
        # Concatenate clips
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Set audio to clip
        final_video = final_video.with_audio(audio)
        
        # Write file (low preset for speed, 24fps)
        # Using libx264 for high compatibility
        final_video.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", temp_audiofile='temp-audio.m4a', remove_temp=True)
        
        return output_path
    except Exception as e:
        import traceback
        error_msg = f"Error creating video: {e}\n{traceback.format_exc()}"
        print(error_msg)
        raise Exception(error_msg)

        raise Exception(error_msg)


def process_video(video_path, start_time=0, end_time=None, text_overlay=None, speed=1.0, output_filename="edited_video"):
    """
    Process an existing video: Trim, Speed, Text Overlay
    """
    output_dir = "content/videos/edited"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, f"{output_filename}.mp4")
    
    try:
        from moviepy.editor import TextClip, CompositeVideoClip, vfx
        
        clip = VideoFileClip(video_path)
        
        # 1. Trim
        if end_time is None or end_time == 0:
            end_time = clip.duration
        
        # Ensure times are valid
        start_time = max(0, start_time)
        end_time = min(clip.duration, end_time)
        
        if start_time < end_time:
            clip = clip.subclipped(start_time, end_time)
            
        # 2. Speed
        if speed != 1.0:
            clip = clip.with_effects([vfx.MultiplySpeed(speed)])
            
        # 3. Text Overlay
        if text_overlay:
            # text_overlay is a dict: {'text': str, 'fontsize': int, 'color': str, 'position': str/tuple}
            txt_clip = TextClip(
                text=text_overlay['text'],
                font='Arial', 
                font_size=text_overlay.get('fontsize', 50),
                color=text_overlay.get('color', 'white'),
                stroke_color='black',
                stroke_width=2
            )
            
            pos = text_overlay.get('position', 'center')
            txt_clip = txt_clip.with_position(pos).with_duration(clip.duration)
            
            clip = CompositeVideoClip([clip, txt_clip])
            
        # Write file
        clip.write_videofile(output_path, fps=24, codec="libx264", audio_codec="aac", temp_audiofile='temp-edit-audio.m4a', remove_temp=True)
        
        return output_path
        
    except Exception as e:
        import traceback
        error_msg = f"Error processing video: {e}\n{traceback.format_exc()}"
        print(error_msg)
        raise Exception(error_msg)
