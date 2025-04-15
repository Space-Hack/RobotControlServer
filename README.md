# RobotControlServer

A FastAPI-based server application for robot control and AI integration. This project provides a robust backend system for managing robot operations, handling WebSocket connections, and integrating AI capabilities.

## Features

- FastAPI-based REST API
- WebSocket support for real-time communication
- AI integration capabilities
- Modular architecture with separate components for:
  - API endpoints
  - WebSocket handling
  - AI processing
  - Command parsing
  - Worker management

## Project Structure

```
RobotControlServer/
├── src/
│   ├── ai.py           # AI integration and processing
│   ├── api.py          # REST API endpoints
│   ├── main.py         # Main application entry point
│   ├── my_types.py     # Custom type definitions
│   ├── parser.py       # Command parsing logic
│   ├── socketHandler.py # WebSocket connection handling
│   └── worker.py       # Worker process management
├── test_client/        # Test client implementation
├── requirements.txt    # Python dependencies
└── .devcontainer.json  # Development container configuration
```


## Running the Server

1. Start the server:
   ```bash
   uvicorn src.main:app --reload
   ```

2. The server will be available at:
   - API: http://localhost:8000
   - WebSocket: ws://localhost:8000/ws

## Development

- The project uses FastAPI for the REST API
- WebSocket connections are handled through the `socketHandler.py` module
- AI integration is implemented in `ai.py`
- Command parsing is managed by `parser.py`
- Worker processes are controlled through `worker.py`
