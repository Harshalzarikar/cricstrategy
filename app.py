import streamlit as st
import ollama
import os
import requests
import json
import time

# Function to read player files and return their names
def get_player_files(directory):
    return [f for f in os.listdir(directory) if f.endswith('.txt')]

# Function to read the content of a selected file
def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Streamlit app
st.title("Cricket GPT - Interactive Analysis with Deepseek 🏏")

# Sidebar for player selection
st.sidebar.header("Player Selection")
player_directory = 'players'

try:
    player_files = get_player_files(player_directory)
except FileNotFoundError:
    st.sidebar.error("Please create a 'players' directory and add player files (.txt)")
    player_files = []

selected_file = st.sidebar.selectbox(
    "Select a player file",
    player_files if player_files else ["No files found"]
)

# Get player name
BATSMAN_NAME = selected_file.rsplit('.', 1)[0] if selected_file != "No files found" else ""

# System context for the chat
SYSTEM_CONTEXT = f"""You are a cricket analyst and commentator specializing in T20 cricket. 
Your expertise includes:
1. Ball-by-ball strategy analysis
2. Field placement recommendations
3. Player strengths and weaknesses
4. Live commentary

Currently analyzing player: {BATSMAN_NAME}

Remember to follow cricket rules and provide practical, evidence-based insights."""

# Add system context to messages if empty
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "system",
        "content": SYSTEM_CONTEXT
    })

# URL input for live commentary
st.sidebar.header("Live Commentary")
URL = st.sidebar.text_input(
    "Cricinfo API URL",
    value="https://hs-consumer-api.espncricinfo.com/v1/pages/match/comments?seriesId=1367856&matchId=1384433&inningNumber=1&commentType=ALL&fromInningOver=2"
)

def get_ball_by_ball_commentary(URL):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(URL, params={}, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Chat interface
for message in st.session_state.messages:
    if message["role"] != "system":  # Don't display system messages
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Quick action buttons
st.sidebar.header("Quick Actions")
if st.sidebar.button("Get Strategy"):
    strategy_prompt = f"""Devise a detailed T20 strategy for getting {BATSMAN_NAME} out:
1. Ball-by-ball plan
2. Field placements
3. Specific bowler recommendations
4. Evidence-based reasoning"""
    
    if selected_file != "No files found":
        try:
            player_content = read_file(os.path.join(player_directory, selected_file))
            strategy_prompt += f"\n\nRecent history:\n{player_content}"
        except Exception as e:
            st.error(f"Error reading player file: {e}")
    
    st.session_state.messages.append({"role": "user", "content": strategy_prompt})
    st.rerun()

if st.sidebar.button("Get Live Commentary"):
    content = get_ball_by_ball_commentary(URL)
    if content:
        commentary_prompt = """Provide ball-by-ball commentary for the following cricket data. 
        Include over number, delivery details, and witty insights in the style of a famous cricket commentator."""
        commentary_prompt += f"\n\nMatch data: {json.dumps(content)}"
        
        st.session_state.messages.append({"role": "user", "content": commentary_prompt})
        st.rerun()

# User input
user_input = st.chat_input("Type your cricket analysis question...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Get response from Ollama
    try:
        with st.spinner("Thinking..."):
            response = ollama.chat(
                model="deepseek-r1:1.5b",
                messages=st.session_state.messages
            )
            bot_response = response["message"]["content"]
            
            # Add bot response to history
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
    except Exception as e:
        st.error(f"Error getting response from Ollama: {e}")
    
    # Refresh the UI
    st.rerun()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("<font color=green>Thanks to Cricinfo</font>", unsafe_allow_html=True)
st.sidebar.markdown("Using locally installed Deepseek-r1:1.5b model")
st.sidebar.markdown("<font color=red>Note: Responses may vary due to the nature of LLMs</font>", unsafe_allow_html=True)