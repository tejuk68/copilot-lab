"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "A club for students who enjoy playing chess.",
        "participants": []
    },
    "Robotics Team": {
        "description": "Design and build robots to compete in local and national competitions.",
        "participants": []
    },
    "Drama Club": {
        "description": "Perform plays and skits throughout the school year.",
        "participants": []
    },
    # New sports-related activities
    "Basketball Team": {
        "description": "Practice and compete in basketball games and tournaments.",
        "participants": []
    },
    "Soccer Club": {
        "description": "Train for soccer matches and improve teamwork skills.",
        "participants": []
    },
    # New artistic activities
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts.",
        "participants": []
    },
    "Music Band": {
        "description": "Form a band to play instruments and perform music.",
        "participants": []
    },
    # New intellectual activities
    "Debate Club": {
        "description": "Engage in debates on various topics to build critical thinking.",
        "participants": []
    },
    "Science Club": {
        "description": "Conduct experiments and learn about scientific principles.",
        "participants": []
    }
}

@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]
    #validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
