def calculate_score(syntax_status, issues):
    score = 100
    feedback = []
    
    if not syntax_status:
        score -= 10
        feedback.append("Syntax error detected")
    score -= 3*len(issues)
    if score < 0:
        score = 0
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
    return {
        "score": score,
        "grade": grade,
        "issues": issues,
        "syntax": syntax_status,
        "feedback": feedback
    }