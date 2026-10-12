import json
from collections import Counter
from pathlib import Path

from analyzer import analyze_code

CORPUS = Path(__file__).parent / "corpus"


def load():
    expected = json.loads((CORPUS / "expected.json").read_text())
    fps = expected.pop("known_false_positives")
    return expected, fps


def actual_findings():
    found = {}
    for path in sorted(CORPUS.glob("*.py")):
        result = analyze_code(path.read_text())
        found[path.name] = {(d.rule_id, d.line) for d in result.diagnostics}
    return found


def test_corpus_matches_expected_exactly():
    expected, _ = load()
    found = actual_findings()
    assert set(found) == set(expected)
    for name, items in expected.items():
        assert found[name] == {(i["rule"], i["line"]) for i in items}, name


def test_precision_recall_report(capsys):
    expected, fps = load()
    found = actual_findings()
    false_pos = {(f["file"], f["rule"], f["line"]) for f in fps}
    tp, fp, fn = Counter(), Counter(), Counter()
    for name, items in expected.items():
        want = {(i["rule"], i["line"]) for i in items}
        for rule, line in found[name]:
            if (name, rule, line) in false_pos:
                fp[rule] += 1
            elif (rule, line) in want:
                tp[rule] += 1
        for rule, _ in want - found[name]:
            fn[rule] += 1
    with capsys.disabled():
        print("\nrule    TP  FP  FN  precision  recall")
        for rule in sorted(set(tp) | set(fp) | set(fn)):
            p = tp[rule] / (tp[rule] + fp[rule]) if tp[rule] + fp[rule] else 1.0
            r = tp[rule] / (tp[rule] + fn[rule]) if tp[rule] + fn[rule] else 1.0
            print(f"{rule}  {tp[rule]:3d} {fp[rule]:3d} {fn[rule]:3d}  {p:9.2f}  {r:6.2f}")
    assert sum(fn.values()) == 0
