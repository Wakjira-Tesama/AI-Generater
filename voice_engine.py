import edge_tts
import asyncio
import os

# Available high-quality voices (Microsoft Edge Neural)
VOICES = {
    "Male (Steffan)": "en-US-SteffanNeural",
    "Male (Christopher)": "en-US-ChristopherNeural",
    "Female (Ava)": "en-US-AvaNeural",
    "Female (Emma)": "en-US-EmmaNeural",
    "Male (Ryan - British)": "en-GB-RyanNeural",
    "Female (Sonia - British)": "en-GB-SoniaNeural",
    "Afaan Oromo (Female)": "en-KE-AsiliaNeural",
    "Afaan Oromo (Male)": "am-ET-AmehaNeural"
}

async def generate_speech(text, voice, output_path, rate="+0%", pitch="+0Hz"):
    """Generates an MP3 file from text using edge-tts."""
    try:
        communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
        await communicate.save(output_path)
        return True
    except Exception as e:
        print(f"Error generating speech: {e}")
        return False

def run_tts(text, voice_key, filename, rate="+0%", pitch="+0Hz"):
    """Wrapper to run the async generator."""
    voice = VOICES.get(voice_key, "en-US-AvaNeural")
    output_dir = "content/audio"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    output_path = os.path.join(output_dir, f"{filename}.mp3")
    asyncio.run(generate_speech(text, voice, output_path, rate, pitch))
    return output_path
