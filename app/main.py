from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import rooms, autocomplete, ws_router, execute, admin
from app.db import init_db
from app.logger import logger
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse

'''
Main application setup and configuration.
'''

title="Pair Programming Prototype"
description="A simple backend for a real-time collaborative code editor with execution capabilities."

tags_metadata = [
    {
        "name": "users endpoints",
        "description": "Operations with users. create room , get room code etc.",
    },
    {
        "name": "admin endpoints",
        "description": "Operations for admin like viewing all rooms.",

    },
]
app = FastAPI(
    title=title,
    description=description,
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.middleware("http")
async def log_requests(request: Request, call_next):
    '''
    Middleware to log incoming HTTP requests and their responses.
    '''

    logger.info(f"HTTP {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"HTTP {request.method} {request.url.path} -> {response.status_code}")
    return response


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    '''
    Global exception handler to catch unhandled exceptions and log them.
    '''

    logger.error(f"Unhandled error at {request.url.path}: {exc}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


init_db()


app.include_router(rooms.router)
app.include_router(autocomplete.router)
app.include_router(ws_router.router)
app.include_router(execute.router) 
app.include_router(admin.router)  

