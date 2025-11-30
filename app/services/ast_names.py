import ast

'''
Module to extract names from Python code using AST.
'''

class NameCollector(ast.NodeVisitor):
    def __init__(self):
        self.globals = set()
        self.functions = set()
        self.classes = set()
        self.imports = set()
        self.params = set()
        self.locals = set()

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.imports.add(alias.asname or alias.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self.functions.add(node.name)
        for arg in node.args.args:
            self.params.add(arg.arg)
        if node.args.vararg:
            self.params.add(node.args.vararg.arg)
        if node.args.kwarg:
            self.params.add(node.args.kwarg.arg)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.classes.add(node.name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for t in node.targets:
            if isinstance(t, ast.Name):
                self.locals.add(t.id)
        self.generic_visit(node)

    def visit_For(self, node):
        if isinstance(node.target, ast.Name):
            self.locals.add(node.target.id)
        self.generic_visit(node)

    def visit_With(self, node):
        for item in node.items:
            if isinstance(item.optional_vars, ast.Name):
                self.locals.add(item.optional_vars.id)
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        if node.name:
            self.locals.add(node.name)
        self.generic_visit(node)


def extract_names(code: str):
    try:
        tree = ast.parse(code)
    except Exception:
        return {
            "globals": [],
            "functions": [],
            "classes": [],
            "imports": [],
            "params": [],
            "locals": [],
        }

    collector = NameCollector()
    collector.visit(tree)

    return {
        "globals": sorted(collector.globals),
        "functions": sorted(collector.functions),
        "classes": sorted(collector.classes),
        "imports": sorted(collector.imports),
        "params": sorted(collector.params),
        "locals": sorted(collector.locals),
    }
