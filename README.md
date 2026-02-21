# 🤖 AI Code Reviewer (Python + AST)

A lightweight AI-inspired Code Reviewer built using **Python** and **Streamlit** that analyzes Python code for syntax errors, structural issues, and basic code quality metrics.

This project demonstrates **static code analysis using Python’s AST module** and a rule-based scoring system.

---

## 🚀 Features

* ✅ Syntax error detection using `ast.parse()`
* 📏 Code length analysis
* 📝 Comment presence detection
* 🔤 Variable naming analysis
* 📊 Dynamic scoring system
* 🏆 Grade classification (Outstanding, Excellent, Good, etc.)
* 🌐 Web interface built with Streamlit
* 🧠 Modular project structure (analyzer + scorer separation)

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

* Python 3.x
* Streamlit
* AST (Abstract Syntax Tree module)
* Regular Expressions (`re`)

---

## 📂 Project Structure

```
AI_Code_Reviewer/
│
├── app.py
├── analyzer.py
├── scorer.py
├── requirements.txt
└── venv/
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone <your-repo-link>
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

## 📊 Scoring Logic

* Base Score: 100
* Syntax Error: −10
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

* AST-based complexity analysis
* Cyclomatic complexity calculation
* Recursion detection
* GitHub repository analyzer
* Machine Learning-based code scoring
* Advanced UI styling

---

## 👨‍💻 Author

Developed by __**Yash**__ as a B.Tech CSE (AIML) project to explore static code analysis and AI-inspired evaluation systems.
