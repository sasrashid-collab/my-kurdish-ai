import streamlit as st
import sqlite3
import hashlib
import platform
import time

# --- ١. پاراستنی ئامێر (Hardware Security) ---
def get_device_id():
    # دروستکردنی ناسنامەیەکی ناوازە بەپێی جۆری ئامێرەکە (مۆبایل یان کۆمپیوتەر)
    device_info = platform.node() + platform.processor() + platform.system()
    return hashlib.sha256(device_info.encode()).hexdigest()[:16]

# --- ٢. دروستکردنی داتابەیسی ناوخۆیی (Local Database) ---
def init_local_db():
    conn = sqlite3.connect('local_user_data.db', check_same_thread=False)
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS projects (id INTEGER PRIMARY KEY, name TEXT, status TEXT)')
    conn.commit()
    return conn

# --- ٣. ڕێکخستنی لاپەڕە و دیزاین ---
st.set_page_config(page_title="AI Maker Studio | Pro", layout="wide", initial_sidebar_state="expanded")

# دیزاینی CSS بۆ جوانکردنی ڕووکارەکە
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button {
        width: 100%; border-radius: 10px; height: 3em;
        background: linear-gradient(135deg, #6e8efb, #a7a7af);
        color: white; border: none; font-weight: bold;
    }
    .status-box {
        padding: 20px; border-radius: 15px; border: 1px solid #333;
        background-color: #161b22; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- ٤. لۆژیکی سەرەکی بەرنامەکە ---
def main():
    st.title("⚡ AI Maker Studio: Professional Hub")
    
    # زانیاری ئامێر لە سایدبار
    dev_id = get_device_id()
    st.sidebar.title("🔐 ئاسایشی سیستم")
    st.sidebar.text(f"ناسنامەی ئامێر:\n{dev_id}")
    st.sidebar.markdown("---")
    
    # مینۆی سەرەکی
    menu = st.sidebar.radio("بڕۆ بۆ بەشی:", ["🏠 ماڵەوە", "🏗️ کارگەی دروستکردن", "📦 کۆگای ناوخۆیی", "💳 مۆڵەت و کڕین"])

    if menu == "🏠 ماڵەوە":
        st.markdown('<div class="status-box"><h3>بەخێرهاتی بۆ گەورەترین پلاتفۆرمی پەرەپێدان</h3><p>لێرەدا دەتوانیت یاری مەزن و سیستەمی ئاڵۆز دروست بکەیت و بیپارێزیت.</p></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.info("🎯 **ئامانجی سیستم:** پاراستنی کۆدی گەنجان و بازرگانیکردن پێیانەوە.")
        with col2:
            st.success("✅ **دۆخی ئامێر:** ئەم ئامێرە ناسراوە و داتابەیسی ناوخۆیی چالاکە.")

    elif menu == "🏗️ کارگەی دروستکردن":
        st.header("🛠️ کارگەی دروستکردنی پڕۆژە")
        p_name = st.text_input("ناوی پڕۆژە (بۆ نموونە: سیستەمی کۆگا)")
        p_desc = st.text_area("وەسفی وردی لۆژیکی پڕۆژەکە:")
        
        if st.button("🚀 داڕشتنی سیستەمی پارێزراو"):
            if p_name and p_desc:
                with st.spinner("خەریکی دروستکردنی قاوغی بەرنامە و بەستنەوەم بە سێرڤەر..."):
                    time.sleep(2)
                    st.code(f"# Secure Output for: {p_name}\n# Encrypted Logic is stored on AI Maker Server\nprint('Access Granted for Device: {dev_id}')", language="python")
                    st.success("پڕۆژەکە دروستکرا و تەنها لەسەر ئەم ئامێرە کار دەکات.")
            else:
                st.warning("تکایە هەموو خانەکان پڕ بکەرەوە.")

    elif menu == "📦 کۆگای ناوخۆیی":
        st.header("💾 داتابەیسی ناوخۆیی ئامێرەکە")
        conn = init_local_db()
        st.write("ئەم داتایانە تەنها لەسەر مۆبایل یان کۆمپیوتەرەکەت پاشەکەوت کراون:")
        # پیشاندانی داتای ناوخۆیی (بۆ ئێستا بەتاڵە)
        st.info("داتابەیسی SQLite چالاکە و ئامادەیە بۆ وەرگرتنی زانیاری فرۆشتن و بەکارهێنەران.")

    elif menu == "💳 مۆڵەت و کڕین":
        st.header("🔑 چالاککردنی مۆڵەت (License)")
        license_key = st.text_input("کلیلی چالاککردن داخڵ بکە:")
        if st.button("پشکنین"):
            st.error("ئەم کلیلە کارا نییە. تکایە پەیوەندی بە کارگێڕی بکە.")

if __name__ == "__main__":
    main()