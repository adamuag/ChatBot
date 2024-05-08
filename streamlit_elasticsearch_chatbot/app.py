import textwrap

import streamlit as st
import ES_helper as esh
import AI_helper as aih


esh.generate_indexes()

st.title("Zoomcamp Q&A ChatBot")

with st.sidebar as sb:
    with st.form(key='query-form'):
        query = st.sidebar.text_area(label="Type  your question here and click submit when you are done.",
                                           max_chars=100)
        submit = st.form_submit_button(label="Submit")

if query:
    answer = aih.qa_bot(query)
    st.subheader("Answer:")
    st.text(textwrap.fill(answer, width=80))
