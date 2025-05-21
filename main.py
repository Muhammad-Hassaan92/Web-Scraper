import streamlit as st
from scrape import scrape_website, split_dom_content, extract_body_content, clean_body_content
from parse import parse_with_gemini

st.title("AI Scraper App")
url = st.text_input("Enter a URL: ")

# Initialize session state
if "dom_content" not in st.session_state:
    st.session_state.dom_content = ""

# Scrape button
if st.button("Scrape Site") and url:
    with st.spinner("Scraping the site..."):
        try:
            result = scrape_website(url)
            body_content = extract_body_content(result)
            cleaned_content = clean_body_content(body_content)
            st.session_state.dom_content = cleaned_content
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)
        except Exception as e:
            st.error(f"Failed to scrape the website: {e}")

# Parse button
if st.session_state.dom_content:
    parse_description = st.text_area("Describe what you want to parse:", height=100)

    if st.button("Parse") and parse_description:
        with st.spinner("Parsing the content..."):
            try:
                dom_chunks = split_dom_content(st.session_state.dom_content)
                result = parse_with_gemini(dom_chunks, parse_description)
                st.write(result)
            except Exception as e:
                st.error(f"Parsing failed: {e}")
