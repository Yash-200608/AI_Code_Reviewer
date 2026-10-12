from analyzer import AnalysisResult, analyze_code, check_syntax


def rules(code):
    return [(d.rule_id, d.line) for d in analyze_code(code).diagnostics]


def test_valid_code_shape():
    result = analyze_code("value = 1\n")
    assert isinstance(result, AnalysisResult)
    assert result.syntax_ok is True
    assert result.syntax_error is None
    assert result.diagnostics == []


def test_invalid_code_shape():
    result = analyze_code("def broken(:\n    pass\n")
    assert isinstance(result, AnalysisResult)
    assert result.syntax_ok is False
    assert result.syntax_error.rule_id == "CR000"
    assert result.syntax_error.line == 1
    assert result.issues == []


def test_empty_input():
    for code in ("", "   \n\n"):
        result = analyze_code(code)
        assert result.syntax_ok is True
        assert result.diagnostics == []


def test_check_syntax():
    assert check_syntax("x = 1") is True
    assert check_syntax("x = ") is False


# CR101
def test_long_function_flagged_per_function():
    body = "\n".join(f"    v{n} = {n}" for n in range(60))
    code = f"def big():\n{body}\n\ndef small():\n    return 1\n"
    assert ("CR101", 1) in rules(code)
    assert not any(r == "CR101" and line == 64 for r, line in rules(code))


def test_many_short_functions_not_flagged():
    code = "\n".join(f"def f{n}():\n    return {n}\n" for n in range(40))
    assert all(r != "CR101" for r, _ in rules(code))


# CR102
def test_short_name_assignment_and_argument():
    code = "def area(w, height):\n    q = w * height\n    return q\n"
    assert rules(code) == [("CR102", 1), ("CR102", 2)]


def test_short_name_exemptions():
    code = (
        "for i in range(3):\n    print(i)\n"
        "try:\n    pass\nexcept ValueError as e:\n    print(e)\n"
        "_ = 1\n"
        "total = [x for x in range(3)]\n"
        "pair = lambda a: a\n"
    )
    assert all(r != "CR102" for r, _ in rules(code))


def test_short_name_not_flagged_in_strings_or_comments():
    code = 'label = "a b c"  # x y z\n'
    assert rules(code) == []


# CR103
def test_no_comments_flagged_for_long_code():
    code = "\n".join(f"value{n} = {n}" for n in range(12)) + "\n"
    assert rules(code) == [("CR103", 1)]


def test_comment_in_string_does_not_count():
    code = "\n".join(f"value{n} = '#'" for n in range(12)) + "\n"
    assert ("CR103", 1) in rules(code)


def test_comment_or_docstring_satisfies_rule():
    body = "\n".join(f"value{n} = {n}" for n in range(12)) + "\n"
    assert rules("# note\n" + body) == []
    assert rules('"""Module doc."""\n' + body) == []


def test_short_code_needs_no_comments():
    assert rules("value = 1\n") == []


# CR104
def test_high_complexity():
    branches = "\n".join(f"    if v == {n}:\n        return {n}" for n in range(11))
    code = f"def pick(v):\n{branches}\n    return -1\n"
    assert ("CR104", 1) in rules(code)


def test_low_complexity_not_flagged():
    code = "def pick(v):\n    if v:\n        return 1\n    return 0\n"
    assert all(r != "CR104" for r, _ in rules(code))


# CR105
def test_unreachable_after_return():
    code = "def func():\n    return 1\n    print('never')\n"
    assert rules(code) == [("CR105", 3)]


def test_reachable_code_not_flagged():
    code = "def func(value):\n    if value:\n        return 1\n    return 0\n"
    assert rules(code) == []
