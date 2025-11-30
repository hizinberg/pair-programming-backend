from pydantic import BaseModel

'''
Pydantic schemas for request and response models.
'''

class CreateRoomResp(BaseModel):
    roomId: str

class AutoRequest(BaseModel):
    code: str
    cursorPosition: int
    language: str = "python"

class AutocompleteResp(BaseModel):
    suggestions: list[str]

