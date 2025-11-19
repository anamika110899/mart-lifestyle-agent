# Demo Video Script for Kaggle Capstone Submission

## 1. Problem Statement
Writing and managing daily productivity tasks manually is time-consuming. Our Concierge Agent automates task management.

## 2. Agents
We created a Productivity Concierge Agent using FastAPI that handles tasks via AI-powered logic.

## 3. Architecture
- main.py → FastAPI server
- agents/ → AI agent logic
- tools/ → helper functions
- memory/ → stores tasks in session memory

## 4. Demo
- GET / → check server is running
- GET /tasks → view default tasks
- POST /tasks → add new task and store in memory

## 5. Build
- Python 3.13
- FastAPI, Uvicorn, Pydantic
- Run `uvicorn main:app --reload` to start server
