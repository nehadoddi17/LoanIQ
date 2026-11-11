import os
from dotenv import load_dotenv
load_dotenv()

print("✅ dotenv OK")

has_openai = bool(os.getenv("OPENAI_API_KEY"))
has_groq = bool(os.getenv("GROQ_API_KEY"))
print(f"OPENAI key: {'✅ set' if has_openai else '❌ missing'}")
print(f"GROQ key:   {'✅ set' if has_groq else '❌ missing'}")

from groq import Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Try known chat models in order until one works
candidates = [
    "llama-3.1-8b-instant",
    "openai/gpt-oss-20b",
    "meta-llama/llama-4-scout-17b-16e-instruct",
    "llama-3.3-70b-versatile",
]

for model in candidates:
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say 'setup complete'"}],
            max_tokens=10,
        )
        print(f"✅ LLM WORKS with {model}: {resp.choices[0].message.content}")
        break
    except Exception as e:
        print(f"❌ {model}: {str(e)[:80]}")
else:
    print("⚠️ No model worked — paste the errors above")

