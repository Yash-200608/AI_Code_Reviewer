import ast
import io
import tokenize
from dataclasses import dataclass, field

# Thresholds used by the rules below
MAX_FUNCTION_LINES = 50
MAX_COMPLEXITY = 10
MIN_LINES_FOR_COMMENTS = 10

# Single-character names that are conventional in specific contexts
LOOP_NAMES = {"i", "j", "k", "n", "x", "y"}
EXCEPTION_NAMES = {"e"}


# One finding reported by a rule, with a stable rule ID and source location
@dataclass(frozen=True)
class Diagnostic:
    rule_id: str
    name: str
    message: str
    line: int
    col: int = 0


# Result of analyzing a piece of code. Always returned by analyze_code(),
# for valid, invalid and empty input alike.
@dataclass
class AnalysisResult:
    syntax_ok: bool
    diagnostics: list = field(default_factory=list)

    # The CR000 diagnostic if the code failed to parse, otherwise None
    @property
    def syntax_error(self):
        for diagnostic in self.diagnostics:
            if diagnostic.rule_id == "CR000":
                return diagnostic
        return None

    # All diagnostics except the syntax error
    @property
    def issues(self):
        return [d for d in self.diagnostics if d.rule_id != "CR000"]


# Function to check if the given Python code has valid syntax
def check_syntax(code):
    try:
        ast.parse(code)
        return True
    except SyntaxError:
        return False


FUNCTION_NODES = (ast.FunctionDef, ast.AsyncFunctionDef)


# CR101: flag individual functions longer than MAX_FUNCTION_LINES
def check_long_functions(tree, code):
    diagnostics = []
    for node in ast.walk(tree):
        if isinstance(node, FUNCTION_NODES):
            length = node.end_lineno - node.lineno + 1
            if length > MAX_FUNCTION_LINES:
                diagnostics.append(Diagnostic(
                    "CR101", "long-function",
                    f"Function '{node.name}' is {length} lines long (max {MAX_FUNCTION_LINES})",
                    node.lineno, node.col_offset,
                ))
    return diagnostics


# Collect the Name nodes bound as for-loop or comprehension targets
def _loop_target_names(tree):
    targets = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.AsyncFor, ast.comprehension)):
            for name in ast.walk(node.target):
                if isinstance(name, ast.Name):
                    targets.add(id(name))
    return targets


# CR102: flag single-character identifiers where they are bound
# (assignments, arguments, def/class names), skipping conventional uses
def check_short_names(tree, code):
    loop_targets = _loop_target_names(tree)
    lambda_args = {
        id(arg) for node in ast.walk(tree) if isinstance(node, ast.Lambda)
        for arg in ast.walk(node.args) if isinstance(arg, ast.arg)
    }
    bindings = []  # (name, line, col)

    for node in ast.walk(tree):
        if isinstance(node, FUNCTION_NODES + (ast.ClassDef,)):
            bindings.append((node.name, node.lineno, node.col_offset))
        elif isinstance(node, ast.arg) and id(node) not in lambda_args:
            bindings.append((node.arg, node.lineno, node.col_offset))
        elif isinstance(node, ast.ExceptHandler) and node.name:
            if node.name not in EXCEPTION_NAMES:
                bindings.append((node.name, node.lineno, node.col_offset))
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            if id(node) in loop_targets and node.id in LOOP_NAMES:
                continue
            bindings.append((node.id, node.lineno, node.col_offset))

    # Report each short name once, at its first binding site
    diagnostics = []
    seen = set()
    for name, line, col in sorted(bindings, key=lambda b: (b[1], b[2])):
        if len(name) == 1 and name != "_" and name not in seen:
            seen.add(name)
            diagnostics.append(Diagnostic(
                "CR102", "short-name", f"Single-character name '{name}'", line, col,
            ))
    return diagnostics


# True if the module, or any class/function in it, has a docstring
def _has_docstring(tree):
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef) + FUNCTION_NODES):
            if ast.get_docstring(node):
                return True
    return False


# CR103: flag longer code that has neither comments nor docstrings.
# Uses the tokenizer so a '#' inside a string literal does not count.
def check_comments(tree, code):
    non_blank = [line for line in code.splitlines() if line.strip()]
    if len(non_blank) < MIN_LINES_FOR_COMMENTS:
        return []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(code).readline)
        if any(token.type == tokenize.COMMENT for token in tokens):
            return []
    except (tokenize.TokenError, SyntaxError):
        return []
    if _has_docstring(tree):
        return []
    return [Diagnostic("CR103", "no-comments", "No comments or docstrings in code", 1)]


# Count decision points inside a function, without descending into nested defs
def _complexity(function):
    complexity = 1
    stack = list(ast.iter_child_nodes(function))
    while stack:
        node = stack.pop()
        if isinstance(node, FUNCTION_NODES + (ast.ClassDef,)):
            continue
        if isinstance(node, (ast.If, ast.For, ast.AsyncFor, ast.While,
                             ast.IfExp, ast.ExceptHandler, ast.match_case)):
            complexity += 1
        elif isinstance(node, ast.comprehension):
            complexity += len(node.ifs)
        elif isinstance(node, ast.BoolOp):
            complexity += len(node.values) - 1
        stack.extend(ast.iter_child_nodes(node))
    return complexity


# CR104: flag functions whose cyclomatic complexity exceeds MAX_COMPLEXITY
def check_complexity(tree, code):
    diagnostics = []
    for node in ast.walk(tree):
        if isinstance(node, FUNCTION_NODES):
            complexity = _complexity(node)
            if complexity > MAX_COMPLEXITY:
                diagnostics.append(Diagnostic(
                    "CR104", "high-complexity",
                    f"Function '{node.name}' has cyclomatic complexity {complexity} (max {MAX_COMPLEXITY})",
                    node.lineno, node.col_offset,
                ))
    return diagnostics


TERMINATORS = {ast.Return: "return", ast.Raise: "raise", ast.Break: "break", ast.Continue: "continue"}


# CR105: flag the first statement after return/raise/break/continue in a block
def check_unreachable(tree, code):
    diagnostics = []
    for node in ast.walk(tree):
        for field_name in ("body", "orelse", "finalbody"):
            block = getattr(node, field_name, None)
            if not isinstance(block, list):
                continue
            for current, following in zip(block, block[1:]):
                keyword = TERMINATORS.get(type(current))
                if keyword:
                    diagnostics.append(Diagnostic(
                        "CR105", "unreachable-code",
                        f"Unreachable code after '{keyword}'",
                        following.lineno, following.col_offset,
                    ))
                    break
    return diagnostics


# Rules run on every syntactically valid input, in this order
RULES = [
    check_long_functions,
    check_short_names,
    check_comments,
    check_complexity,
    check_unreachable,
]


# Main function to analyze code and collect diagnostics
def analyze_code(code):
    if not code.strip():
        return AnalysisResult(syntax_ok=True)

    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        error = Diagnostic("CR000", "syntax-error", f"Syntax error: {e.msg}",
                           e.lineno or 1, e.offset or 0)
        return AnalysisResult(syntax_ok=False, diagnostics=[error])

    diagnostics = []
    for rule in RULES:
        diagnostics.extend(rule(tree, code))
    diagnostics.sort(key=lambda d: (d.line, d.rule_id))
    return AnalysisResult(syntax_ok=True, diagnostics=diagnostics)
