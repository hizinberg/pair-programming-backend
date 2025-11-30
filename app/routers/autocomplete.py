from fastapi import APIRouter
from app.schemas import AutoRequest
from typing import Dict, List
from ..services.ast_names import extract_names

router = APIRouter()

@router.post("/autocomplete",tags=["users endpoints"],summary="Get code autocomplete suggestions")
def autocomplete(req: AutoRequest) -> Dict[str, List[str]]:
    '''
    Provide code autocomplete suggestions based on the current code context.
    '''

    code = req.code or ""
    cursor = req.cursorPosition or len(code)

    prefix = code[:cursor]
    current_line = prefix.split("\n")[-1]
    words = current_line.split()
    last_word = words[-1] if words else ""

    # Get AST names (dict)
    ast_names = extract_names(code)

    suggestions = []

    # --- Context-based matching ---
    if last_word.startswith("imp"):
        suggestions = [
            f"import {mod}" for mod in ast_names["imports"]
        ] + ["import os", "import sys", "import json"]

    elif last_word.startswith("def"):
        suggestions = [
            "def function_name():",
            "def __init__(self):",
            "def main():",
        ]

    else:
        dynamic = (
            ast_names["locals"]
            + ast_names["params"]
            + ast_names["functions"]
            + ast_names["classes"]
            + ast_names["imports"]
        )

        # prefix filtering
        suggestions = [n for n in dynamic if n.startswith(last_word)]

        suggestions += [
            "print",
            "return",
            "class",
            "def",
            "if __name__ == '__main__':"
        ]

    return {"suggestions": suggestions}
