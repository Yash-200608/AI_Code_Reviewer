# Function to calculate score and grade based on syntax and issues
def calculate_score(syntax_status, issues):
    score = 100
    feedback = []
    
    # Deduct marks if syntax error exists
    if not syntax_status:
        score -= 10
        feedback.append("Syntax error detected")

    # Deduct 3 marks for each issue found
    score -= 3*len(issues)

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
        grade ="Needs Improvement"

    # Return results as dictionary
    return {
        "score": score,
        "grade": grade,
        "issues": issues,
        "syntax": syntax_status,
        "feedback": feedback
    }
