import yt_dlp
import os
import imageio_ffmpeg

def download_video_clip(url, output_filename, start_time=0, duration=10):
    """
    Downloads a specific clip from a YouTube URL.
    """
    output_dir = "content/clips"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_path = os.path.join(output_dir, f"{output_filename}.mp4")
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
    ffmpeg_dir = os.path.dirname(ffmpeg_exe)
    
    # Create a local 'bin' directory and symlink/copy ffmpeg.exe if it doesn't exist
    # This helps yt-dlp and other tools that look for 'ffmpeg.exe' specifically
    base_dir = os.path.dirname(os.path.abspath(__file__))
    local_bin = os.path.join(base_dir, "bin")
    if not os.path.exists(local_bin):
        os.makedirs(local_bin)
    
    local_ffmpeg = os.path.join(local_bin, "ffmpeg.exe")
    if not os.path.exists(local_ffmpeg):
        import shutil
        try:
            shutil.copy2(ffmpeg_exe, local_ffmpeg)
        except Exception:
            pass # Fallback to path modification if copy fails
            
    if local_bin not in os.environ["PATH"]:
        os.environ["PATH"] = local_bin + os.pathsep + os.environ["PATH"]
    
    # Preferred format: Single file mp4 if possible, fallback to best quality
    # We avoid the '+' operator to prevent merging errors if ffprobe is missing
    format_str = 'best[ext=mp4][height<=720]/best[height<=720]/best'
    
    ydl_opts = {
        'format': format_str,
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'download_ranges': lambda info_dict, ydl: [{'start_time': start_time, 'end_time': start_time + duration}],
        'force_keyframes_at_cuts': True,
        'ffmpeg_location': local_bin, # Use the directory path
        'quiet': True,
        'no_warnings': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return output_path
    except Exception as e:
        print(f"Partial download failed: {e}. Trying full download and local clip...")
        # Fallback: Download full and clip locally
        full_video_path = os.path.join(output_dir, f"{output_filename}_full.mp4")
        ydl_opts_full = {
            'format': 'best[ext=mp4][height<=720]/best[height<=720]/best',
            'outtmpl': full_video_path,
            'quiet': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts_full) as ydl:
                ydl.download([url])
            
            # Clip with moviepy
            from moviepy import VideoFileClip
            video = VideoFileClip(full_video_path)
            clip = video.subclipped(start_time, start_time + duration)
            clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
            video.close()
            clip.close()
            
            # Remove full video
            if os.path.exists(full_video_path):
                os.remove(full_video_path)
                
            return output_path
        except Exception as fallback_e:
            error_msg = f"Error downloading YouTube clip: {fallback_e}"
            print(error_msg)
            raise Exception(error_msg)

def search_youtube_links(query, max_results=3):
    """
    Searches for YouTube videos based on a query.
    Note: Standard yt-dlp doesn't have a direct search-then-return-urls API easily,
    so we use the 'ytsearch' prefix.
    """
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    search_query = f"ytsearch{max_results}:{query}"
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(search_query, download=False)
            if 'entries' in result:
                return [{"title": entry['title'], "url": f"https://www.youtube.com/watch?v={entry['id']}"} for entry in result['entries']]
            return []
    except Exception as e:
        print(f"Error searching YouTube: {e}")
        return []
