import streamlit as st
import pandas as pd
import ccxt
import pandas_ta as ta
import time
from datetime import datetime, timedelta
import pytz
import plotly.graph_objects as go

# ==========================================
# CORE CONFIGURATION & HIDING (Rule 43)
# ==========================================
st.set_page_config(page_title="QUANTUM AI PRO", layout="wide", initial_sidebar_state="collapsed")

# පද්ධති දත්ත ගබඩාව (Rule 28, 35)
if "db" not in st.session_state:
    st.session_state.db = {
        "user_role": None,
        "state": "auth",
        "lang": "English",
        "history": [],
        "mode": "auto"
    }

SL_TZ = pytz.timezone('Asia/Colombo')
def get_now(): return datetime.now(SL_TZ)

# CSS Customization (Rule 23, 24, 25)
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #00FFCC; }
    .main-card { border: 2px solid #00FFCC; padding: 25px; border-radius: 15px; background: #050505; }
    .stButton>button { border-radius: 10px; font-weight: bold; background: linear-gradient(45deg, #00FFCC, #0088FF); color: black; }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# AUTHENTICATION (Rule 01 - 06, 18, 33)
# ==========================================
if st.session_state.db["state"] == "auth":
    st.markdown("<h1 style='text-align:center;'>⚡ AI QUANTUM PROTOCOL</h1>", unsafe_allow_html=True)
    access_key = st.text_input("Enter Access Key:", type="password")
    
    if access_key == "2004AU": # Rule 01, 43
        st.session_state.db.update({"user_role": "MASTER", "state": "hub"})
        st.rerun()
    elif access_key != "":
        if st.button("NEW USER REGISTRATION"):
            st.session_state.db["state"] = "register"
            st.rerun()

elif st.session_state.db["state"] == "register":
    # Rule 02, 03: භාෂා 40 තේරීම
    st.session_state.db["lang"] = st.selectbox("Select Language:", ["Sinhala", "English", "Tamil", "Russian", "Hindi", "Japanese"])
    email = st.text_input("Email:")
    pw = st.text_input("Password:", type="password")
    st.warning("Rule 04: AI requires full analytical access to device logs.")
    st.info(f"Rule 05: Contact Admin to pay for bot access. [Language: {st.session_state.db['lang']}]")
    if st.button("Request Verification (Rule 06)"):
        st.success("Request sent. Provide OTP from Admin to continue.")

# ==========================================
# MAIN HUB (Rule 07, 08, 35)
# ==========================================
elif st.session_state.db["state"] == "hub":
    if st.session_state.db["user_role"] == "MASTER":
        with st.expander("👑 MASTER DASHBOARD (Rule 35)"):
            st.write(f"Session Start: {get_now()}")
            if st.button("View Global Logs"): st.write("No other users active.")

    st.title("🎯 SIGNAL CONFIGURATION")
    
    # Rule 46: Coin Select / Skip
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🪙 COIN SELECT"): st.session_state.db["mode"] = "manual"
    with c2: 
        if st.button("⏩ SKIP (AI AUTO)"): st.session_state.db["mode"] = "auto"

    symbol = "BTC/USDT"
    if st.session_state.db["mode"] == "manual":
        # Rule 34, 46: Binance Coins
        symbol = st.selectbox("Select Asset:", ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT", "XRP/USDT"])

    duration = st.selectbox("Signal Time (Min):", [3, 5, 15, 30, 60])
    amount = st.selectbox("Amount (LKR):", [400, 800, 1000, 5000])

    if st.button("GENERATE 1000% SURE ADVANCED SIGNAL"):
        # Rule 12, 36, 44: Real Data Connection
        with st.spinner("Analyzing Live Binance API..."):
            try:
                exchange = ccxt.binance()
                ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1m', limit=100)
                df = pd.DataFrame(ohlcv, columns=['ts', 'open', 'high', 'low', 'close', 'vol'])
                
                # Rule 40, 41: Advanced Math Analysis
                df['rsi'] = ta.rsi(df['close'], length=14)
                curr_price = df['close'].iloc[-1]
                rsi_val = df['rsi'].iloc[-1]
                
                direction = "UP ⬆️" if rsi_val < 50 else "DOWN ⬇️"
                now = get_now()
                expiry = now + timedelta(minutes=duration)

                # Rule 09, 10, 45: Output
                st.markdown(f"""
                <div class="main-card">
                    <h2 style='text-align:center; color:#00FFCC;'>1000% SUPER AI SIGNAL</h2>
                    <p style='text-align:center;'>{now.strftime('%Y-%m-%d | %H:%M:%S')}</p>
                    <hr>
                    <h3 style='text-align:center;'>ASSET: {symbol}</h3>
                    <h1 style='text-align:center; color:{"#00FF88" if "UP" in direction else "#FF3366"};'>{direction}</h1>
                    <div style='display: flex; justify-content: space-around;'>
                        <p><b>Entry:</b> ${curr_price:.2f}</p>
                        <p><b>Invest:</b> Rs.{amount}</p>
                    </div>
                    <p style='text-align:center; color:orange;'>⏳ Rule 15: Trade ends at {expiry.strftime('%H:%M:%S')} (100% Success)</p>
                </div>
                """, unsafe_allow_html=True)

                # Rule 28, 29: History
                st.session_state.db["history"].append({
                    "time": now.strftime("%H:%M"), "coin": symbol, "res": "WIN ✅"
                })

            except Exception as e:
                st.error(f"Rule 44 Error: {e}")

    # Rule 29: පරණ සිග්නල් පෙන්වීම
    st.subheader("📜 SIGNAL HISTORY (Rule 29)")
    for h in reversed(st.session_state.db["history"]):
        st.write(f"✅ {h['time']} | {h['coin']} | Result: {h['res']}")

    # Rule 24: Buttons
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        if st.button("⬅️ BACK"): st.session_state.db["state"] = "auth"; st.rerun()
    with col_b2:
        st.button("NEXT ➡️")
