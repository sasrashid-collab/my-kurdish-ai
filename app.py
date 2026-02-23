import os
from google.colab import userdata

# ١. دۆزینەوەی کلیلەکان بە شێوەیەکی خۆکار لەناو سیکریتەکاندا
all_secrets = os.environ # یان بەکارهێنانی userdata
g_key = None
x_key = None

# گەڕان بەدوای کلیلی Groq (بۆ وێنەکە)
for k in ['GROQ_API_KEY', 'GROK_KEY', 'GROQ', 'groq']:
    try:
        val = userdata.get(k)
        if val: 
            g_key = val
            break
    except: continue

# گەڕان بەدوای کلیلی Grok (بۆ چاتەکە)
for k in ['XAI_API_KEY', 'GROK_API_KEY', 'XAI', 'grok']:
    try:
        val = userdata.get(k)
        if val: 
            x_key = val
            break
    except: continue

# ٢. دروستکردنی فایلی سایتەکە بەو کلیلانەی دۆزراونەتەوە
with open('app.py', 'w') as f:
    f.write(f"""
import streamlit as st
from groq import Groq
from openai import OpenAI
import base64

# بەکارهێنانی ئەو کلیلانەی دۆزرانەوە
groq_client = Groq(api_key="{g_key}")
xai_client = OpenAI(api_key="{x_key}", base_url="https://api.x.ai/v1")

st.set_page_config(page_title="Kurdish AI Fixed", layout="wide")
st.title("🦁 Kurdish AI: Stable & Ready")

up = st.file_uploader("وێنەی پسوڵە یان دەق دابنێ", type=["jpg", "png", "jpeg"])
if up and st.button("🔍 شیکار بکە"):
    try:
        img_bytes = up.read()
        base64_image = base64.b64encode(img_bytes).decode('utf-8')
        with st.spinner("چاوەڕێ بکە..."):
            res = groq_client.chat.completions.create(
                model="llama-3.2-11b-vision-preview",
                messages=[{{
                    "role": "user",
                    "content": [
                        {{"type": "text", "text": "ئەم وێنەیە بە زمانی کوردی بە وردی شیکار بکە."}},
                        {{"type": "image_url", "image_url": {{"url": f"data:image/jpeg;base64,{{base64_image}}"}} }}
                    ]
                }}]
            )
            st.success("تەواو!")
            st.write(res.choices[0].message.content)
    except Exception as e:
        st.error(f"هەڵە لە سێرڤەر: {{e}}")
""")

# ٣. ڕاکردنی سێرڤەر
!streamlit run app.py & /usr/local/bin/cloudflared tunnel --url http://localhost:8501
