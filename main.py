
import openai
import requests
import os
from datetime import datetime

# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_FORM_URL = os.getenv("GOOGLE_FORM_URL")

def generate_video_idea():
    openai.api_key = OPENAI_API_KEY
    prompt = "Give me a viral TikTok or YouTube Shorts idea for today. Format: Title, Hook, Script"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    idea = response['choices'][0]['message']['content']
    return idea

def generate_veo_prompt(script):
    openai.api_key = OPENAI_API_KEY
    prompt = f"Rewrite this short video script as a cinematic Google Veo video prompt: {script}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

def submit_to_google_form(title, hook, script, veo_prompt):
    payload = {
        "entry.123456": title,
        "entry.654321": hook,
        "entry.112233": script,
        "entry.445566": veo_prompt,
        "entry.778899": datetime.now().isoformat()
    }
    requests.post(GOOGLE_FORM_URL, data=payload)

def parse_idea(raw_text):
    try:
        lines = raw_text.strip().split("\n")
        title = lines[0].replace("Title:", "").strip()
        hook = lines[1].replace("Hook:", "").strip()
        script = " ".join([line.strip() for line in lines[2:] if "Script" not in line])
        return title, hook, script
    except Exception as e:
        return "Unknown", "N/A", raw_text

def main():
    idea = generate_video_idea()
    title, hook, script = parse_idea(idea)
    veo_prompt = generate_veo_prompt(script)
    submit_to_google_form(title, hook, script, veo_prompt)
    print("✅ Idea logged and prompt generated.")

if __name__ == "__main__":
    main()
