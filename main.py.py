import streamlit as st
from scrape import (
    scrape_web,
    split_doc_content,
    clean_body_content,
    extract_body_content,
)
from parse import parse_with_ollama


st.title("AI web Scrapper")
url = st.text_input("Enter a Website URL: ")

if st.button("Scrape Site"):
    st.write("Scraping the Website")
    result = scrape_web(url)
    body_content = extract_body_content(result)
    cleaned_content = clean_body_content(body_content)

    st.session_state.dom_content = cleaned_content

    with st.expander("View DOM content"):
        st.text_area("DOM Content", cleaned_content, height=3)

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse?")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content")

            dom_chunks = split_doc_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            st.write(result)
