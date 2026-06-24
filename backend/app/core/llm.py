import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def parse_analysis_response(text: str) -> dict:
    result = {
        "summary": "",
        "pros": "",
        "cons": "",
        "verdict": "",
        "confidence": 0.5,
    }

    for line in text.strip().splitlines():
        if line.startswith("SUMMARY:"):
            result["summary"]=line.replace("SUMMARY:","").strip()
        elif line.startswith("PROS"):
            result["pros"]=line.replace("PROS:","").strip()
        elif line.startswith("CONS:"):
            result["cons"]=line.replace("CONS:","").strip()
        elif line.startswith("VERDICT:"):
            result["veridct"]=line.replace("VERDICT:","").strip()
        elif line.startswith("CONFIDENCE:"):
            try:
                result["confidence"]=float(line.replace("CONFIDENCE:","").strip())

            except ValueError:
                result["confidence"]=0.5
    
    return result

def generate_analysis(prompt: str) -> dict:
    response = model.generate_content(prompt)
    raw_text=response.text
    parsed =parse_analysis_response(raw_text)
    parsed["model_used"]="gemini-2.5-flash"
    parsed["prompt_tokens"]=len(prompt.split())

    return parsed
