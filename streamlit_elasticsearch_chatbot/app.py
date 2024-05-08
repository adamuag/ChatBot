import textwrap

import streamlit as st
import ES_helper as esh
import AI_helper as aih

esh.generate_indexes()
cohort_list = esh.get_cohort()
st.title("Zoomcamp Q&A ChatBot")

with st.sidebar as sb:
    with st.form(key='query-form'):
        course_cohort = st.selectbox(label="Course Cohort : ", options=cohort_list)
        query = st.text_area(label="",
                             placeholder="-- Type your question here! --",
                             max_chars=100)
        submit = st.form_submit_button(label="Submit")

if query and course_cohort and query != "-- question --" and query.strip() != "":
    answer = aih.qa_bot(query, course_cohort)
    st.subheader("Answer:")
    st.text(textwrap.fill(answer, width=80))
