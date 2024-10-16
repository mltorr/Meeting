import openai
import os
from dotenv import load_dotenv
from docx import Document
import streamlit as st

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_transcript(transcript_text, prompt):
    # Prepare the messages for the chat completion
    messages = [
        {"role": "user", "content": prompt + "\n\n" + transcript_text}
    ]
    
    # Use the chat completion endpoint
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # Specify the correct model
        messages=messages,
    )
    
    # Extract and return the response text
    return response.choices[0].message['content']

# def main():


# if __name__ == "__main__":
#     main()



# Go to the Azure Portal and navigate to "Azure Active Directory. https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps/ApplicationsListBlade"
# Under "Manage," select "App registrations" and then click "New registration."
# Fill in the necessary details:
# Name: Your app name
# Supported account types: Accounts in any organizational directory and personal Microsoft accounts
# Redirect URI: Set the redirect URI to https://apps.btgi.com.au:port or http://localhost:port if you're testing locally
# Once registered, note the Application (client) ID and Directory (tenant) ID.
# Under "Certificates & secrets," create a new client secret and note it down.

from login import *

# Main page (after login)
def main_page():
    st.title("Meeting Transcript Summarizer")

    uploaded_file = st.file_uploader("Upload a Transcript (Text/Word Document)", type=["txt", "docx"])
    
    if uploaded_file is not None:
        # Read the uploaded file
        if uploaded_file.type == "text/plain":
            transcript_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            doc = Document(uploaded_file)
            transcript_text = "\n".join([para.text for para in doc.paragraphs])

        # Custom prompt
        prompt = """
        You are an AI assistant tasked with summarizing meeting transcripts. Below is the transcript of a recent meeting. Your summary should include the following sections:

        1. **Meeting Summary**: A brief overview of the meeting's key topics and discussions.
        2. **Next Steps**: A list of actionable items mentioned during the meeting, with timestamps for each item.
        3. **AI Insights**: A summary of the engagement level, clarity of next steps, time management, and overall sentiment expressed by participants.
        4. **Topics & Highlights**: A detailed breakdown of main topics discussed, including specific comments made during the meeting, with timestamps for each key point.

        The meeting transcript is as follows:
        """

        if st.button("Generate Summary"):
            summary = process_transcript(transcript_text, prompt)
            # st.subheader("Meeting Summary:")
            st.write(summary)
    logout()

# Main function to handle the app flow
def main():
    set_page_config()
    custom_css()

    # Check if user is logged in via query params (code) or session state
    if 'code' in st.query_params or 'access_token' in st.session_state:
        if 'code' in st.query_params and 'access_token' not in st.session_state:
            auth_code = st.query_params['code']
            if isinstance(auth_code, list):
                auth_code = auth_code[0]

            token = get_token_from_code(auth_code)
            if 'access_token' in token:
                st.session_state['access_token'] = token['access_token']
                user_profile = get_user_profile(token)

                st.session_state['user_profile'] = user_profile  # Store profile in session state
                st.success(f"Logged in as {user_profile['displayName']}")

                # #Get values from user profile
                # given_name = user_profile.get('givenName', 'there')  # Use 'there' as default if 'givenName' is missing
                # st.title(f"Hi {given_name}! Welcome!")
                # st.write(user_profile)

        # Check if user profile exists in session state
        if 'user_profile' in st.session_state:
            main_page()
    else:
        login_page()

if __name__ == "__main__":
    main()