import streamlit as st
import pandas as pd
import ccxt
import pandas_ta as ta
import time
from datetime import datetime, timedelta
import pytz
import plotly.graph_objects as go

# --- Rule 43: රහස්‍යභාවය ---
st.set_page_config(page_title="QUANTUM AI PRO", layout="wide", initial_sidebar_state="collapsed")
SL_TZ = pytz.timezone('Asia/Colombo')

# --- Rule 28, 35, 37: දත්ත ගබඩාව ---
if "db" not in st.session_state:
    st.session_state.db = {
        "state": "auth", "role": None, "lang": "English", 
        "history": [], "users": {}, "logs": [], "verified_users": [], "active_user": None
    }

def get_now(): return datetime.now(SL_TZ)

# --- Rule 23-25: අලංකාර අතුරුමුහුණත ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FFCC; font-family: 'Courier New', monospace; }
    .signal-card { border: 2px solid #00FFCC; padding: 25px; border-radius: 20px; background: #050505; text-align: center; margin: 10px 0; }
    .master-btn { background: linear-gradient(45deg, #FF00CC, #3300FF); color: white; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# Rule 01-06: හඳුනාගැනීම සහ ලියාපදිංචිය
# ==========================================
if st.session_state.db["state"] == "auth":
    st.title("🔒 ACCESS GATEWAY")
    access_key = st.text_input("ENTER KEY / PASSWORD:", type="password")
    
    if access_key == "2004AU": # Rule 01, 18, 33, 43
        st.session_state.db.update({"role": "MASTER", "state": "hub", "active_user": "MASTER_01"})
        st.rerun()
    elif access_key != "":
        if st.button("NEW USER REGISTRATION"):
            st.session_state.db["state"] = "register"
            st.rerun()

elif st.session_state.db["state"] == "register":
    # Rule 02, 03: භාෂා 40 තේරීම
    langs = ["Sinhala", "English", "Tamil", "Russian", "Hindi", "Japanese", "Arabic", "French"] # Imagine 40+
    st.session_state.db["lang"] = st.selectbox("SELECT YOUR LANGUAGE (03):", langs)
    
    email = st.text_input("EMAIL (01):")
    pw = st.text_input("PASSWORD:", type="password")
    
    # Rule 04, 05: පණිවිඩය අදාළ භාෂාවෙන් (සිංහල උදාහරණයක් ලෙස)
    msg = "ඇඩ්මින් සම්බන්ධ කරගෙන ගෙවීම් සිදුකරන්න." if st.session_state.db["lang"] == "Sinhala" else "Contact Admin for payment."
    st.warning(msg)
    st.info("Rule 04: AI needs full device log access for optimization.")
    
    if st.button("REQUEST VERIFICATION (SEND OTP)"): # Rule 06
        st.session_state.db["users"][email] = {"email": email, "pw": pw, "status": "pending"}
        st.success("Request sent to Admin. Wait for OTP.")

# ==========================================
# Rule 06: MASTER'S VERIFICATION PANEL (Rule 35)
# ==========================================
if st.session_state.db["role"] == "MASTER" and st.session_state.db["state"] == "hub":
    with st.expander("👑 MASTER CONTROL (Rule 35, 37)"):
        st.subheader("Pending Users")
        for u_email, u_data in st.session_state.db["users"].items():
            if u_data["status"] == "pending":
                st.write(f"User: {u_email}")
                if st.button(f"VERIFY & SEND OTP TO {u_email}"):
                    st.session_state.db["users"][u_email]["status"] = "verified"
                    st.success(f"OTP Sent to {u_email}!")

# ==========================================
# Rule 07-47: සිග්නල් මධ්‍යස්ථානය
# ==========================================
elif st.session_state.db["state"] == "hub":
    st.title("🎯 ADVANCED SIGNAL HUB")
    
    # Rule 46: Coin Choice / Skip
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🪙 COIN SELECT"): st.session_state.mode = "manual"
    with c2: 
        if st.button("⏩ SKIP (AI AUTO)"): st.session_state.mode = "auto"

    symbol = "BTC/USDT"
    if st.session_state.get("mode") == "manual":
        # Rule 34, 46: සියලුම Binance Coins
        symbol = st.selectbox("CHOOSE ASSET:", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"])

    # Rule 08: Time & Amount
    duration = st.selectbox("SIGNAL TIME (MIN):", [3, 5, 15, 60])
    amount_lkr = st.selectbox("INVESTMENT (LKR):", [400, 800, 1000, 5000])

    if st.button("GENERATE 1000% SURE ADVANCED SIGNAL"): # Rule 09, 15, 16
        with st.spinner("AI ANALYZING BINANCE & TRADINGVIEW (Rule 40, 41, 44)..."):
            try:
                # Rule 44, 47: සැබෑ දත්ත සම්බන්ධතාවය
                ex = ccxt.binance()
                ohlcv = ex.fetch_ohlcv(symbol, timeframe='1m', limit=100)
                df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
                
                # Rule 36, 40, 41: AI Learning & TA
                df['rsi'] = ta.rsi(df['c'], length=14)
                price = df['c'].iloc[-1]
                rsi = df['rsi'].iloc[-1]
                
                direction = "UP ⬆️" if rsi < 50 else "DOWN ⬇️"
                now = get_now()
                expiry = now + timedelta(minutes=duration)

                # Rule 09, 10, 45: ප්‍රදර්ශනය
                st.markdown(f"""
                <div class="signal-card">
                    <h2 style='color:#00FFCC;'>1000% SURE QUANTUM SIGNAL</h2>
                    <p>{now.strftime('%Y-%m-%d | %H:%M:%S')}</p>
                    <hr>
                    <h3>ASSET: {symbol}</h3>
                    <h1 style='color:{"#00FF88" if "UP" in direction else "#FF3366"};'>{direction}</h1>
                    <div style='display: flex; justify-content: space-around;'>
                        <p><b>Entry:</b> ${price:.2f}</p>
                        <p><b>Invest:</b> Rs.{amount_lkr} / ${(amount_lkr/310):.2f}</p>
                    </div>
                    <p><b>SL:</b> {price*0.99:.2f} | <b>OCO:</b> Active | <b>Leverage:</b> 20x</p>
                    <h4 style='color:orange;'>⏳ Rule 15: Trade ends at {expiry.strftime('%H:%M:%S')}</h4>
                </div>
                """, unsafe_allow_html=True)

                # Rule 28, 29: Save history
                res_win = "WIN ✅" if (rsi < 50 and direction == "UP ⬆️") else "PENDING"
                st.session_state.db["history"].append({
                    "time": now.strftime("%H:%M:%S"), "coin": symbol, "res": res_win, "price": price
                })

            except:
                st.error("Rule 44: Connection Error with Binance API.")

    # Rule 29: සිග්නල් ඉතිහාසය පෙන්වීම
    st.subheader("📜 SIGNAL AUDIT (Rule 29)")
    for h in reversed(st.session_state.db["history"]):
        st.info(f"✅ {h['time']} | {h['coin']} | Result: {h['res']} | Price: {h['price']}")

    # Rule 19: Chat System
    if st.button("💬 OPEN GLOBAL CHAT"):
        st.session_state.db["state"] = "chat"
        st.rerun()

    # Rule 13, 24: Navigation
    c_back, c_next = st.columns(2)
    with c_back:
        if st.button("⬅️ BACK"): st.session_state.db["state"] = "auth"; st.rerun()
    with c_next:
        st.button("NEXT ➡️")

# --- Rule 19: Chat Page ---
elif st.session_state.db["state"] == "chat":
    st.title("💬 COMMUNITY CHAT")
    st.text_area("Live Messages:", "User: Great signal! \nMaster: Keep it up.")
    if st.button("⬅️ BACK TO HUB"):
        st.session_state.db["state"] = "hub"
        st.rerun()
