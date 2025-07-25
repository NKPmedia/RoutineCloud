# RoutineCloud

![RoutineCloud Logo](routinecloud.png)

A web application with a Vue.js frontend, Express.js backend, and a FastAPI-based Raspberry Pi component for controlling a child's bedtime routine.

## Project Structure

```
RoutineCloud/
├── backend/             # FastAPI backend for Raspberry Pi
│   ├── main.py          # Main entry point
│   ├── fastapi_server.py # REST API endpoints
│   ├── routine_state.py # Shared singleton state
│   ├── display_thread.py # Pygame thread for display and sound
│   ├── ws_client.py     # WebSocket client for cloud connection
│   ├── bedtime_routine.service # Systemd service file
│   ├── requirements.txt # Python dependencies
│   └── README.md        # Backend documentation
│
└── frontend/            # Vue.js frontend (created with npm create vue@latest)
    ├── public/          # Static assets
    ├── src/             # Source files
    │   ├── assets/      # Static assets for the application
    │   ├── components/  # Vue components
    │   ├── router/      # Vue Router configuration
    │   ├── stores/      # Pinia stores
    │   ├── views/       # Vue views
    │   ├── App.vue      # Root component
    │   └── main.ts      # Entry point
    ├── .gitignore       # Frontend gitignore
    ├── package.json     # Frontend dependencies
    ├── tsconfig.json    # TypeScript configuration
    └── vite.config.ts   # Vite configuration
```

## Components

### Cloud Server (Not Yet Implemented)
The cloud server will be an Express.js backend that provides:
- User authentication
- Routine management
- WebSocket server for communicating with Raspberry Pi devices

### Frontend (Not Yet Implemented)
A Vue.js frontend that provides:
- User interface for managing routines
- Dashboard for monitoring Raspberry Pi devices
- Controls for starting/stopping routines remotely

### Raspberry Pi Backend
A FastAPI-based backend that runs on a Raspberry Pi and provides:
- Visual display of the current task using pygame
- Sound playback for each task
- REST API for local control
- WebSocket client for receiving commands from the cloud server

## Setup Instructions

### Raspberry Pi Backend

See the [backend README](backend/README.md) for detailed setup instructions.

Quick start:
```bash
cd backend
pip install -r pyproject.toml
python main.py
```

### Frontend (When Implemented)

```bash
cd frontend
npm install
npm run dev  # Start the development server
```

## Development

- Raspberry Pi Backend runs on: http://localhost:8000
- Frontend runs on: http://localhost:5173 (default Vite dev server port)

## Building for Production

### Frontend (When Implemented)

```bash
cd frontend
npm run build
```

### Raspberry Pi Backend

See the [backend README](backend/README.md) for instructions on setting up the systemd service for production deployment.
