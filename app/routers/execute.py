from fastapi import APIRouter
from pydantic import BaseModel
import io
import contextlib

router = APIRouter()

class ExecuteRequest(BaseModel):
    code: str

@router.post("/execute",tags=["users endpoints"],summary="Execute code and return output")
def execute_code(req: ExecuteRequest):
    """
    WARNING: usage of exec() is unsafe for production. 
    This is a simplified example and should be used with caution.
    In a real-world scenario, consider using a sandboxed environment.
    """

    code = req.code
    
    # Create a buffer to capture stdout
    buffer = io.StringIO()
    
    try:
        # Redirect stdout to our buffer
        with contextlib.redirect_stdout(buffer):
            # Create a localized dictionary for variables (so they don't pollute global scope)
            local_scope = {}
            exec(code, {}, local_scope)
        
        output = buffer.getvalue()
        
    except Exception as e:
        # Capture standard runtime errors
        output = f"Error: {str(e)}"
    
    return {"output": output}