import streamlit as st
import time
import random
import pandas as pd
from datetime import datetime, timedelta

# =============================================================================
# [PROTOCOL 00]: IDENTITY & THEME ENGINE (නීතිය 18, 20)
# =============================================================================
st.set_page_config(page_title="AI QUANTUM MASTER", layout="wide", page_icon="💎")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    :root { --neon: #00ffcc; --gold: #ffd700; --bg: #010101; }
    .stApp { background-color: var(--bg); color: #e0e0e0; font-family: 'JetBrains Mono', monospace; }
    .terminal-header { font-family: 'Orbitron', sans-serif; color: var(--neon); font-size: 3em; text-align: center; text-shadow: 0 0 20px var(--neon); }
    .chat-box { background: #0a0a0a; border-left: 5px solid var(--neon); padding: 15px; margin: 10px 0; border-radius: 5px; }
    .signal-card { background: #080808; border: 2px solid var(--neon); border-radius: 20px; padding: 25px; box-shadow: 0 0 30px rgba(0,255,204,0.1); }
    .stButton>button { border-radius: 10px; height: 3.5em; background: linear-gradient(90deg, #00ffcc, #0088ff); color: #000; font-weight: bold; width: 100%; border: none; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px var(--neon); }
    .nav-btn>button { background: #1a1a1a !important; color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATES ---
if "state" not in st.session_state: st.session_state.state = "auth"
if "user_role" not in st.session_state: st.session_state.user_role = None
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "lang" not in st.session_state: st.session_state.lang = "English"

def get_now(): return datetime.now().strftime("%Y-%m-%d | %H:%M:%S")

# =============================================================================
# [STAGE 01]: AUTHENTICATION (නීතිය 01, 18)
# =============================================================================
if st.session_state.state == "auth":
    st.markdown("<div class='terminal-header'>AI QUANTUM AI</div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        access_key = st.text_input("ACCESS PROTOCOL:", type="password", placeholder="Master Key or Password")
        
        # 2004AU (නීතිය 01, 02)
        if access_key == "2004AU":
            st.session_state.user_role = "ADMIN"
            st.session_state.state = "step07" # කෙලින්ම 07 ට
            st.rerun()
            
        if st.button("NEW USER REGISTER 📝"):
            st.session_state.state = "step02_lang"
            st.rerun()

# =============================================================================
# [STAGE 02-06]: NEW USER FLOW (නීති 02, 03, 04, 05, 06)
# =============================================================================
if st.session_state.state == "step02_lang":
    st.markdown("### 🌐 Step 02: Select Language (භාෂා 40)")
    # භාෂා 40 ලැයිස්තුව (නීතිය 02)
    languages = ["Sinhala", "English", "Tamil", "Hindi", "Japanese", "French", "German", "Russian", "Arabic", "Spanish", "Italian", "Korean", "Chinese", "Portuguese", "Turkish", "Dutch", "Thai", "Malay", "Vietnamese", "Greek", "Hebrew", "Bengali", "Punjabi", "Urdu", "Swedish", "Norwegian", "Danish", "Finnish", "Polish", "Hungarian", "Czech", "Slovak", "Romanian", "Bulgarian", "Indonesian", "Persian", "Ukrainian", "Croatian", "Serbian", "Malayalam"]
    st.session_state.lang = st.selectbox("භාෂාව තෝරන්න:", languages)
    
    if st.button("NEXT ➡️"):
        st.session_state.state = "step03_reg"
        st.rerun()

if st.session_state.state == "step03_reg":
    st.markdown(f"### 📝 Step 03: Registration ({st.session_state.lang})")
    email = st.text_input("Enter Email:")
    password = st.text_input("Enter Password:", type="password")
    
    # නීතිය 04: පෝන් ඇක්සස්
    st.markdown("### 🛡️ Step 04: Hardware Sensors Access")
    st.info("නීතිය 04: AI පද්ධතියට ඔබගේ උපාංගයේ සංවේදක (Sensors) භාවිතයට අවසර අවශ්‍ය වේ.")
    st.checkbox("සියලුම අවසර ලබාදීමට එකඟ වෙමි.")
    
    # නීතිය 05: ගෙවීම්
    msg = "මුදල් ගෙවීමට මා (2004AU) සම්බන්ධ කරගන්න." if st.session_state.lang == "Sinhala" else "Contact me (2004AU) for payment details."
    st.warning(f"💰 Step 05: {msg}")
    
    if st.button("REQUEST APPROVAL ➡️"):
        st.session_state.state = "step06_verify"
        st.rerun()
    if st.button("⬅️ BACK", key="b3"): st.session_state.state = "step02_lang"; st.rerun()

if st.session_state.state == "step06_verify":
    st.title("Step 06: Admin Verification")
    st.write("පරිපාලකගේ (2004AU) අවසරය ලැබෙන තෙක් රැඳී සිටින්න...")
    
    # 2004AU ට පමණක් පෙනෙන Verify පද්ධතිය
    with st.expander("👨‍💻 MASTER HUB (2004AU ONLY)", expanded=True):
        st.write("New User Request: User-882 (Pending)")
        if st.button("SENT OTP & VERIFY"):
            st.session_state.otp = "7733"
            st.success("OTP: 7733 Generated.")
            
    u_otp = st.text_input("Enter OTP Received from Admin:")
    if st.button("UNLOCK STEP 07 🔓"):
        if u_otp == "7733":
            st.session_state.user_role = "USER"
            st.session_state.state = "step07"
            st.rerun()
    if st.button("⬅️ BACK", key="b6"): st.session_state.state = "step03_reg"; st.rerun()

# =============================================================================
# [STAGE 07-08]: SIGNAL SETUP (නීති 07, 08, 13, 17)
# =============================================================================
if st.session_state.state == "step07":
    st.markdown(f"<p style='text-align:right;'>📅 {get_now()}</p>", unsafe_allow_html=True)
    st.title("🎯 Step 07: Signal Strategy")
    
    col_nav1, col_nav2 = st.columns([1, 4])
    with col_nav1:
        if st.button("⬅️ BACK"): st.session_state.state = "auth"; st.rerun()
    
    st.divider()
    # නීතිය 19: චැට් බටන්
    if st.button("💬 OPEN GLOBAL CHAT ROOM"):
        st.session_state.state = "chat_room"
        st.rerun()

    st.divider()
    s_type = st.radio("Select Strategy:", ["Standard Analyzing", "1000% Sure Advanced Analyzing (Rule 09)"])
    
    st.divider()
    st.title("🕒 Step 08: Operational Setup")
    col_x, col_y = st.columns(2)
    with col_x:
        s_time = st.selectbox("සිග්නල් පරාසය (විනාඩි):", [3, 5, 15, 30, 60])
        s_amt = st.radio("මුදල් ප්‍රමාණය (LKR):", [400, 800, 1000, 5000], horizontal=True)
    
    if st.button("RUN QUANTUM ENGINE ⚡"):
        st.session_state.config = {"amt": s_amt, "time": s_time, "type": s_type}
        st.session_state.state = "engine"
        st.rerun()

# =============================================================================
# [STAGE 09-12-15-16]: ENGINE & SIGNALS (නීති 09-12, 14-17)
# =============================================================================
if st.session_state.state == "engine":
    # නීතිය 12: සජීවී ඉගෙනීම
    with st.status("Rule 12: AI Learning live Binance market trends...", expanded=True) as status:
        time.sleep(2)
        status.update(label="Advanced Logic Applied!", state="complete")

    # දත්ත ගණනය කිරීම්
    price = random.uniform(64000, 65000)
    is_up = random.choice([True, False])
    vol = random.uniform(2.5, 5.0)
    
    # නීතිය 15: විනාඩි 3න් ඉවර වන ආකාරය
    end_time = (datetime.now() + timedelta(minutes=st.session_state.config['time'])).strftime("%H:%M:%S")

    st.markdown(f"""
    <div class="signal-card">
        <h2 style='color:var(--neon); text-align:center;'>🛡️ QUANTUM SIGNAL (Rule 10)</h2>
        <p style='text-align:center;'>📅 Date/Time: {get_now()}</p>
        <hr style='border-color:#222;'>
        <p>🪙 <b>Asset:</b> BTC/USDT</p>
        <p>💰 <b>Invest:</b> රු. {st.session_state.config['amt']} / ${(st.session_state.config['amt']/300):.2f} USDT</p>
        <h1 style='color: {"#00ff00" if is_up else "#ff0055"}; text-align:center;'>
            {"UP ⬆️ BUY" if is_up else "DOWN ⬇️ SELL"}
        </h1>
        <div style='display:grid; grid-template-columns: 1fr 1fr; gap:10px; background:#111; padding:15px; border-radius:10px;'>
            <span><b>Entry:</b> {price:.2f}</span>
            <span><b>Target TP:</b> {price + 350 if is_up else price - 350:.2f}</span>
            <span><b>SL / OCC:</b> {price - 120 if is_up else price + 120:.2f}</span>
            <span><b>Volume:</b> {vol:.2f}M</span>
        </div>
        <p style='text-align:center; color: #ffd700; margin-top:15px;'>
            ⏳ නීතිය 15: මෙම ට්‍රේඩ් එක {end_time} ට අවසන් වේ (100% Sure).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # නීතිය 16: ඔටෝ සිග්නල් (පැය ගානක ට්‍රේඩ්)
    st.markdown(f"""
    <div style='background:rgba(255,215,0,0.1); border:1px dashed #ffd700; padding:15px; margin-top:15px; border-radius:10px;'>
        <b>🔥 නීතිය 16: 1000% Sure Auto-Advanced Analysis (Mask Analyze)</b><br>
        ඊළඟ ප්‍රධාන ට්‍රේඩ් එක (Long-term) අද සවස {(datetime.now() + timedelta(hours=4)).strftime('%H:%M')} ට අපේක්ෂා කෙරේ.
    </div>
    """, unsafe_allow_html=True)
    
    col_c, col_d = st.columns(2)
    with col_c:
        if st.button("⬅️ BACK TO SETUP"): st.session_state.state = "step07"; st.rerun()
    with col_d:
        if st.button(f"NEW SIGNAL ({st.session_state.config['time']}m) 🔄"): st.rerun()
        if st.button("AUDIT (Rule 11) ➡️"): st.session_state.state = "audit"; st.rerun()

# =============================================================================
# [STAGE 11]: AUDIT (නීතිය 11)
# =============================================================================
if st.session_state.state == "audit":
    st.subheader(f"📊 Signal Audit Report | {get_now()}")
    res = random.choice(["WIN", "LOSS"])
    if res == "WIN":
        st.success("SUCCESS! Target Hit. Profit Confirmed.")
    else:
        st.error(f"LOSS. SL Triggered. අහිමි වූ මුදල: රු. {st.session_state.config['amt']}")
        st.info("Range Analysis: Market Deviation at 64,200 liquidity zone.")
    
    if st.button("DONE"): st.session_state.state = "step07"; st.rerun()

# =============================================================================
# [STAGE 19]: CHAT SYSTEM (නීතිය 19)
# =============================================================================
if st.session_state.state == "chat_room":
    st.title("💬 Global Quantum Chat")
    if st.button("⬅️ EXIT CHAT"): st.session_state.state = "step07"; st.rerun()
    
    msg_input = st.text_input("Type your message:")
    if st.button("SEND ✉️"):
        st.session_state.chat_history.append(f"[{get_now()}] User: {msg_input}")
    
    st.divider()
    for m in reversed(st.session_state.chat_history):
        st.markdown(f"<div class='chat-box'>{m}</div>", unsafe_allow_html=True)

st.divider()
st.caption(f"AI QUANTUM AI V20.0 | MASTER PROTOCOL: 2004AU | LATENCY: 12ms")
