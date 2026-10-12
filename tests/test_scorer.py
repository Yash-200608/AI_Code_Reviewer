from analyzer import AnalysisResult, Diagnostic, analyze_code
from scorer import calculate_score


def make(count, syntax_ok=True):
    issues = [Diagnostic("CR102", "short-name", "m", n + 1) for n in range(count)]
    return AnalysisResult(syntax_ok=syntax_ok, diagnostics=issues)


def test_clean_code_is_outstanding():
    report = calculate_score(analyze_code("value = 1\n"))
    assert report["score"] == 100
    assert report["grade"] == "Outstanding"
    assert report["syntax"] is True


def test_syntax_error_scores_zero():
    report = calculate_score(analyze_code("def broken(:\n"))
    assert report["score"] == 0
    assert report["grade"] == "Needs Improvement"
    assert report["syntax"] is False
    assert "Syntax error detected" in report["feedback"]


def test_penalty_and_grade_bands():
    assert calculate_score(make(1))["score"] == 97
    assert calculate_score(make(2))["grade"] == "Excellent"  # 94
    assert calculate_score(make(5))["grade"] == "Excellent"  # 85
    assert calculate_score(make(6))["grade"] == "Good"  # 82
    assert calculate_score(make(8))["grade"] == "Good"  # 76
    assert calculate_score(make(9))["grade"] == "Average"  # 73
    assert calculate_score(make(14))["grade"] == "Needs Improvement"  # 58
    assert calculate_score(make(40))["score"] == 0
