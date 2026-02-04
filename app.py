import streamlit as st
import google.generativeai as genai
import prompts
import voice_engine
import video_engine
import downloader
import os
import glob

# Page Config
st.set_page_config(page_title="Oromo Heritage AI", page_icon="🇪🇹", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #fdfaf6;
    }
    .stButton>button {
        background-color: #008000;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #006400;
        color: white;
    }
    h1, h2, h3 {
        color: #8b4513;
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Settings")
    # Try to load from secrets, otherwise empty
    default_key = st.secrets["GEMINI_API_KEY"] if "GEMINI_API_KEY" in st.secrets else ""
    api_key = st.text_input("Enter Gemini API Key", type="password", value=default_key)
    channel_handle = st.text_input("YouTube Channel Handle", value="@Wakjira-b8c")
    
    st.divider()
    st.markdown(f"### Channel: {channel_handle}")
    st.info(f"This tool is optimized for {channel_handle} to share Oromo history, culture, and struggle with the world.")

# Initialize Gemini
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=prompts.SYSTEM_PROMPT)
else:
    st.warning("Please enter your Gemini API Key in the sidebar to start.")

# Header
st.title("🌳 Oromo Heritage AI Generator")
st.subheader("Create high-quality content about History, Culture, and Politics")

# Tabs for different functions
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["🎥 Video Script", "🔍 SEO & Metadata", "📚 Historical Research", "📈 Channel Strategy", "🎙️ Voice Generator", "🎬 Video Creator", "🎞️ Video Editor"])

with tab1:
    st.header("Generate Video Script")
    topic_script = st.text_input("Enter Video Topic (e.g., The Gadaa System, The Battle of Gulale, Oromo Culture)")
    if st.button("Generate Script"):
        if api_key and topic_script:
            with st.spinner("Writing script..."):
                try:
                    prompt = prompts.get_script_prompt(topic_script)
                    response = model.generate_content(prompt)
                    st.markdown("### Generated Script")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Please provide an API key and a topic.")

with tab2:
    st.header("SEO & Metadata")
    topic_seo = st.text_input("Enter Topic for SEO Optimization")
    if st.button("Generate SEO Metadata"):
        if api_key and topic_seo:
            with st.spinner("Generating SEO tags..."):
                try:
                    prompt = prompts.get_seo_prompt(topic_seo)
                    response = model.generate_content(prompt)
                    st.markdown("### Titles, Description & Tags")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Please provide an API key and a topic.")

with tab3:
    st.header("Historical Research Summary")
    topic_research = st.text_input("Enter Historical Fact or Event to Research")
    if st.button("Generate Summary"):
        if api_key and topic_research:
            with st.spinner("Researching..."):
                try:
                    prompt = prompts.get_research_prompt(topic_research)
                    response = model.generate_content(prompt)
                    st.markdown("### Research Summary")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Please provide an API key and a topic.")

with tab4:
    st.header("📈 Channel Growth Strategy")
    st.write(f"Generate a customized strategy for **{channel_handle}**")
    if st.button("Generate Growth Plan"):
        if api_key:
            with st.spinner("Analyzing and planning..."):
                try:
                    prompt = prompts.get_growth_strategy_prompt(channel_handle)
                    response = model.generate_content(prompt)
                    st.markdown("### Your Customized Growth Strategy")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Please provide an API key.")

with tab5:
    st.header("🎙️ Text-to-Speech Voice Generator")
    st.write("Convert your scripts into professional voiceovers.")
    
    tts_text = st.text_area("Paste your script text here", height=300, placeholder="Example: For centuries, the Oromo people have walked this land...")
    
    col1, col2 = st.columns(2)
    with col1:
        # Default to Afaan Oromo (Female) which is "en-KE-AsiliaNeural"
        voice_option = st.selectbox("Select Voice Model", list(voice_engine.VOICES.keys()), index=list(voice_engine.VOICES.keys()).index("Afaan Oromo (Female)"))
        voice_speed = st.slider("Voice Speed (%)", min_value=-50, max_value=50, value=0, step=5)
    with col2:
        audio_filename = st.text_input("Audio Filename", value="oromo_voiceover")
        voice_pitch = st.slider("Voice Pitch (Hz)", min_value=-50, max_value=50, value=0, step=5)

    if st.button("Generate Audio"):
        if tts_text:
            with st.spinner("Generating high-quality neural voice..."):
                try:
                    # Format rate and pitch for edge-tts
                    rate_str = f"{'+' if voice_speed >= 0 else ''}{voice_speed}%"
                    pitch_str = f"{'+' if voice_pitch >= 0 else ''}{voice_pitch}Hz"
                    
                    output_file = voice_engine.run_tts(tts_text, voice_option, audio_filename, rate=rate_str, pitch=pitch_str)
                    if os.path.exists(output_file):
                        st.success(f"Audio generated successfully: {audio_filename}.mp3")
                        st.audio(output_file)
                        with open(output_file, "rb") as f:
                            st.download_button(
                                label="Download Voiceover",
                                data=f,
                                file_name=f"{audio_filename}.mp3",
                                mime="audio/mpeg"
                            )
                    else:
                        st.error("Failed to generate audio file.")
                except Exception as e:
                    st.error(f"Error: {e}")
        else:
            st.error("Please paste some text to convert.")

