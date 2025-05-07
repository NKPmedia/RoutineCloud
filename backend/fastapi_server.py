"""
fastapi_server.py

This module provides a FastAPI server with REST endpoints to control the bedtime routine.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

from routine_state import routine_state

# Create FastAPI app
app = FastAPI(title="Bedtime Routine API", 
              description="API for controlling a child's bedtime routine on Raspberry Pi")

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Response models
class Task(BaseModel):
    id: int
    name: str
    sound: str
    duration: int

class RoutineStatus(BaseModel):
    is_active: bool
    current_task: Optional[Task] = None
    current_sound: Optional[str] = None

# API endpoints
@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the Bedtime Routine API"}

@app.get("/tasks", response_model=List[Task])
async def get_tasks():
    """Get all tasks in the routine."""
    return routine_state.tasks

@app.get("/status", response_model=RoutineStatus)
async def get_status():
    """Get the current status of the routine."""
    current_task = routine_state.current_task
    
    return {
        "is_active": routine_state.is_routine_active,
        "current_task": current_task,
        "current_sound": routine_state.current_sound
    }

@app.post("/routine/start", response_model=Task)
async def start_routine():
    """Start the routine from the beginning."""
    try:
        task = routine_state.start_routine()
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/routine/next", response_model=Optional[Task])
async def next_task():
    """Move to the next task in the routine."""
    if not routine_state.is_routine_active:
        raise HTTPException(status_code=400, detail="No active routine")
    
    task = routine_state.next_task()
    if task is None:
        return None  # Routine is complete
    return task

@app.post("/routine/stop")
async def stop_routine():
    """Stop the current routine."""
    routine_state.stop_routine()
    return {"message": "Routine stopped"}

@app.post("/sound/play/{sound_name}")
async def play_sound(sound_name: str):
    """Play a specific sound."""
    success = routine_state.play_sound(sound_name)
    if not success:
        raise HTTPException(status_code=400, detail=f"Could not play sound: {sound_name}")
    return {"message": f"Playing sound: {sound_name}"}

# Function to start the server
def start_server(host: str = "0.0.0.0", port: int = 8000):
    """Start the FastAPI server."""
    import uvicorn
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()