SYSTEM_PROMPT = """
You are an expert historian, cultural researcher, and content creator specializing in Oromo heritage. 
Your goal is to help users create high-quality, accurate, and engaging content about the Oromo people, 
their history (including the struggle against imperial systems), their politics (Gadaa system, etc.), and their rich culture.

When generating content:
1. Maintain a respectful and educational tone.
2. Use accurate historical terms (e.g., Gadaa, Finfinnee, Oromia).
3. Focus on empowering narratives while remaining factual.
4. If a topic is sensitive, present it with historical context and nuance.
5. Provide strategic advice for the YouTube channel '@Wakjira-b8c' (and other Oromo heritage channels) to reach a wider audience.
"""

def get_growth_strategy_prompt(channel_name):
    return f"""
Provide a comprehensive growth strategy for the YouTube channel: {channel_name}.
The channel focuses on Oromo history, culture, and struggle.
Include:
- 5 unique video series ideas.
- Advice on how to engage the Oromo diaspora and local communities.
- Collaboration ideas with other educators or influencers.
- Suggestions for community post topics to keep the audience engaged.
"""

def get_script_prompt(topic):
    return f"""
Generate a professional YouTube video script about: {topic}.
The script should include:
- A compelling hook (Intro)
- 3-5 main sections explaining the history/culture/politics
- A call to action (Cora, Like, Subscribe)
- Tone: Engaging and informative.
- Language: English (with Oromo terms where appropriate).
"""

def get_seo_prompt(topic):
    return f"""
Generate SEO metadata for a YouTube video about: {topic}.
Include:
- 3 catchy, high-CTR Titles.
- A descriptive, keyword-rich video description.
- 15-20 relevant tags (e.g., #OromoHistory, #GadaaSystem, #Ethiopia, #Culture).
"""

def get_research_prompt(topic):
    return f"""
Provide a detailed research summary on the historical topic: {topic}.
Focus on:
- Key dates and figures.
- The significance of the event in the Oromo struggle or culture.
- Social and political impact.
Include bullet points for easy reading.
"""
