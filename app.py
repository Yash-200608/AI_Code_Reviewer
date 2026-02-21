import streamlit as st 
from analyzer import analyze_code
from scorer import calculate_score


st.set_page_config(page_title="AI Code Reviewer", layout="centered")

st.title("AI Code Reviewer")
st.write("Paste your python code below to analyze it.")

code = st.text_area("Enter Python Code", height=300)

if st.button("Analyze Code"):
    if code.strip() == "":
        st.warning("Please enter some code.")
    else:
        syntax_status, issues = analyze_code(code)
        result = calculate_score(syntax_status, issues)
        st.subheader("Analysis Result")
        st.write("Syntax Status: ", result["syntax"])
        st.write("Score: ", result["score"])
        st.write("Grade: ", result["grade"])

        if result["issues"]:
            st.subheader("Issues Found")
            for issue in result["issues"]:
                st.write("-", issue)
        else:
            st.success("No issues found. Great Job! ")