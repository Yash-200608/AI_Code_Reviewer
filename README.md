# 🤖 AI Code Reviewer (Python + AST)

A lightweight AI-inspired Code Reviewer built using **Python** and **Streamlit** that analyzes Python code for syntax errors, structural issues, and basic code quality metrics.

This project demonstrates **static code analysis using Python’s AST module** and a rule-based scoring system.

---

## 🚀 Features

Every finding has a stable rule ID and a source line number.

| ID | Rule | What it checks |
|---|---|---|
| CR000 | syntax-error | Code fails to parse (reports line and message) |
| CR101 | long-function | A single function longer than 50 lines |
| CR102 | short-name | Single-character names where they are bound (exempts `_`, loop vars `i j k n x y`, `except ... as e`, lambda args) |
| CR103 | no-comments | 10+ lines of code with no comments or docstrings (uses the tokenizer, so `#` in strings is ignored) |
| CR104 | high-complexity | Function cyclomatic complexity above 10 |
| CR105 | unreachable-code | Statement after `return` / `raise` / `break` / `continue` |

CR102 reports each short name **once, at its first binding**, not at every binding site.

* 📊 Dynamic scoring system and 🏆 grade classification
* 🌐 Web interface built with Streamlit
* 🧠 Modular structure (analyzer + scorer separation)

---

## 🧠 How It Works

1. User pastes Python code into the web interface.
2. The `analyzer.py` module:

   * Parses code into an Abstract Syntax Tree (AST)
   * Detects syntax issues
   * Applies rule-based checks
3. The `scorer.py` module:

   * Calculates quality score
   * Assigns grade
   * Generates feedback
4. Results are displayed via Streamlit UI.

---

## 🛠 Tech Stack

* Python 3.10+
* Streamlit
* AST (Abstract Syntax Tree module)
* pytest (tests)

---

## 📂 Project Structure

```
AI_Code_Reviewer/
├── app.py
├── analyzer.py
├── scorer.py
├── requirements.txt
├── requirements-dev.txt
├── tests/
│   ├── corpus/          # labeled snippets + expected.json
│   └── test_*.py
└── .github/workflows/ci.yml
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Yash-200608/AI_Code_Reviewer
cd AI_Code_Reviewer
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

Then open:

```
http://localhost:8501
```

---

## 🧪 Running Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```

`tests/corpus/expected.json` records the expected rule/line for each corpus snippet,
plus known false positives; `python -m pytest -s tests/test_corpus.py` prints per-rule precision/recall.

### Corpus results

Measured on `tests/corpus` (8 snippets; small, so treat as a regression guard, not a benchmark):

| Rule | TP | FP | FN | Precision | Recall |
|---|---|---|---|---|---|
| CR000 | 1 | 0 | 0 | 1.00 | 1.00 |
| CR102 | 1 | 1 | 0 | 0.50 | 1.00 |
| CR104 | 1 | 0 | 0 | 1.00 | 1.00 |
| CR105 | 1 | 0 | 0 | 1.00 | 1.00 |

The one recorded false positive is `w` in `short_names.py` (a plausible width abbreviation, flagged by design).
CR101 and CR103 have unit tests but no positive corpus snippet yet.

---

## 📊 Scoring Logic

* Base Score: 100
* Syntax Error: score 0 (code that does not parse is not analyzed further)
* Each detected issue: −3
* Grades:

  * 95+ → Outstanding
  * 85+ → Excellent
  * 75+ → Good
  * 60+ → Average
  * Below 60 → Needs Improvement

---

## 🎯 Learning Outcomes

* Understanding Python AST
* Static code analysis fundamentals
* Rule-based evaluation systems
* Web app development using Streamlit
* Debugging and modular project design
* Virtual environment management

---

## 🔮 Future Improvements

* Recursion detection
* Duplicate-code detection
* GitHub repository analyzer
* Machine Learning-based code scoring
* Advanced UI styling

---

## 👨‍💻 Author

Developed by __**Yash**__ as a B.Tech CSE (AIML) project to explore static code analysis and AI-inspired evaluation systems.
