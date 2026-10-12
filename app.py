import streamlit as st
from analyzer import analyze_code
from scorer import calculate_score

# Configure Streamlit page settings
st.set_page_config(page_title="AI Code Reviewer", layout="centered")

# App title and description
st.title("AI Code Reviewer")
st.write("Paste your python code below to analyze it.")

# Text area for user to paste Python code
code = st.text_area("Enter Python Code", height=300)

# Button to trigger code analysis
if st.button("Analyze Code"):
    # Check if input is empty
    if code.strip() == "":
        st.warning("Please enter some code.")
    else:
        # Analyze the code using analyzer module
        analysis = analyze_code(code)
        # Calculate score and grade
        result = calculate_score(analysis)
        # Display results
        st.subheader("Analysis Result")
        st.write("Syntax Status: ", "Valid" if result["syntax"] else "Invalid")
        st.write("Score: ", result["score"])
        st.write("Grade: ", result["grade"])

        # Show where parsing failed
        error = analysis.syntax_error
        if error:
            st.error(f"`{error.rule_id}` line {error.line}: {error.message}")

        # Display issues if found
        if result["issues"]:
            st.subheader("Issues Found")
            for issue in result["issues"]:
                st.markdown(f"- `{issue.rule_id}` line {issue.line}: {issue.message}")
        elif result["syntax"]:
            st.success("No issues found. Great Job! ")
