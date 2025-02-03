Cricket GPT - Interactive Cricket Analysis with Deepseek 🏏
This project is an interactive cricket analysis tool built using Streamlit and Deepseek (Ollama). It provides real-time cricket analysis, live commentary, and strategic insights for cricket players, analysts, and fans.

Key Features:
Interactive Cricket Chatbot: Engage in conversations with an AI-powered cricket expert to get detailed insights on players, match strategies, and more.
Ball-by-Ball Commentary: Fetch live commentary data from Cricinfo API for ongoing matches.
Player Strategy: Get detailed strategies for dismissing a batsman in T20 cricket, including ball-by-ball plans, field placements, and bowler recommendations.
Data-Driven Insights: Integrates player performance data for evidence-based analysis and decision-making.
Technologies Used:
Python: Backend programming language.
Streamlit: Web framework for building the user interface.
Deepseek (Ollama API): AI model used for the cricket analysis chatbot.
Cricinfo API: API for fetching live ball-by-ball commentary.
File-Based Player Data: Historical player data to generate strategies and analysis.
Setup Instructions:
Clone the repository:
git clone https://github.com/yourusername/cricket-gpt.git
cd cricket-gpt

Install the required packages: Make sure you have Python 3.7+ installed. Then, run:


pip install -r requirements.txt


Run the Streamlit app: Start the app locally using:
streamlit run app.py

Player Files:

Add cricket player files (.txt) inside the players directory. These files should contain relevant player performance data for strategy analysis.
Cricinfo API URL:

Enter the Cricinfo API URL in the sidebar to fetch live match commentary.
Features Walkthrough:
Player Selection: Choose a player file from the sidebar to analyze.
Live Commentary: View ball-by-ball commentary from an ongoing match (based on the Cricinfo API).
Get Strategy: Generate a detailed strategy to dismiss the selected player in T20 cricket.
Interactive Chat: Ask cricket-related questions and receive insights powered by the AI model.

