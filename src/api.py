from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from socketHandler import robots

app = FastAPI()

# add cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/v1/robots")
async def root():
    return [{"id": robot.get_name()} for robot in robots if robot.get_name() is not None]


@app.post("/v1/robots/{robot_id}/task")
async def root(robot_id: str, task: dict):
    robot = next((robot for robot in robots if robot.get_name() == robot_id), None)
    if robot is None:
        return {"error": "Robot not found"}
    
    robot.attach_task(task["name"], task["system_prompt"])
    return {"message": "Task attached successfully"}
