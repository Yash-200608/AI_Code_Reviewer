# Points deducted for each diagnostic (other than a syntax error)
ISSUE_PENALTY = 3


# Function to calculate score and grade from an AnalysisResult
def calculate_score(result):
    feedback = []

    # Code that does not parse cannot be analyzed, so it gets no credit
    if not result.syntax_ok:
        score = 0
        feedback.append("Syntax error detected")
    else:
        score = 100 - ISSUE_PENALTY * len(result.issues)

    # Ensure score does not go below 0
    if score < 0:
        score = 0

    # Assign grade based on score
    if score >= 95:
        grade = "Outstanding"
    elif score >= 85:
        grade = "Excellent"
    elif score >= 75:
        grade = "Good"
    elif score >= 60:
        grade = "Average"
    else:
        grade = "Needs Improvement"

    # Return results as dictionary
    return {
        "score": score,
        "grade": grade,
        "issues": result.issues,
        "syntax": result.syntax_ok,
        "feedback": feedback,
    }
