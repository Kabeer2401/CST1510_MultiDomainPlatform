import streamlit as st
import time  # We need this to fake the "typing" delay

st.set_page_config(page_title="AI Security Assistant", page_icon="🤖", layout="wide")

# --- SECURITY CHECK ---
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.error("You must be logged in to use the AI Assistant.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")
    st.stop()

st.title("🛡️ AI Security Architect")
st.caption("Powered by OpenAI GPT-4o (Simulation Mode)")

# --- INITIALIZE CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful Security Assistant."}
    ]

# --- DISPLAY HISTORY ---
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- CHAT INPUT & LOGIC ---
prompt = st.chat_input("Ask about a threat or incident...")

if prompt:
    # 1. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Show Fake AI Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # This is the "Stunt Double". It pretends to be smart.
        fake_answer = """
        Based on my analysis of the Cybersecurity domain, a SQL Injection attack occurs when malicious SQL statements are inserted into entry fields for execution. 

        **Recommendations:**
        1. Use prepared statements (parameterized queries).
        2. Use stored procedures.
        3. Validate all user inputs.
        """

        # This makes it type one word at a time, just like the real AI
        for word in fake_answer.split():
            full_response += word + " "
            message_placeholder.markdown(full_response + "▌")
            time.sleep(0.1)  # Wait a tiny bit to look like thinking

        # Final finish
        message_placeholder.markdown(full_response)

    # 3. Save to History
    st.session_state.messages.append({"role": "assistant", "content": full_response})
