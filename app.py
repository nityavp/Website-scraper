import streamlit as st
import requests
import pandas as pd

# Function to analyze a URL with Diffbot
def analyze_with_diffbot(url, diffbot_token):
    api_url = f"https://api.diffbot.com/v3/analyze?url={url}&token={diffbot_token}"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Diffbot Error: {response.status_code}")
        return None

# Helper function to flatten JSON
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

# Streamlit app
st.title("URL Content Analyzer with Diffbot")

# User inputs
url = st.text_input("Enter the URL to analyze")
diffbot_token = st.text_input("Enter your Diffbot token", type="password")

if st.button("Analyze URL"):
    if url and diffbot_token:
        # Analyze URL with Diffbot
        result = analyze_with_diffbot(url, diffbot_token)
        if result:
            # Flatten JSON data to make it table-friendly
            flat_data = flatten_json(result)
            df = pd.DataFrame([flat_data])
            
            # Display results in a table
            st.write("Analysis Results:")
            st.table(df)
    else:
        st.error("Please provide both the URL and Diffbot token.")
