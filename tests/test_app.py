from pathlib import Path

from streamlit.testing.v1 import AppTest

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def run(code):
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.text_area[0].set_value(code)
    at.button[0].click()
    return at.run()


def test_valid_code_renders_without_error():
    at = run("def add(first, second):\n    return first + second\n")
    assert not at.exception
    assert any("Analysis Result" in s.value for s in at.subheader)
    assert len(at.success) == 1


def test_invalid_code_shows_syntax_error():
    at = run("def broken(:\n    pass\n")
    assert not at.exception
    assert len(at.error) == 1
    assert "CR000" in at.error[0].value


def test_empty_input_warns():
    at = run("   ")
    assert not at.exception
    assert len(at.warning) == 1


def test_issues_listed_with_rule_ids():
    at = run("def f():\n    return 1\n    q = 2\n")
    assert not at.exception
    text = " ".join(m.value for m in at.markdown)
    assert "CR105" in text and "CR102" in text