with tab6:
    st.header("🎬 Video Creator")
    st.write("Merge your voiceovers and thumbnails into final videos.")
    
    # Selection from project folders
    audio_files = glob.glob("content/audio/*.mp3")
    image_files = glob.glob("content/*.png") + glob.glob("content/history/*.png") + \
                  glob.glob("*.png") + glob.glob("C:/Users/Wak/.gemini/antigravity/brain/05018379-5571-4970-ab84-119a5a6cabe2/*.png")
    
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        audio_choice = st.radio("Audio Source", ["AI Voiceover", "Keep Original YouTube Audio"])
        if audio_choice == "AI Voiceover":
            if audio_files:
                selected_audio = st.selectbox("Select Voiceover File", [os.path.basename(f) for f in audio_files])
            else:
                st.info("No audio files found. Go to 'Voice Generator' to create some first.")
                selected_audio = None
        else:
            selected_audio = "ORIGINAL"
            
    with col_v2:
        source_type = st.radio("Background Visuals", ["Generated Image", "YouTube Clip"])
        if source_type == "Generated Image":
            if image_files:
                selected_images = st.multiselect("Select Images/Thumbnails (Sequential)", [os.path.basename(f) for f in image_files])
            else:
                st.info("No images found. Generate some in the content tabs first.")
                selected_images = None
        else:
            yt_input_mode = st.radio("YouTube Input Mode", ["Search", "Direct URL"])
            
            if yt_input_mode == "Search":
                yt_query = st.text_input("Search YouTube for B-Roll", placeholder="Oromo celebration...")
                if st.button("Search YouTube"):
                    with st.spinner("Searching..."):
                        results = downloader.search_youtube_links(yt_query)
                        if results: st.session_state.yt_results = results
                        else: st.error("No results found.")
                
                if 'yt_results' in st.session_state:
                    selected_yt = st.selectbox("Select Clip from Results", 
                                               [f"{r['title']} ({r['url']})" for r in st.session_state.yt_results])
                    st.session_state.selected_yt_url = selected_yt.split("(")[-1].strip(")")
            else:
                direct_url = st.text_input("YouTube URL", value="https://youtu.be/c8oyqCdEQ8k?si=-Ra8sZ39_0tyWLFy")
                if direct_url:
                    st.session_state.selected_yt_url = direct_url
                    st.success("✅ YouTube Link ready!")

            # Add Clip Timing Controls
            st.divider()
            st.write("**Clip Settings**")
            c_col1, c_col2 = st.columns(2)
            with c_col1:
                clip_start = st.number_input("Start Time (seconds)", min_value=0, value=0)
            with c_col2:
                clip_dur = st.number_input("Duration (seconds)", min_value=1, max_value=60, value=10)
    
    video_out_name = st.text_input("Output Video Filename", value="oromo_final_video")
    
    if st.button("🎬 BUILD FINAL VIDEO"):
        if selected_audio and ( (source_type == "Generated Image" and selected_images) or (source_type == "YouTube Clip" and 'selected_yt_url' in st.session_state) ):
            
            with st.spinner("Assembling your Oromo Masterpiece..."):
                try:
                    if source_type == "Generated Image":
                        if selected_audio == "ORIGINAL":
                            st.error("Cannot use 'Original YouTube Audio' with static images. Please select a Voiceover.")
                        else:
                            full_audio_path = next(f for f in audio_files if os.path.basename(f) == selected_audio)
                            
                            # Get full paths for all selected images
                            full_image_paths = []
                            for img_name in selected_images:
                                full_path = next(f for f in image_files if os.path.basename(f) == img_name)
                                full_image_paths.append(full_path)
                                
                            video_path = video_engine.create_video(full_image_paths, full_audio_path, video_out_name)
                    else:
                        # Process YouTube Clip
                        with st.status("Fetching YouTube Clip...") as status:
                            clip_path = downloader.download_video_clip(st.session_state.selected_yt_url, "temp_broll", start_time=clip_start, duration=clip_dur)
                            if clip_path:
                                status.update(label="Processing Video...", state="running")
                                if selected_audio == "ORIGINAL":
                                    video_path = video_engine.create_video_with_clip(clip_path, output_filename=video_out_name, keep_original_audio=True)
                                else:
                                    full_audio_path = next(f for f in audio_files if os.path.basename(f) == selected_audio)
                                    video_path = video_engine.create_video_with_clip(clip_path, full_audio_path, video_out_name)
                            else:
                                video_path = None
                    
                    if video_path and os.path.exists(video_path):
                        st.success(f"Video created successfully! Download it below.")
                        st.video(video_path)
                        with open(video_path, "rb") as f:
                            st.download_button(label="📥 Download Video", data=f, file_name=f"{video_out_name}.mp4", mime="video/mp4")
                    else:
                        st.error("Failed to create video. Please check your source settings.")
                except Exception as e:
                    st.error("Error occurred. Check settings or URL.")
                    with st.expander("Technical Details"):
                        st.code(str(e))
        else:
            st.error("Please ensure all sources are selected correctly.")

