import pickle
import google.generativeai as genai
import streamlit as st
import os
from time import sleep

GOOGLE_API_KEY='AIzaSyB4UJ9nA4c3mhFXmfx-45XZil-67OHLBo4'
genai.configure(api_key=GOOGLE_API_KEY)    
# model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel('gemini-1.5-pro-latest')

colLeft, colRight = st.columns([1,1])
# Check if the pickle file exists
chatHistoryFile = 'chat_history.pkl'

if os.path.isfile(chatHistoryFile):
    # Load the chat history from the pickle file
    with open(chatHistoryFile, 'rb') as f:
        chatHistory = pickle.load(f)
else:
    # Initialize an empty chat history
    chatHistory = []

# Create a sidebar
sidebar = st.sidebar
sidebar.markdown("* Use '/c' to clear the chat history.")
sidebar.markdown("* Use '/r [file name]' to summarize a code file.")
# Define the current working directory
cwd = os.getcwd()

#! read code from "./pages/code.py"
def readCode(fileName):    
    code_file_path = os.path.join(cwd, "pages", fileName)

    # Check if the code.py file exists
    if os.path.isfile(code_file_path):

        # Read the contents of the code.py file
        with open(code_file_path, 'r') as f:
            code_contents = f.read()

        # Generate a summary of the code.py file using the AI model
        with st.spinner('🚀🚀🚀Working at max speed...'):
            summary = model.generate_content({'parts': [f'Summarize this code for me: {code_contents}']})

        # Add the summary to the chat history
        userRequest = {'role':'user','parts': [f'Summary the file {code_file_path} for me']}
        aiResponse = {'role': 'model', 'parts': [summary.text]}
        chatHistory.append(userRequest)
        chatHistory.append(aiResponse)
    else:

        # Display an error message
        st.error(f"The file {fileName} does not exist.")
# readCode()



userInput=st.chat_input("Please ask me a question, boss...")

with colLeft:
    if userInput:
        if userInput == "/c":
            # Clear the chat history
            chatHistory = []
        elif userInput.startswith("/r"):
            file_name = userInput[3:]
            readCode(file_name)
        else:
            userRequest = {'role':'user','parts': [userInput]}
            chatHistory.append(userRequest)
            try:
                if chatHistory:
                    with st.spinner('🚀🚀🚀Working at max speed...'):
                        response = model.generate_content(chatHistory)
                    aiResponse={'role':'model','parts':[response.text]}
                    chatHistory.append(aiResponse)
            except:
                pass


with colRight:
    with st.expander("🧠🧠🧠Chat History"):

        if chatHistory:
            for index, message in enumerate(reversed(chatHistory)):
                messageToDisplay=message['parts'][0]
                role=message['role']
                if role=='user':
                    st.success('😎Boss:')
                    st.write(f'{messageToDisplay}')
                else:
                    st.warning('🪶Premium assitant:')
                    st.write(f'{messageToDisplay}')
                        

with colLeft:
    with st.expander("👉👉👉Latest History",expanded=True):
        if chatHistory:
            for index, message in enumerate(chatHistory[-2:]):
                messageToDisplay=message['parts'][0]
                role=message['role']
                if role=='user':
                    st.success('😎Boss:')
                    st.write(f'{messageToDisplay}')
                else:
                    st.warning('🪶Premium assitant:')
                    st.write(f'{messageToDisplay}')
                        
# Save the chat history to the pickle file
with open(chatHistoryFile, 'wb') as f:
    pickle.dump(chatHistory, f)