with tab7:
    st.header("🎞️ Video Editor (Beta)")
    st.write("Post-process your videos: Trim, Speed Up/Down, Add Text.")
    
    # 1. Select Video
    video_files = glob.glob("content/videos/*.mp4") + glob.glob("content/videos/edited/*.mp4")
    # Sort by modification time to show newest first
    try:
        video_files.sort(key=os.path.getmtime, reverse=True)
    except:
        pass
        
    if video_files:
        selected_edit_video = st.selectbox("Select Video to Edit", [os.path.basename(f) for f in video_files])
        full_edit_path = next(f for f in video_files if os.path.basename(f) == selected_edit_video)
        
        st.video(full_edit_path)
        
        # 2. Controls
        st.divider()
        col_e1, col_e2 = st.columns(2)
        
        with col_e1:
            st.subheader("✂️ Trim & Speed")
            # We need duration. Let's try to guess or just let user input numbers.
            # Ideally we read metadata but lightweight way:
            st.info("Set start/end times. Leave End Time as 0 to keep until end.")
            edit_start = st.number_input("Start Time (sec)", min_value=0.0, value=0.0, step=0.5)
            edit_end = st.number_input("End Time (sec)", min_value=0.0, value=0.0, step=0.5)
            edit_speed = st.slider("Playback Speed", 0.5, 2.0, 1.0, 0.1)
            
        with col_e2:
            st.subheader("✍️ Add Text Overlay")
            overlay_text = st.text_input("Text Content (Optional)")
            if overlay_text:
                overlay_pos = st.selectbox("Position", ["center", "top", "bottom", "west", "east", "north", "south"])
                overlay_size = st.number_input("Font Size", 20, 200, 50)
                overlay_color = st.color_picker("Text Color", "#FFFFFF")
            
        edit_out_name = st.text_input("Edited Filename", value=f"edited_{selected_edit_video.split('.')[0]}")
        
        if st.button("RENDER EDITED VIDEO"):
            with st.spinner("Processing video... (This may take a moment)"):
                try:
                    text_conf = None
                    if overlay_text:
                        text_conf = {
                            'text': overlay_text,
                            'fontsize': overlay_size,
                            'color': overlay_color,
                            'position': overlay_pos
                        }
                    
                    out_path = video_engine.process_video(
                        full_edit_path,
                        start_time=edit_start,
                        end_time=edit_end if edit_end > 0 else None,
                        text_overlay=text_conf,
                        speed=edit_speed,
                        output_filename=edit_out_name
                    )
                    
                    if out_path and os.path.exists(out_path):
                        st.success("Video Edited Successfully!")
                        st.video(out_path)
                        with open(out_path, "rb") as f:
                            st.download_button(label="📥 Download Edited Video", data=f, file_name=f"{edit_out_name}.mp4", mime="video/mp4")
                    else:
                        st.error("Failed to save video.")
                        
                except Exception as e:
                    st.error(f"Error editing video: {e}")
                    
    else:
        st.info("No videos found in content/videos to edit. Create one in the Video Creator tab first!")

st.divider()
st.markdown(f"*Empowering {channel_handle} through technology. #OromoHistory #Bulbula*")
